package main

import (
	"apps"
	"context"
	"fmt"

	"github.com/redis/go-redis/v9"
)

// TODO: supervise and restart the heartbeat service if needed?

// Nota: there is no need to check the heartbeat ALL THE TIME.
//       instead when needed, we can subscribed to the channel,
//       wait for 2 seconds and if there is no heartbeat,
//       restart the heartbeat service.

func main() {
	ctx := context.Background()
	address := fmt.Sprintf("%s:%d", apps.Host, apps.Port)
	rdb := redis.NewClient(
		&redis.Options{
			Addr: address,
		})

	pubsub := rdb.Subscribe(ctx, "heartbeat")
	defer pubsub.Close()

	// Get the channel to receive messages
	ch := pubsub.Channel()

	for msg := range ch {
		fmt.Println(msg.Payload)
	}
}
