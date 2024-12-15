import time
import redis

r = redis.Redis(
    host="5.tcp.eu.ngrok.io",
    port=19516,
)

timeout = 60

for _ in range(timeout):
    r.publish("heartbeat", "❤️")
    time.sleep(1.0)
