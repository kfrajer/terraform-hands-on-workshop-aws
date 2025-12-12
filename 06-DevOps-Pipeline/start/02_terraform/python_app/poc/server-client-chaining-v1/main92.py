## QUICK START
##
## pyenv virtualenv 3.12 venvads312
## pyenv activate venvads312
## pip install -r requirements.txt
##
## python main92.py --port 5000
## python main92.py --port 5001
## python main92.py --port 5002


"""
## SET ALIASES
  alias curlhealth='curl -X GET http://localhost:5000/health -H "Content-Type: application/json"'
  alias curloff00='curl -X POST http://localhost:5000/relay -H "Content-Type: application/json" -H "X-Trigger-External-Call: off" -H "X-Trigger-External-TracerID: dummytraceid" -H "X-Trigger-External-No-Resp-Propagation: on"'
  alias curloff01='curl -X POST http://localhost:5001/relay -H "Content-Type: application/json" -H "X-Trigger-External-Call: off" -H "X-Trigger-External-TracerID: dummytraceid" -H "X-Trigger-External-No-Resp-Propagation: on"'
  alias curlon00='curl -X POST http://localhost:5000/relay -H "Content-Type: application/json" -H "X-Trigger-External-Call: on" -H "X-Trigger-External-Curr-Counter: 0" -H "X-Trigger-External-TracerID: dummytraceid" -H "X-Trigger-External-No-Resp-Propagation: on"'


## SEND REQUESTS

  curloff00 -i -d '{}'; curloff01 -i -d '{}'; curlhealth

  curlon00 -i -d "{}"
  curlon00 -i -d '{"0": "http://localhost:5001/relay"}'
  curlon00 -d '{"0": "http://localhost:5001/relay", "1": "http://localhost:5000/relay", "2": "http://localhost:5001/relay"}'

## NEW SEND REQUESTS

  curlon00 -i -d '{ "data": {"quaz": "tarx"}, "queue": { "pod_a": {"url": "http://localhost:5001/relay", "delay": {"min": "2", "max": "2.1"}} } }'
  curlon00 -i -d '{ "data": {"foobar": "quaz"}, "queue": {"pod_a": {"url": "http://localhost:5001/relay", "delay": {"min": "0", "max": "0"}}, "pod_b": {"url": "http://localhost:5000/relay", "delay": {"min": "2.8", "max": "3.8"}}, "pod_c": {"url": "http://localhost:5001/relay", "delay": {"min": "0", "max": "0"}}  } }'

"""

import argparse
import random
import requests
import time

from datetime import datetime
from flask import Flask, request, jsonify, make_response
from functools import wraps



app = Flask(__name__)

# Sample words
fruits = ['apple', 'banana', 'cherry', 'mango', 'grape', 'kiwi', 'peach', 'pear', 'plum', 'orange']
colors = ['red', 'green', 'yellow', 'purple', 'orange', 'blue', 'pink', 'brown', 'white', 'black']
nouns = ['table', 'cloud', 'mountain', 'river', 'book', 'window', 'door', 'car', 'phone', 'house']
adjectives = ['happy', 'blue', 'tall', 'bright', 'noisy', 'quiet', 'quick', 'brave', 'smart', 'calm']

APP_HEADER_PREFIX = "X-Trigger-External-"
VALUE_NO_COUNTER = "-1"
VALUE_NO_TRACEID = "0"


def is_truly(value):
    return True if value and value.lower() in ("true", "on", "1") else False


