import marimo

__generated_with = "0.9.34"
app = marimo.App(width="medium")


@app.cell
def __():
    import base64
    import json
    import time
    return base64, json, time


@app.cell
def __():
    import marimo as mo
    import numpy
    return mo, numpy


@app.cell
def __():
    import openai
    return (openai,)


@app.cell
def __():
    import cloudpickle
    return (cloudpickle,)


@app.cell
def __():
    import requests
    return (requests,)


@app.cell
def __():
    FOREVER = 3600 * 24
    return (FOREVER,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""Service public redis : `tcp://4.tcp.eu.ngrok.io:16961`""")
    return


@app.cell
def __():
    import redis
    return (redis,)


@app.cell
def __(mo):
    mo.md(r"""Redis conn. info : `tcp://5.tcp.eu.ngrok.io:19516`""")
    return


@app.cell
def __(redis):
    r = redis.Redis(
        host="5.tcp.eu.ngrok.io",
        port=19516,
        #decode_responses=True, # temporary
    )
    return (r,)


@app.cell
def __(r):
    r.ping()
    return


@app.cell
def __(r):
    r.set("réponse", "Sébastien".encode("utf-8"))
    return


@app.cell
def __(r):
    val = r.get("réponse")
    val
    return (val,)


@app.cell
def __(mo):
    mo.md(r"""## Publish-Subscribe""")
    return


@app.cell
def __(r):
    p = r.pubsub()
    return (p,)


@app.cell
def __(r):
    r.publish("general", b"DATA ...") # 0 subscribers so far
    return


@app.cell
def __(p):
    p.subscribe("general")
    return


@app.cell
def __(p):
    p.get_message()
    return


@app.cell
def __(r):
    r.publish("general", b"ANOTHER DATA CHUNK")
    return


@app.cell
def __(p):
    p.get_message() is None
    return


@app.cell
def __(FOREVER, p):
    p.get_message(timeout=FOREVER)
    return


@app.cell
def __(r, time):
    def start_heartbeat(timeout=60):
        for _ in range(timeout):
            r.publish("heartbeat", "❤️")
            time.sleep(1.0)
    return (start_heartbeat,)


@app.cell
def __(start_heartbeat):
    start_heartbeat(60)
    return


@app.cell
def __(FOREVER, r):
    def check_heartbeat():
        "Return True/False"
        p = r.pubsub()
        p.subscribe("heartbeat")
        s = p.get_message(timeout=FOREVER) 
        m = p.get_message(timeout=2.0)
        p.unsubscribe() 
        return m is not None
    return (check_heartbeat,)


@app.cell
def __(check_heartbeat):
    check_heartbeat()
    return


@app.cell
def __():
    import datetime
    return (datetime,)


@app.cell
def __(datetime):
    str(datetime.datetime.now())
    return


@app.cell
def __(FOREVER, r):
    MYSELF = "boisgera"
    p_inbox = r.pubsub()
    p_inbox.subscribe(MYSELF)
    p_inbox.get_message(timeout=FOREVER) # confir subsc.
    return MYSELF, p_inbox


@app.cell
def __(MYSELF, p_inbox, r):
    r.publish("clock", MYSELF)
    m_ = p_inbox.get_message(timeout=10.0)
    print(m_["data"])
    return (m_,)


@app.cell
def __(requests):
    response = requests.get("http://api.open-notify.org/iss-now.json")
    if response.status_code == 200: # Everything's fine
        data = response.json()
    data
    return data, response


@app.cell
def __(data):
    type(data)
    return


@app.cell
def __(data, json):
    data_as_str = json.dumps(data)
    data_as_str
    return (data_as_str,)


@app.cell
def __(data_as_str):
    type(data_as_str)
    return


@app.cell
def __(data_as_str, json):
    json.loads(data_as_str)
    return


@app.cell(hide_code=True)
def __(FOREVER, MYSELF, json, r):
    p2 = r.pubsub()
    p2.subscribe(MYSELF)
    p2.get_message(timeout=FOREVER)

    r.publish("ISS", MYSELF)
    _m = p2.get_message(timeout=FOREVER)
    data_ISS = _m["data"]
    position = json.loads(data_ISS.decode("utf-8"))["iss_position"]
    lat = float(position["latitude"])
    lon = float(position["longitude"])
    p2.unsubscribe()
    lat, lon
    return data_ISS, lat, lon, p2, position


@app.cell
def __(lat, lon):
    import folium
    from folium import plugins

    location = [lat, lon]

    # Create a new Folium map object
    m = folium.Map(location=location, zoom_start=3)

    # Add a marker for the ISS station
    m.add_child(folium.Marker(location=location, popup='ISS Station'))

    # Display the map
    m

    return folium, location, m, plugins


@app.cell
def __():
    import math
    def f():
        return math.factorial(42)
    return f, math


@app.cell
def __(f):
    f()
    return


@app.cell
def __(cloudpickle, f):
    f_bin = cloudpickle.dumps(f) # binary data!
    f_bin
    return (f_bin,)


@app.cell
def __(base64, f_bin):
    f_base64 = base64.b64encode(f_bin)
    f_base64.decode("ascii")
    return (f_base64,)


@app.cell
def __(FOREVER, MYSELF, base64, cloudpickle, f, json, r):
    def remote_f(channel):
        payload = cloudpickle.dumps(f) # desc. of f as binary data
        payload_str = base64.b64encode(payload).decode("ascii")
        data = {"channel": MYSELF, "payload": payload_str}
        
        p = r.pubsub()
        p.subscribe(MYSELF)
        p.get_message(timeout=FOREVER)

        r.publish(channel, json.dumps(data))

        # Protocol: the answer is made of the binary generated by 
        # cloudpickle
        m = p.get_message(timeout=FOREVER)
        data = m["data"]
        result = cloudpickle.loads(data)
        return result
    return (remote_f,)


@app.cell
def __(remote_f):
    remote_f(channel="remote")
    return


@app.cell
def __(f):
    f()
    return


if __name__ == "__main__":
    app.run()
