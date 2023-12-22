import json
import os
import platform
import numpy as np  
import numpy.random as npr

import redis

r = redis.Redis(
    host = "redis-18650.c325.us-east-1-4.ec2.cloud.redislabs.com",
    port = "18650",
    password = "sMvW0CnKQG1A3Y8QYAgtZXn6epWm1AQ6"
)

n = 100_000_000 # size arr: 800 Mo

pid = os.getpid()
name = platform.node()

print(pid)
print(name)

name = f"{name}-{pid}"

while True:
    x = npr.uniform(0.0, 1.0, n)
    y = npr.uniform(0.0, 1.0, n)

    arr = (x**2 + y**2 <= 1.0).astype(np.float64)
    pi_approx = 4.0 * np.mean(arr)

    json_data = {"name": name, "pi": pi_approx}
    r.publish("pi-collector-2", json.dumps(json_data).encode("utf-8"))