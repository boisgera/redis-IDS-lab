import json
import threading
import time

import numpy as np
import redis

FOREVER = 365 * 24 * 60 * 60 # or threading.TIMEOUT_MAX

r = redis.Redis(
    host = "redis-18650.c325.us-east-1-4.ec2.cloud.redislabs.com",
    port = "18650",
    password = "sMvW0CnKQG1A3Y8QYAgtZXn6epWm1AQ6"
)

n = 10_000_000 # size r: 80 Mo
p = r.pubsub()

p.subscribe("pi-collector-2")
m = p.get_message(timeout=FOREVER)
assert m["type"] == "subscribe"

partial_results = []
contributors = {}
start = time.time()

while True:
    m = p.get_message(timeout=FOREVER)
    if m is not None:
        try:
            json_str = m["data"].decode("utf-8")
            json_data = json.loads(json_str)
            # json_data = {"name": "wreck-5264", "pi": 3.1407}
            name = json_data["name"]
            pi_approx = json_data["pi"]
            contributors.setdefault(name, 0)
            contributors[name] += 1
            partial_results.append(pi_approx)
            sigma = np.sqrt(4*(np.pi/4)*(1-np.pi/4)/(n*len(partial_results)))
            pi_mean = np.mean(partial_results)

            elapsed = time.time() - start
            if elapsed > 5.0:
                print(40*"-")
                contributors = dict(sorted(contributors.items(), key=lambda x: x[1], reverse=True))
                for c in contributors:
                    print(c, contributors[c])
        except Exception as e:
            print("🔥🔥🔥 Invalid Pi Collector Data")
            print(type(e).__name__, e)
            print(m["data"])