def elapsed_time(func):
    """
    A decorator to measure the execution time of a function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Use perf_counter for more precise measurements
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")
        return result
    return wrapper


def make_custom_response(payload, response_stack, status_code, request, trace_id, curr_ctr):

    new_ctr = str(curr_ctr + 1) if curr_ctr != int(VALUE_NO_COUNTER) else VALUE_NO_COUNTER
    payload["curr_counter_request"] = new_ctr
    payload["trace_id"] = trace_id
    payload["local_time"] = datetime.now()
    payload["base_url"] = request.base_url

    key = "{}____{}".format(new_ctr, request.base_url)
    new_slot = {key: payload}

    response_payload = new_slot
    response_payload.update(response_stack)

    """Wraps a Flask JSON response with custom headers"""
    response = make_response(jsonify(response_payload), status_code)
    response.headers['X-Trigger-External-TracerID'] = trace_id
    response.headers['X-Trigger-External-Curr-Counter'] = new_ctr
    response.headers['X-completed'] = 'yes'

    return response

##TODO PRIORITY1 Input structure management
##TODO PRIORITY2 Proper propagation of data to next server and return this data so it is added to the stack
##TODO Make_custom_response as an object? Manage propagate_response flag in make_custom_response
##TODO Add loggging capabilities
##TODO hog memory
##TODO Make min/max delay optionalk
##TODO Create diagram of requests/responses in order to validate data output
##TODO Create UTEST

@app.route('/health', methods=['GET'])
def health_request():
    return jsonify({"message": "OK", "local_time": datetime.now()}), 200


@app.route('/relay', methods=['POST'])
@elapsed_time
def process_request():
    spyder_flag = request.headers.get('X-Trigger-External-Call', None)
    trace_id = request.headers.get('X-Trigger-External-TracerID', VALUE_NO_TRACEID)
    curr_request_ctr = request.headers.get('X-Trigger-External-Curr-Counter', VALUE_NO_COUNTER)
    propagate_response = request.headers.get('X-Trigger-External-No-Resp-Propagation', False)

    spyder_flag = is_truly(spyder_flag)
    propagate_response = is_truly(propagate_response)
    try:
        curr_request_ctr = int(curr_request_ctr)
    except ValueError:
        return make_custom_response({"error": "Invalid X-Trigger-External-Curr-Counter value, must be an int"}, {}, 400, request, trace_id, curr_ctr)

    data = request.get_json()

    ##Case spyder is off or not queue in payload
    if not spyder_flag or not data:
        return make_custom_response({
                                      "message": "Nothing done...",
                                      "local_time": datetime.now(),
                                      "base_url": request.base_url,
                                    },
                                    {},
                                    200,
                                    request,
                                    trace_id,
                                    curr_request_ctr
                                   )
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    ##WIP { "data": {"foobar": "quaz"}, "queue": {"pod_a": {"url": "http://pod_a/relay", "delay": {"min": "0", "max": "0"}}, "pod_b": {"url": "http://pod_b/relay", "delay": {"min": "2.8", "max": "3.8"}}} }

    queue = data.get("queue", {}) ## queue will contain the list of servers to reach
    res_data = data.get("data", {})   ## data will contain the random data from a (chained) request

    print("INFO::queue size {}".format(len(queue)))
    print("INFO::this is the queue: {}".format(queue))
    print("INFO::this is the res_data: {}".format(res_data))

    new_queue = {}
    min_delay = 0
    max_delay = 0
    queue_size = len(queue)
    if queue_size:
        first_key = next(iter(queue))
        first_value = queue.pop(first_key)
        next_url = first_value.get("url","EMPTY")
        ##TODO strict schema required or error handling
        min_delay = float(first_value.get("delay",{}).get("min", "0"))
        max_delay = float(first_value.get("delay",{}).get("max", "0"))
        new_queue = {"queue": queue}

    ## Cul-de-sac after poping element
    if queue_size == 0:
        selected_nouns = random.sample(nouns, 5)
        noun_adj_dict = {noun: random.choice(adjectives) for noun in selected_nouns}

        ##Only when propagate response is on
        noun_adj_dict.update(res_data)
        payload = {"data": noun_adj_dict} if propagate_response else {}
        stack = {}

        random_delay = random.uniform(min_delay, max_delay)
        time.sleep(random_delay)

        return make_custom_response(payload, stack, 200, request, trace_id, curr_request_ctr)

    ## Relay
    else:
        selected_fruits = random.sample(fruits, 5)
        fruit_color_dict = {fruit: random.choice(colors) for fruit in selected_fruits}

        try:
            headers = {k: request.headers.get(k, "UNKNOWN") for k in request.headers.keys() if k.startswith(APP_HEADER_PREFIX)}
            headers["X-Trigger-External-Curr-Counter"] = str(curr_request_ctr + 1) ## Update counter
            headers["Content-Type"] = "application/json"

            new_queue.update({"data": fruit_color_dict})

            response = requests.post(
                next_url,
                json=new_queue,
                ##WIP xxoo Send the data in request (?):  fruit_color_dict,
                headers = headers,
            )

            ## Introduce fake dekay - server supposely working hard
            ##TODO expose in return payload and logs
            random_delay = random.uniform(min_delay, max_delay)
            time.sleep(random_delay)

            stack = {}
            payload = {}
            if propagate_response:
                stack = response.json()

                payload = {
                    "status": "sent to external server",
                    #"data": fruit_color_dict, ##WIP xxoo Data should be managed/concatenated at the endpoint
                    "external_response_status": response.status_code
                }

            return make_custom_response(payload, stack, 200, request, trace_id, curr_request_ctr)

        except requests.RequestException as e:
            return make_custom_response({
                "error": "Failed to contact external API",
                "details": str(e)
            }, stack, 502, request, trace_id, curr_request_ctr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", dest="port", type=int, required=True, default=5000,
                        help="Port to start the server on")
    parser.add_argument("--no_debug", dest="no_debug", action='store_false',
                        required=False, default=True, help="Disable server debug")

    args = parser.parse_args()
    app.run(port=args.port, debug=args.no_debug)


## SAMPLE OUTPUT

"""
cmosquer@CMOSQUER-M-Q4XC python_app % curloff -d '{}' -i
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.13.3
Date: Sat, 27 Sep 2025 13:47:42 GMT
Content-Type: application/json
Content-Length: 141
X-Trigger-External-TracerID: dummytraceid
X-Trigger-External-Curr-Counter: 1
X-completed: yes
Connection: close

