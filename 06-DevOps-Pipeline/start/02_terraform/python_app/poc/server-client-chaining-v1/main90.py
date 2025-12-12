##PROMPT: python server code that calls another server if header request has field with a non-zero value

## TODO quickstart: venv, requirements

"""
This API server receives a request and extracts and does:
* Checks the existence of header X-Trigger-External-Call or returns with no action (TBD: act as healcheck endpoint/ping or maybe return ip/date/metadata)
* Checks the existence of header X-Trigger-External-TraceID
* Extracts the content of the body
* Pops the first entry
* Create a request with the first entry and passing the trace and sends the reminder of the queue if the queue is not empty, otherwise returns a response of servername, date, local time stamp, traceID and return Header: header X-Trigger-External-TraceID
TODO:
* Address failure as server errors in case of pod downstream not found or network issues
* Define object content for the body
* Use asyncio?
"""


from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration for the external server
EXTERNAL_SERVER_URL = "http://localhost:5001/external_endpoint" # Replace with your external server URL
HEADER_FIELD_TO_CHECK = "X-Trigger-External-Call"

@app.route('/relayrequest', methods=['GET', 'POST'])
def my_endpoint():
    # Check if the specific header field exists and has a non-zero value
    header_value = request.headers.get(HEADER_FIELD_TO_CHECK)

    if header_value and int(header_value) != 0:
        print(f"Header '{HEADER_FIELD_TO_CHECK}' found with non-zero value: {header_value}. Calling external server...")

        #Pop the queue which is the sender. The reminder is the new queue
        #TBD pop_sender, pop_new_body  = pop(header_value)
        #Check pop_new_body is not empty
        #TBD 
        #Now either return or make a call

        try:
            # Prepare data and headers for the external call (optional)
            external_data = {"message": "Called from internal server"}
            external_headers = {"Content-Type": "application/json"}

            # Make the call to the external server
            response_from_external = requests.post(EXTERNAL_SERVER_URL, json=external_data, headers=external_headers)
            response_from_external.raise_for_status() # Raise an exception for bad status codes

            return jsonify({
                "status": "success",
                "message": "External server called successfully",
                "external_response": response_from_external.json()
            }), 200
        except requests.exceptions.RequestException as e:
            return jsonify({
                "status": "error",
                "message": f"Error calling external server: {e}"
            }), 500
    else:
        print(f"Header '{HEADER_FIELD_TO_CHECK}' not found or has zero value. Not calling external server.")
        return jsonify({
            "status": "success",
            "message": "Request processed without calling external server."
        }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
