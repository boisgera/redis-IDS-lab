import json
import datetime
import time

import redis
import requests

r = redis.Redis(
    host="5.tcp.eu.ngrok.io",
    port=19516,
)
FOREVER = 3600*24

p = r.pubsub()
p.subscribe("ISS")
p.get_message(timeout=FOREVER) # subscribe ack.

while True:
    m = p.get_message(timeout=FOREVER)
    try:
        channel = m["data"]
    except:
        print("ERROR")
        continue
    print(m)
    
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code == 200: # Everything's fine
        data = json.dumps(response.json())
        r.publish(channel, data)

        print(data)
        time.sleep(1.0)