{"curr_request_ctr":"1","data":{"house":"quick","mountain":"smart","phone":"calm","river":"calm","window":"tall"},"trace_id":"dummytraceid"}
"""


## FULL FLOW

"""
## START
External client generates a request with proper headers:

curlon -d '{ "queue": {"pod_a": {"url": "http://pod_a/relay", "delay": "0"}, "pod_b": {"url": "http://pod_b/relay", "delay": "1000"}} }'

## POD_A

On receiving request:
* Extract headers
* Extracts payload

If no spyder: Return 'OK' status aka. ping response
If payload.queue is empty, then it returns standard response
If payload.queue is not empty then:
** Pop top entry from queue and gets next URL to send to. Note the queue has decreased by one by the pop o.
** Send request to URL.
** On response from external endpoint(URL):
  * It extracts response object
  * Creates self.response.payload (Standard response)
  * Stack self.response on top of received response
  * Returns stacked.payload

REMARK: What is a standard reponse?
message: OK
local_timestamp: Sat 27 Sep 2025 12:17:54 EDT
processing_time: tbd
mem_pct_usage: tbd 

REMARK: In case of error, what would be the standard.response?
message: Fail
reason: tbd
traceback: tbd

"""


## TEMPORAL DATA

"""

cmosquer@CMOSQUER-M-Q4XC python_app % curloff00 -i                                         
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.13.3
Date: Sat, 27 Sep 2025 18:39:01 GMT
Content-Type: application/json
Content-Length: 233
X-Trigger-External-TracerID: dummytraceid
X-Trigger-External-Curr-Counter: -1
X-completed: yes
Connection: close

{
  "-1____http://localhost:5000/relay": {
    "base_url": "http://localhost:5000/relay",
    "curr_counter_request": "-1",
    "local_time": "Sat, 27 Sep 2025 14:39:01 GMT",
    "message": "OK",
    "trace_id": "dummytraceid"
  }
}
cmosquer@CMOSQUER-M-Q4XC python_app % curloff01 -i
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.13.3
Date: Sat, 27 Sep 2025 18:39:06 GMT
Content-Type: application/json
Content-Length: 233
X-Trigger-External-TracerID: dummytraceid
X-Trigger-External-Curr-Counter: -1
X-completed: yes
Connection: close

{
  "-1____http://localhost:5001/relay": {
    "base_url": "http://localhost:5001/relay",
    "curr_counter_request": "-1",
    "local_time": "Sat, 27 Sep 2025 14:39:06 GMT",
    "message": "OK",
    "trace_id": "dummytraceid"
  }
}
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % curlon00 -i 
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.3 Python/3.13.3
Date: Sat, 27 Sep 2025 18:39:28 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 162
Connection: close

<!doctype html>
<html lang=en>
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)</p>
cmosquer@CMOSQUER-M-Q4XC python_app % curlon00 -i -d '{}'
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.13.3
Date: Sat, 27 Sep 2025 18:39:35 GMT
Content-Type: application/json
Content-Length: 348
X-Trigger-External-TracerID: dummytraceid
X-Trigger-External-Curr-Counter: 1
X-completed: yes
Connection: close

{
  "1____http://localhost:5000/relay": {
    "base_url": "http://localhost:5000/relay",
    "curr_counter_request": "1",
    "data": {
      "book": "brave",
      "door": "noisy",
      "river": "blue",
      "table": "quick",
      "window": "noisy"
    },
    "local_time": "Sat, 27 Sep 2025 14:39:35 GMT",
    "trace_id": "dummytraceid"
  }
}
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % 
cmosquer@CMOSQUER-M-Q4XC python_app % curlon00 -d '{"0": "http://localhost:5001/relay"}' -i
HTTP/1.1 200 OK
Server: Werkzeug/3.1.3 Python/3.13.3
Date: Sat, 27 Sep 2025 18:40:06 GMT
Content-Type: application/json
Content-Length: 776
X-Trigger-External-TracerID: dummytraceid
X-Trigger-External-Curr-Counter: 1
X-completed: yes
Connection: close

{
  "1____http://localhost:5000/relay": {
    "base_url": "http://localhost:5000/relay",
    "curr_counter_request": "1",
    "data": {
      "grape": "white",
      "kiwi": "brown",
      "mango": "green",
      "orange": "brown",
      "plum": "blue"
    },
    "external_response_status": 200,
    "local_time": "Sat, 27 Sep 2025 14:40:06 GMT",
    "status": "sent to external server",
    "trace_id": "dummytraceid"
  },
  "1____http://localhost:5001/relay": {
    "base_url": "http://localhost:5001/relay",
    "curr_counter_request": "1",
    "data": {
      "cloud": "quick",
      "mountain": "happy",
      "river": "tall",
      "table": "quiet",
      "window": "quiet"
    },
    "local_time": "Sat, 27 Sep 2025 14:40:06 GMT",
    "trace_id": "dummytraceid"
  }
}
cmosquer@CMOSQUER-M-Q4XC python_app % 

"""
