# Python Standard Library
import base64
import json
import os
import threading
import time

FOREVER = threading.TIMEOUT_MAX

# Third-Party Libraries
import cloudpickle as cp
import redis
import requests

# If you are the one tunneling the redis service, we can ask ngrok what the public name and port are
res = requests.get(
    "http://127.0.0.1:4040/api/tunnels"
)  # see https://ngrok.com/docs/agent/api/
ngrok_info = res.json()
URL = ngrok_info["tunnels"][0]["public_url"]
HOST, PORT = URL[6:].split(":")
PORT = int(PORT)
CHANNEL = "boisgera"

TO = "COMPUTE"
SUBJECT = ""

r = redis.Redis(host=HOST, port=PORT)
p = r.pubsub()
p.subscribe(CHANNEL)
p.get_message(timeout=FOREVER)


def f():
    import math
    return math.factorial(42)

r.publish(TO, json.dumps({
    "from": CHANNEL,
    "subject": SUBJECT,
    "body": base64.b64encode(cp.dumps(f)).decode("utf-8")
}))
m = p.get_message(timeout=FOREVER)
print("**")
print(m)