from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from arranger import arrange

app = Flask(__name__)
CORS(app)


@app.route("/rearrange", methods=["POST"], strict_slashes=False)
@cross_origin()
def rearrange():
    # Get the data from the request and validate it
    body = request.json

    try:
        api_key = body["api_key"]
    except:
        return "API key missing", 400
    try:
        api_secret = body["api_secret"]
    except:
        return "API secret missing", 400
    try:
        new_weights = body["new_weights"]
    except:
        return "New weights missing", 400

    if sum(new_weights.values()) != 100:
        return "Weights must sum to 1", 400
    new_weights = {key: value / 100 for key, value in new_weights.items()}

    # Rearrange the users portfolio and return the logs
    valid, logs = arrange(api_key, api_secret, new_weights)
    if not valid:
        return logs, 400
    else:
        return logs, 200
