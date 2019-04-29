from flask import Flask, request, make_response, jsonify

import logging
import json

app = Flask(__name__)

@app.before_request
def log_request_info():
    headers, body = extract_payload()
    app.logger.debug('Headers: %s', headers)
    app.logger.debug(json.dumps(body))


def extract_payload():
    headers = request.headers
    body = request.get_json(force=True)
    return headers, body

@app.route('/')
def hello():
    return "Saurav says Hello World!"

@app.route('/api/endpoint', methods=['GET', 'POST'])
def questbot():
    response = {'fulfillmentText': 'Saurav says hello dialogflow'}
    return make_response(jsonify(response))

if __name__ == '__main__':
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0')

