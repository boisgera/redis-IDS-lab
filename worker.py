# Python Standard Library
import os
import cloudpickle as pickle
import sys

# Third-Party Libraries
import redis

r = redis.Redis(
      host='redis-14706.c275.us-east-1-4.ec2.cloud.redislabs.com',
      port=14706,
      password="w84kju6EutdIMHOQXyAvC2kefA1SGQpx"
)
p = r.pubsub()

sender = sys.argv[1]

pid = os.getpid()
p.subscribe(pid)
p.get_message(timeout=3600.0)

print(pid, flush=True)

d = pickle.loads(p.get_message(timeout=3600.0)["data"])
out = d["function"](*d["args"])
r.publish(sender, pickle.dumps({"result": out, "id": d["id"]}))
