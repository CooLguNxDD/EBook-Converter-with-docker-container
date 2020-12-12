package main

type Worker interface {
	Run() interface{}
}

type EBookElementQueue struct {
	Jobs          chan Worker
	ResultElement chan interface{}
}

func Create(nWorkers uint, maxPage uint) *EBookElementQueue {
	// initial
	queue := new(EBookElementQueue)
	queue.Jobs = make(chan Worker, maxPage)
	return queue
}
