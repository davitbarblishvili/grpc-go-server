package main

import (
	"context"
	"fmt"
	"grpc_go/greetings/calculator/calculatorpb"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	fmt.Println("Calculator Client")
	cc, err := grpc.Dial("localhost:50058", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("Could not connect: %v\n", err)
	}

	defer cc.Close()

	c := calculatorpb.NewCalculatorServiceClient(cc)

	//doUnary(c)
	//doServerStreaming(c)
	//doClientStreaming(c)
	doBiDiStreaming(c)
}

func doBiDiStreaming(c calculatorpb.CalculatorServiceClient) {
	fmt.Println("Starting to do a ComputeAverage Client Streaming RPC")
	stream, err := c.FindMaximum(context.Background())
	if err != nil {
		log.Fatalf("Error while creating stream: %v", err)
	}

	requests := []int32{1, 20, 3, 40, 5, 2, 75, 40, 120, 300, 3, 1200, 56}

	waitc := make(chan struct{})

	go func() {
		for _, req := range requests {
			fmt.Printf("Sending message: %v\n", req)
			stream.Send(&calculatorpb.FindMaximumRequest{Number: req})
			time.Sleep(1000 * time.Millisecond)
		}
		stream.CloseSend()
	}()

	go func() {
		for {
			res, err := stream.Recv()

			if err == io.EOF {
				break
			}
			if err != nil {
				log.Fatalf("Error while receiving: %v\n", err)
				break
			}

			fmt.Printf("Received : %v\n", res.GetMaximum())
		}
		close(waitc)

	}()

	<-waitc

}

func doClientStreaming(c calculatorpb.CalculatorServiceClient) {
	fmt.Println("Starting to do a ComputeAverage Client Streaming RPC")

	requests := []int32{1, 2, 3, 4, 5}
	stream, err := c.ComputeAverage(context.Background())

	if err != nil {
		log.Fatalf("Error while calling ComputeAverage RPC: %v", err)
	}

	for _, req := range requests {
		fmt.Printf("Sending request: %v\n", req)
		stream.Send(&calculatorpb.ComputeAverageRequest{
			Number: req,
		})

	}

	resp, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatalf("Error while receiving response from ComputeAverage: %v", err)
	}
	fmt.Printf("ComputeAverage response: %v\n", resp.GetResult())

}

func doServerStreaming(c calculatorpb.CalculatorServiceClient) {
	fmt.Println("Starting to do a PrimeDecomposition Client Streaming RPC")
	req := &calculatorpb.PrimeNumberDecompositionRequest{
		Number: 48,
	}
	stream, err := c.PrimeNumberDecomposition(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling PrimeDecomposition RPC: %v", err)

	}
	for {
		res, err := stream.Recv()
		if err == io.EOF {
			break
		}

		if err != nil {
			log.Fatalf("Something happened: %v", err)
		}

		fmt.Println(res.GetPrimeFactor())

	}
}

func doUnary(c calculatorpb.CalculatorServiceClient) {
	fmt.Println("Starting to do a Sum Unary RPC")
	req := &calculatorpb.SumRequest{
		FirstNumber:  5,
		SecondNumber: 40,
	}
	res, err := c.Sum(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Greet RPC: %v", err)

	}
	log.Printf("Response from Sum: %v", res.SumResult)

}
