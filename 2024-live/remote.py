import json
import datetime
import time
import cloudpickle
import base64

import redis
import requests

r = redis.Redis(
    host="5.tcp.eu.ngrok.io",
    port=19516,
)
FOREVER = 3600*24

p = r.pubsub()
p.subscribe("remote")
p.get_message(timeout=FOREVER) # subscribe ack.

while True:
    m = p.get_message(timeout=FOREVER)
    try:
        data = m["data"]
    except:
        print("ERROR")
        continue
    print(m)

    json_data = json.loads(data)
    channel = json_data["channel"]
    payload = json_data["payload"]
    payload = base64.b64decode(payload)
    f = cloudpickle.loads(payload)

    result = f()

    output = cloudpickle.dumps(result)

    r.publish(channel, output)
