package main

import (
	"context"
	"fmt"
	"grpc_go/greetings/greet/greetpb"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	fmt.Println("Hello I am a client")
	cc, err := grpc.Dial("localhost:50057", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("could not connect: %v\n", err)
	}

	defer cc.Close()

	c := greetpb.NewGreetServiceClient(cc)

	//doUnary(c)
	//doServerStreaming(c)
	//doClientStreaming(c)
	doBiDiStreaming(c)

}

func doBiDiStreaming(c greetpb.GreetServiceClient) {
	fmt.Println("Starting to do a BiDi Streaming RPC")

	stream, err := c.GreetEveryone(context.Background())
	if err != nil {
		log.Fatalf("Error while creating stream: %v", err)
	}
	requests := []*greetpb.GreetEveryoneRequest{
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Davit",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Ana",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Mitsuki",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "David",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Moira",
			},
		},
	}

	waitc := make(chan struct{})

	go func() {
		for _, req := range requests {
			fmt.Printf("Sending message: %v\n", req)
			stream.Send(req)
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

			fmt.Printf("Received : %v\n", res.GetResult())
		}
		close(waitc)

	}()

	<-waitc

}

func doClientStreaming(c greetpb.GreetServiceClient) {
	fmt.Println("Starting to do a Client Streaming RPC")
	requests := []*greetpb.LongGreetRequest{
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Davit",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Ana",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Mitsuki",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "David",
			},
		},
		{
			Greeting: &greetpb.Greeting{
				FirstName: "Moira",
			},
		},
	}
	stream, err := c.LongGreet(context.Background())
	if err != nil {
		log.Fatalf("error while calling long greet: %v", err)
	}

	for _, req := range requests {
		fmt.Printf("Sending request: %v\n", req)
		stream.Send(req)
		time.Sleep(1000 * time.Millisecond)
	}

	resp, err := stream.CloseAndRecv()
	if err != nil {
		log.Fatalf("Error while receiving response from long greet: %v", err)
	}
	fmt.Printf("LongGreet response: %v\n", resp)

}

func doServerStreaming(c greetpb.GreetServiceClient) {
	fmt.Println("Starting to do a Server Streaming RPC")
	req := &greetpb.GreetManyTimesRequest{
		Greeting: &greetpb.Greeting{
			FirstName: "Davit",
			LastName:  "Barblishvili",
		},
	}
	res_stream, err := c.GreetManyTimes(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling GreetManyTime RPC: %v", err)
	}

	for {
		msg, err := res_stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("Error while reading stream: %v", err)
		}

		log.Printf("Response from GreetManyTimes: %v", msg.GetResult())

	}

}

func doUnary(c greetpb.GreetServiceClient) {
	fmt.Println("Starting to do a Unary RPC")
	req := &greetpb.GreetRequest{
		Greeting: &greetpb.Greeting{
			FirstName: "Davit",
			LastName:  "Barblishvili",
		},
	}
	res, err := c.Greet(context.Background(), req)
	if err != nil {
		log.Fatalf("error while calling Greet RPC: %v", err)

	}
	log.Printf("Response from Greet: %v", res.Result)

}
