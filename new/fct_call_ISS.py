# Python Standard Library
import json
import os
import threading
import time

FOREVER = threading.TIMEOUT_MAX

# Third-Party Libraries
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

TO = "ISS"
SUBJECT = ""

r = redis.Redis(host=HOST, port=PORT)
p = r.pubsub()
p.subscribe(CHANNEL)
p.get_message(timeout=FOREVER)


def get_ISS_info():
    r.publish("ISS", json.dumps({
        "from": CHANNEL,
        "subject": "Hey pls answer me!",
        "body": ""
    }))
    m = p.get_message(timeout=FOREVER)
    return json.loads(m["data"])["body"]

if __name__ == "__main__":
    print(get_ISS_info())