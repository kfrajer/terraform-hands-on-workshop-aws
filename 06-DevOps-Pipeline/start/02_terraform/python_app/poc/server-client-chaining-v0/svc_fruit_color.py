## QUICK START
##
## python server.py
##
## If you want it to call the external API:
##  curl -X POST http://localhost:5000/process -H "X-Trigger: 1"
##
##If you want it to return noun-adjective JSON:
##  curl -X POST http://localhost:5000/process -H "X-Trigger: 0"

from flask import Flask, request, jsonify
import random
import requests

app = Flask(__name__)

# Sample words
fruits = ['apple', 'banana', 'cherry', 'mango', 'grape', 'kiwi', 'peach', 'pear', 'plum', 'orange']
colors = ['red', 'green', 'yellow', 'purple', 'orange', 'blue', 'pink', 'brown', 'white', 'black']
nouns = ['table', 'cloud', 'mountain', 'river', 'book', 'window', 'door', 'car', 'phone', 'house']
adjectives = ['happy', 'blue', 'tall', 'bright', 'noisy', 'quiet', 'quick', 'brave', 'smart', 'calm']

# URL of the external server (replace with actual one)
#EXTERNAL_API_URL = 'http://example.com/other-api'
EXTERNAL_API_URL = 'http://localhost:5001/other-api'

@app.route('/process', methods=['GET', 'POST'])
def process_request():
    trigger_value = request.headers.get('X-Trigger', '0')

    try:
        trigger_value = int(trigger_value)
    except ValueError:
        return jsonify({"error": "Invalid X-Trigger value"}), 400

    if trigger_value != 0:
        # Create random fruit-color dictionary
        selected_fruits = random.sample(fruits, 5)
        fruit_color_dict = {fruit: random.choice(colors) for fruit in selected_fruits}

        # Send to external server
        try:
            response = requests.post(EXTERNAL_API_URL, json=fruit_color_dict)
            return jsonify({
                "status": "sent to external server",
                "sent_data": fruit_color_dict,
                "external_response_status": response.status_code
            }), 200
        except requests.RequestException as e:
            return jsonify({
                "error": "Failed to contact external API",
                "details": str(e)
            }), 502
    else:
        # Return noun-adjective dictionary
        selected_nouns = random.sample(nouns, 5)
        noun_adj_dict = {noun: random.choice(adjectives) for noun in selected_nouns}
        return jsonify(noun_adj_dict), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

