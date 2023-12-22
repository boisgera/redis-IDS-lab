import json
import threading

import redis

FOREVER = threading.TIMEOUT_MAX

r = redis.Redis(
    host = "redis-18650.c325.us-east-1-4.ec2.cloud.redislabs.com",
    port = "18650",
    password = "sMvW0CnKQG1A3Y8QYAgtZXn6epWm1AQ6"
)
p = r.pubsub()

p.subscribe("boisgera")
m = p.get_message(timeout=FOREVER)
assert m["type"] == "subscribe"

inbox = [] 

def fetch():
    while True:
        m = p.get_message()
        if m is None:
            return
        try:
            inbox.append(json.loads(m["data"].decode("utf-8")))
        except Exception as e:
            print(type(e).__name__, e)

def send(message):
    target = message["to"] 
    r.publish(target, json.dumps(message))   
