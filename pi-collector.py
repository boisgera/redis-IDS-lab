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

p.subscribe("pi-collector")
m = p.get_message(timeout=FOREVER)
assert m["type"] == "subscribe"

partial_results = []
start = time.time()

while True:
    m = p.get_message(timeout=FOREVER)
    if m is not None:
        try:
            data = m["data"].decode("utf-8")
            pi_approx = float(data)
            partial_results.append(pi_approx)
            sigma = np.sqrt(4*(np.pi/4)*(1-np.pi/4)/(n*len(partial_results)))
            pi_mean = np.mean(partial_results)

            elapsed = time.time() - start
            if elapsed > 5.0:
                start = time.time()
                print(f"{pi_mean:.17f} ± {3*sigma:.5g}")
        except Exception as e:
            print("🔥🔥🔥 Invalid Pi Collector Data")
            print(type(e).__name__, e)
            print(m["data"])

