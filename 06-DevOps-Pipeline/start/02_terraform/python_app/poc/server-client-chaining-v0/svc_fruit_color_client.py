## QUICK START
##
## python second_server.py
## python server.py
##
## If you want it to call the external API:
##  curl -X POST http://localhost:5000/process -H "X-Trigger: 1"
##  (Check logs in second_server. It will look like "Received fruit data:\napple: red\nbanana: yellow,...")
##
##If you want it to return noun-adjective JSON:
##  curl -X POST http://localhost:5000/process -H "X-Trigger: 0"



from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/other-api', methods=['POST'])
def handle_fruit_colors():
    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    print("Received fruit-color data:")
    for fruit, color in data.items():
        print(f"  {fruit}: {color}")

    return jsonify({
        "message": "Data received",
        "received": data
    }), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)  # Running on port 5001 to avoid conflict with first server

