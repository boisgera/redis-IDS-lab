import marimo

__generated_with = "0.9.12"
app = marimo.App(width="medium", layout_file="layouts/notebook.slides.json")


@app.cell
def __(mo):
    mo.md(
        """
        # Distributed Computing (on top of Redis Pub-Sub)

        **Getting started**

          - Setup dev environment with [pixi](https://pixi.sh/latest/)

          - Get the info about the publicly exposed Redis server.

          - Connect to the server, ping it.

          - Test the put/get feature.

        **Publish-subscribe basics**

          - Shared channel

          - Work with strings/binary only

          - Dedicated publisher instance to read only what's in this channel

          - Read everything (filter out the first subscribe message?),

          - Use a marimo state to remember all past message and have an always
            up to date dataframe with the contents

        **Beyond binary messages**

          - TODO: JSON, 
          - TODO: messagepack?
          - TODO: cloudpickle? Later? Yes, to move the code closer to the data.

        **The Inbox pattern**

          - structured messages : JSON with from, to, subject, body
          - manual fetch
          - filtering & removal operations

        **Actors**

          - Use the Inbox pattern to make some queries, first, "textually" encoded
          - Sync/async patterns
          - ISS service : find the GPS location of the ISS and display it with leaflet
          - OLLAMA bot
          - encode payload with cloudpickle ; split, send & gather stuff like that?

        **Distributed Patterns**

          - Distribute computation, fan-out, map-reduce, supervision, etc.?
          - Examples of 'loads' : Crypto proof of work, STL marching cubes, etc.?
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Configure and Test the Redis Server

        Preamble: 

        - Start a redis server locally with `redis-server`,
        - Expose it publicly with `ngrok tcp 6379`.

        ℹ️ `fuser -k 6379/tcp` may come in handy to get rid of an old process using the port 6379.
        """
    )
    return


@app.cell
def __(requests):
    try: # If you are the one tunneling the redis service, we can ask ngrok what the public name and port are
        res = requests.get("http://127.0.0.1:4040/api/tunnels") # see https://ngrok.com/docs/agent/api/
        ngrok_info = res.json()
        URL = ngrok_info["tunnels"][0]["public_url"]
        HOST, PORT = URL[6:].split(":")
        PORT = int(PORT)
        HOST, PORT
    except requests.exceptions.ConnectionError: # Otherwise, fill these values manually
        HOST = None # 🚧 TODO
        PORT = None # 🚧 TODO
    f"""
    {HOST = }
    {PORT = }
    """
    return HOST, PORT, URL, ngrok_info, res


@app.cell
def __(HOST, PORT, redis):
    r_test = redis.Redis(host=HOST, port=PORT, decode_responses=True)
    return (r_test,)


@app.cell
def __(r_test):
    r_test.ping()
    return


@app.cell
def __(r_test):
    r_test.set("greetings", "Hello!")
    r_test.get("greetings")
    return


@app.cell
def __(mo):
    mo.md("""## Bytes (not strings) all the way""")
    return


@app.cell
def __(HOST, PORT, redis):
    r_test_2 = redis.Redis(host=HOST, port=PORT) # decode_responses = False is the default
    r_test_2.set("greetings", "Hello!")
    r_test_2.get("greetings") # Not a string anymore!
    return (r_test_2,)


@app.cell
def __(r_test_2):
    r_test_2.set("greetings", "Hello!".encode("utf-8")) # bytes in
    r_test_2.get("greetings").decode("utf-8") # bytes out
    return


@app.cell
def __(r_test_2):
    r_test_2.set("data", bytes(range(0, 256)))
    r_test_2.get("data")
    return


@app.cell
def __(mo):
    mo.md("""## Publish-Subscribe""")
    return


@app.cell
def __(FOREVER, HOST, PORT, redis):
    r = redis.Redis(host=HOST, port=PORT)
    p = r.pubsub()
    p.subscribe("general")
    assert p.get_message(timeout=FOREVER)["type"] == "subscribe"
    return p, r


@app.cell
def __():
    return


@app.cell
def __():
    """
    get_error, set_error = mo.state(None)
    get_latest_general, set_latest_general = mo.state(None)
    @background
    def watch_general():
        set_error(None)
        try:
            while True:
                m = p.get_message(timeout=FOREVER) 
                if m is not None:
                    set_latest_general(m)
        except Exception as e:
            set_error(e)

    watch_general()
    """
    return


@app.cell
def __():
    #get_error() # should be None
    return


@app.cell
def __(p):
    p.get_message()
    return


@app.cell
def __(mo):
    general_message = mo.ui.text_area(
        label="Message", placeholder="Type your message ..."
    )

    general_form = mo.md("""
    **Send a message to the "general" channel**

    {message}
    """).batch(
        message=general_message,
    ).form(clear_on_submit=True, bordered=False)
    general_form
    return general_form, general_message


