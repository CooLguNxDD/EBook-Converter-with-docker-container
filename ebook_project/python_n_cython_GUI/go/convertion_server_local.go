package main

import (
	"encoding/json"
	"github.com/streadway/amqp"
	"log"
	"strconv"
)

//rabbitMQ tutorial: https://www.rabbitmq.com/tutorials/tutorial-one-go.html
func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

//type HTMLFormat struct {
//	Page    int      `json:"page"`
//	Content []string `json:"content"`
//}

func toHtml(request map[string][]string) []map[int][]string {
	//var formatter []HTMLFormat
	var formatter []map[int][]string //dict(page:content)

	for page, element := range request {

		var htmlString []string
		htmlString = append(htmlString, "<?xml version='1.0' encoding='utf-8'?>\n")        //utf-8 encoding
		htmlString = append(htmlString, "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n") //html elements
		htmlString = append(htmlString, "   <head>\n")
		htmlString = append(htmlString, "      <title></title>\n")
		htmlString = append(htmlString, "      <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n")
		htmlString = append(htmlString, "</head>\n")
		htmlString = append(htmlString, "   <body>\n")

		pageInt := 0
		length := len(element)
		for i := 0; i < length; i++ {
			htmlString = append(htmlString, "   <p>\n")
			htmlString = append(htmlString, element[i])
			htmlString = append(htmlString, "   </p>\n")
		}
		htmlString = append(htmlString, "   </body>\n")
		htmlString = append(htmlString, "</html>\n")
		pageInt, _ = strconv.Atoi(page)
		formatter = append(formatter, map[int][]string{pageInt: htmlString})

		//formatter = append(formatter, HTMLFormat{
		//	Page:    pageInt,
		//	Content: element,
		//})
	}
	return formatter
}

func main() {
	//conn, err := amqp.Dial("amqp://rabbitmq:3/")
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/") //window
	failOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	failOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"local_queue", // name
		false,         // durable
		false,         // delete when unused
		false,         // exclusive
		false,         // no-wait
		nil,           // arguments
	)
	failOnError(err, "Failed to declare a queue")

	err = ch.Qos(
		1,     // prefetch count
		0,     // prefetch size
		false, // global
	)
	failOnError(err, "Failed to set QoS")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		false,  // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)
	failOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			var request map[string][]string
			json.Unmarshal(d.Body, &request)
			failOnError(err, "Failed to convert body")
			//log.Printf("%s", request)
			response := toHtml(request)
			body, err := json.Marshal(response)
			err = ch.Publish(
				"",        // exchange
				d.ReplyTo, // routing key
				false,     // mandatory
				false,     // immediate
				amqp.Publishing{
					ContentType:   "text/plain",
					CorrelationId: d.CorrelationId,
					Body:          body,
				})
			failOnError(err, "Failed to publish a message")

			d.Ack(false)
		}
	}()

	log.Printf("Awaiting RPC requests")
	<-forever
}
