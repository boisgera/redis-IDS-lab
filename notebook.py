import marimo

__generated_with = "0.9.12"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md("""## Configure and Test the Redis Server""")
    return


@app.cell
def __():
    """
    redis_conf = (
        mo.md('''
        **Redis Server Configuration**

        {host}

        {port}
    ''')
        .batch(
            host=mo.ui.text(label="host", value="localhost"),
            port=mo.ui.text(label="port", value="6379"),
        )
        .form(show_clear_button=True, bordered=False)
    )
    """
    return


@app.cell
def __():
    # redis_conf
    return


@app.cell
def __():
    HOST = "localhost"
    PORT = "6379"
    return HOST, PORT


@app.cell
def __(HOST, PORT, mo, redis):
    r = redis.Redis(host=HOST, port=PORT)

    try:
        status = r.ping()
    except redis.ConnectionError:
        status = False

    mo.md(f"**Redis Server Status**: {'✅' if status else '❌'}")
    return r, status


@app.cell
def __(mo):
    mo.md("""## Publish-Subscribe""")
    return


@app.cell
def __(FOREVER, r):
    p = r.pubsub()
    myself = "boisgera"
    p.subscribe(myself)
    p.get_message(timeout=FOREVER)
    return myself, p


@app.cell
def __(FOREVER, p, r):
    r.publish("boisgera", "Hello boisgera! 👋")
    p.get_message(timeout=FOREVER)
    return


@app.cell
def __(FOREVER, p, r):
    r.publish("boisgera", "Hello boisgera! 👋")
    _msg = p.get_message(timeout=FOREVER)
    _msg["data"].decode("utf-8")
    return


@app.cell
def __(FOREVER, p, r):
    _bytes = "Hello boisgera! 👋".encode("utf-8")
    r.publish("boisgera", _bytes)
    _msg = p.get_message(timeout=FOREVER)
    _msg["data"].decode("utf-8")
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
def __(fetch, get_inbox, pd):
    fetch()
    inbox = get_inbox()
    pd.DataFrame(inbox)
    return (inbox,)


@app.cell
def __(r):
    r.publish("boisgera", b"zzzzz")
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
    "inbox" in globals()
    return


@app.cell
def __(message_sender, r):
    message_info = message_sender.value
    r.publish(message_info["to"], message_info["message"])
    return (message_info,)


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
    import threading

    # Third-Party Libraries
    import marimo as mo
    import pandas as pd
    import redis
    return mo, pd, redis, threading


@app.cell
def __(threading):
    FOREVER = threading.TIMEOUT_MAX
    return (FOREVER,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
