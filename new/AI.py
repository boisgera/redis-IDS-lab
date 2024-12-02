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
CHANNEL = "AI"

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

# Python Standard Library
import json
import sys

# Third-Party
import requests

SERVER = "http://localhost:11434"
url = f"{SERVER}/api/generate"

def answer(prompt):
    results = []
    json_data = {"model": "mistral", "prompt": prompt}
    response = requests.post(url, json=json_data, stream=True)
    if response.status_code == 200:
        for response_line in response.iter_lines():
            json_line = response_line.decode("utf-8")
            answer = json.loads(json_line)
            if not answer["done"]:
                results.append(answer["response"])
            else:
                break
    else:
        response.raise_for_status()
    return "".join(results)

while True:
    inbox += fetch()
    os.system("cls" if os.name == "nt" else "clear")
    for m in inbox:
        d = json.loads(m["data"])
        from_ = d["from"]
        subject = d["subject"]
        prompt = d["body"]
        answer_ = answer(prompt)
        print({
            "from": CHANNEL,
            "subject": subject,
            "body": answer
        })
        r.publish(from_, json.dumps({
            "from": CHANNEL,
            "subject": subject,
            "body": answer_
        }))
    inbox[:] = []

    time.sleep(0.1)
