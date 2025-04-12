import os
import time

from flask import Flask
from flask import render_template_string
from flask import request

#https://stackoverflow.com/questions/60828641/simplest-way-to-perform-logging-from-google-cloud-run
#https://cloud.google.com/logging/docs/setup/python
import google.cloud.logging
import logging

app = Flask(__name__)

cname = os.environ.get("CONTAINER_NAME", "Unknown")
appkey = os.environ.get("FAKE_API_KEY", "Unknown")

@app.route("/")
def hello_world():
    """Example Hello World route."""
    name = os.environ.get("NAME", "World")
    return f"Hello {name}!"

@app.route("/info")
def get_info():
    apptoken = os.environ.get("FAKE_API_TOKEN", "Unknown")
    return f"INFO: cname/appkey/apptoken : {cname}/{appkey}/{apptoken}"

@app.route("/health")
def get_health():
    time_sec = time.time() 
    return f"OK @ {time_sec}"

@app.route("/sleep5")
def get_sleep5():
    time_sec = time.time()
    formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_sec))
    time.sleep(5)
    time_diff = time.time() - time_sec
    apptoken = os.environ.get("FAKE_API_TOKEN", "Unknown")
    return f"HEALTHZ by apptoken : {apptoken} received at {formatted_time} with diff {time_diff}"

@app.route("/delay", defaults={'duration': None}, methods=['GET', 'POST'])
@app.route("/delay/<duration>", methods=['GET', 'POST'])
def get_delay(duration):
    #if request.method == 'GET':
    #    username = request.args['username']
    #    passkey = request.args['passkey']
    # Instantiates a client
    client = google.cloud.logging.Client()

    # Connects the logger to the root logging handler; by default this captures
    # all logs at INFO level and higher
    client.setup_logging()

    request_type = request.method
    if duration is None:
        duration = 5
    duration = int(duration)
    time_sec = time.time()
    time.sleep(duration)
    time_diff = time.time() - time_sec

    logging.info(f"method:{request_type}, start at {time_sec}, delta was {time_diff}")
    return f"[{request_type}]::Delay request({duration}) received at {time_sec} with time difference {time_diff}"

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template_string('PageNotFound {{ errorCode }} !!!', errorCode='404'), 404

if __name__ == "__main__":
    app.run(debug=True, host="1.0.0.0", port=int(os.environ.get("PORT", 8080)))