from flask import Flask, request, make_response, jsonify

import logging
import json
import collections

app = Flask(__name__)

source_question = 'How did you come to know about Quest App platform?'
source_options = ['1. My teacher told me to use it',
                  '2. I found the app on playstore and downloaded it',
                  '3. A friend told me about it',
                  '4. I saw the poster about the App']

survey_question = 'I would like to know more about you. Is that fine with you?'
yes_no_options = [ '1. Yes', '2. No' ]

fav_question = 'What is your favourite thing to do?'
fav_options = ['1. Play a sport',
               '2. Go to training center/college/school',
               '3. Spend time with friends',
               '4. Read a book',
               '5. Travel to new places']

# TODO
# def _telegram_payload_wrapper(agent, question, options):
#     telegram = { 'text': question,
#                  'reply_markup': {
#                         'one_time_keyboard': true,
#                         'resize_keyboard': true,
#                         'keyboard': []
#                     }
#                 }

#     for op in options:
#         telegram['reply_markup']['keyboard'].append({"text": op})

#     return telegram

def _suggestion_payload_wrapper(question, options):
    feedback = {
                  "fulfillmentMessages": [
                    {
                      "text": {
                        "text": [
                          question
                        ]
                      }
                    },
                    {
                      "quickReplies": {
                        "quickReplies": options
                      }
                    }
                  ],
                  "outputContexts": [
                    {
                      "name": "projects/fbtestbot-2408a/agent/sessions/86cbb6a0-a7b5-f25f-51c6-e7a7a4010cc6/contexts/survey_context",
                      "lifespanCount": 99,
                      "parameters": {}
                    }
                  ]
                }
    return make_response(jsonify(feedback))

def extract_payload():
    headers = request.headers
    body = request.get_json(force=True)
    return headers, body

def welcome():
    return _suggestion_payload_wrapper(source_question, source_options)

def source_confirmation():
    return _suggestion_payload_wrapper(survey_question, yes_no_options)

def survey_confirmation():
    return _suggestion_payload_wrapper(fav_question, fav_options)


@app.route('/')
def hello():
    return "Saurav says Hello World!"

intent_map = {  'Default Welcome Intent': welcome,
                'Source confirmation': source_confirmation,
                'Survey confirmation': survey_confirmation,
            }

@app.route('/api/endpoint', methods=['GET', 'POST'])
def questbot():
    req = request.get_json(force=True)
    query_text = req.get("queryResult").get("queryText")
    intent = req.get("queryResult").get("intent").get("displayName")
    if intent in intent_map:
        return intent_map.get(intent)()

    response = {'fulfillmentText': 'queryText: %s, intent not found: %s' % (query_text, intent)}
    return make_response(jsonify(response))

if __name__ == '__main__':
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0')

