package main

import (
	"apps"
	"context"
	"fmt"
	"time"

	"github.com/redis/go-redis/v9"
)

func main() {
	ctx := context.Background()
	address := fmt.Sprintf("%s:%d", apps.Host, apps.Port)
	rdb := redis.NewClient(
		&redis.Options{
			Addr: address,
		})
	ticker := time.NewTicker(1 * time.Second)
	defer ticker.Stop()
	for {
		<-ticker.C
		err := rdb.Publish(ctx, "heartbeat", "*").Err()
		if err != nil {
			panic(err)
		} else {
			fmt.Println("*")
		}
	}
}