@app.cell
def __(general_form, r):
    _gfv = general_form.value
    if _gfv is not None:
        r.publish("general", _gfv["message"])
    return


@app.cell
def __(mo):
    mo.md("""## Message passing and Structured Data""")
    return


@app.cell
def __(FOREVER, p):
    p.subscribe("json")
    p.get_message(timeout=FOREVER) # We're having issues with the background thread ...
    return


@app.cell
def __(datetime, json, r):
    now = datetime.datetime.now().isoformat()
    sender = "boisgera"
    r.publish("json", json.dumps({"time": now, "sender": sender}))
    return now, sender


@app.cell
def __(json, p):
    m = p.get_message()
    json.loads(m["data"])
    return (m,)


@app.cell
def __(mo):
    mo.md("""## Mailbox Pattern""")
    return


@app.cell
def __(p):
    me = "boisgera"
    p.subscribe(me)
    p.get_message(timeout=3.0)
    return (me,)


@app.cell
def __(mo):
    mo.md(
        """
        By convention, we want a JSON message with a 'from' field and some 'subject' and 'body'. Is that good enough?

        It's A START. At least if there is a reply to be done we know what channel we should forward it to.
        We could also have a 'reply-to' optional field.

        We'll have to adapt the things a bit later for distributed tasks, but the core issue is here: 
        every actor (human or "bot"/"service" has its own channel), we have an "id" (subject) to identify the thread if there are extra exchanges and we know who we should reply to (with the same subject).

        Then we can specialize this stuff with specific kind of messages that will be interpreted to make different kind of tasks.

        **TODO?**. Make a LLM bot with ollama running on my machine? I could do that. That's a nice example of actor/service.
        """
    )
    return


@app.cell
def __():
    # r.publish("boisgera", "Hello boisgera! 👋")
    # p.get_message(timeout=3.0)
    return


@app.cell
def __():
    # r.publish("boisgera", "Hello boisgera! 👋")
    # _msg = p.get_message(timeout=3.0)
    # _msg["data"].decode("utf-8")
    return


@app.cell
def __():
    #_bytes = "Hello boisgera! 👋".encode("utf-8")
    #r.publish("boisgera", _bytes)
    #_msg = p.get_message(timeout=3.0)
    #_msg["data"].decode("utf-8")
    return


@app.cell
def __():
    return


@app.cell
def __(mo):
    mo.md("""## Mailbox""")
    return


@app.cell
def __(mo):
    get_inbox, set_inbox = mo.state([])
    return get_inbox, set_inbox


@app.cell
def __(p, set_inbox):
    def fetch():
        while message := p.get_message():
            def update_inbox(inbox):
                inbox.append(message)
                return inbox
            set_inbox(update_inbox)
    return (fetch,)


@app.cell
def __():
    #fetch()
    #inbox = get_inbox()
    #pl.DataFrame(inbox)
    return


@app.cell
def __():
    # r.publish("boisgera", b"zzzzz")
    return


@app.cell
def __(mo):
    message_sender = (
        mo.md('''
        **Send a message**

        {to}

        {message}
    ''')
        .batch(
            to=mo.ui.text(label="To", value="boisgera"),
            message=mo.ui.text_area(label="Message", placeholder="Type your message ..."),
        )
        .form(show_clear_button=True, bordered=False)
    )
    return (message_sender,)


@app.cell
def __():
    return


@app.cell
def __(message_sender):
    message_sender
    return


@app.cell
def __():
    # "inbox" in globals()
    return


@app.cell
def __():
    #message_info = message_sender.value
    #r.publish(message_info["to"], message_info["message"])
    return


@app.cell
def __(mo):
    mo.md(
        """
        ## Sending structured data

        TODO:

          - add sender info
          - add date + time
          - add PJ!!! (file uploader -> file name + base64 encoding ?)
          - send Python global variables (that can be pickled)
          - change the "mail reader" (keep the old version as a "raw messages reader")
        """
    )
    return


@app.cell
def __():
    return


@app.cell
def __(mo):
    mo.md("""## Appendix""")
    return


@app.cell
def __():
    # Python Standard Library
    import datetime
    import json
    import threading
    import time

    # Third-Party Libraries
    import marimo as mo
    import polars as pl
    import plumbum 
    import quak
    import redis
    import requests
    return (
        datetime,
        json,
        mo,
        pl,
        plumbum,
        quak,
        redis,
        requests,
        threading,
        time,
    )


@app.cell
def __(threading):
    FOREVER = threading.TIMEOUT_MAX
    return (FOREVER,)


@app.cell
def __(mo):
    # threading.excepthook = lambda *_args: None # No message to stderr when the thread dies

    def background(fun):
        def _fun(*args, **kwargs):
            thread = mo.Thread(target=fun, name=fun.__name__, args=args, kwargs=kwargs)
            thread.start()
        return _fun
    return (background,)


if __name__ == "__main__":
    app.run()
