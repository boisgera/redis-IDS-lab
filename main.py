import json
import time

import redis

r = redis.Redis(
    host = "redis-18650.c325.us-east-1-4.ec2.cloud.redislabs.com",
    port = "18650",
    password = "sMvW0CnKQG1A3Y8QYAgtZXn6epWm1AQ6"
)

p = r.pubsub()

p.subscribe("my-first-channel")
time.sleep(1.0)
p.get_message()

while True:
    time.sleep(1.0)
    message = p.get_message()
    if message is not None:
        try:
            json_str = message["data"].decode("utf-8")
            json_data = json.loads(json_str)
            name = json_data["name"]
            message = json_data["message"]
            print(f"{name}: {message}")
        except Exception as e:
            print("🔥🔥🔥 Invalid message")
            print(type(e).__name__, e)
            print(message["data"])
            continue

