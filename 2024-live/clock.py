import datetime
import time
import redis

r = redis.Redis(
    host="5.tcp.eu.ngrok.io",
    port=19516,
)
FOREVER = 3600*24

p = r.pubsub()
p.subscribe("clock")
p.get_message(timeout=FOREVER) # subscribe ack.

while True:
    m = p.get_message(timeout=FOREVER)
    try:
        channel = m["data"]
    except:
        print("ERROR")
        continue
    print(m)
    now = str(datetime.datetime.now())
    print(channel, now)
    r.publish(channel, now)
