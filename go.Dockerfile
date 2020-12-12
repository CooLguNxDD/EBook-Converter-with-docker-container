FROM golang:1.15


WORKDIR /app

RUN go get -d -v github.com/streadway/amqp github.com/google/uuid
RUN go install -v github.com/streadway/amqp github.com/google/uuid

COPY . .
CMD TIMEOUT 10
CMD go run ebook_project/go/convertion_server.go
