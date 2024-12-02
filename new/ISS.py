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
CHANNEL = "ISS"

r = redis.Redis(host=HOST, port=PORT)
p = r.pubsub()
p.subscribe(CHANNEL)
p.get_message(timeout=FOREVER)

inbox = []

def fetch():
    messages = []
    while (m := p.get_message()) is not None:
        messages.append(m)
    return messages

while True:
    inbox += fetch()
    os.system("cls" if os.name == "nt" else "clear")
    for m in inbox:
        d = json.loads(m["data"])
        from_ = d["from"]
        subject = d["subject"]
        rep = requests.get("http://api.open-notify.org/iss-now.json").json()
        r.publish(from_, json.dumps({
            "from": CHANNEL,
            "subject": subject,
            "body": rep
        }))
    inbox[:] = []

    time.sleep(0.1)
