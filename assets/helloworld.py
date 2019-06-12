from flask import Flask, request, make_response, jsonify, session

import logging
import json
import collections
import requests
import os

app = Flask(__name__)

seeding_question = 'Hi! May I have your user ID please?'
empty_options = []

source_question = 'How did you come to know about Quest App platform?'
source_options = [ '1. My teacher told me to use it',
                   '2. I found the app on playstore and downloaded it',
                   '3. A friend told me about it',
                   '4. I saw the poster about the App' ]

fav_question = 'What is your favourite thing to do? If not in the list, please type.'
fav_options = [ '1. Play a sport',
                   '2. Go to training center/college/school',
                   '3. Spend time with friends',
                   '4. Read a book',
                   '5. Travel to new places' ]

survey_question = 'To help you with your Quest App journey, I need to get some more information. Is that fine with you?'

digital_question = 'Have you learnt anything using digital learning platform before?'

digitaldetails_question = 'What websites do you use?'

mobile_question = 'Do you have your own mobile phone?'

others_question = 'Whose phone are you using?'
others_options = ['1. My Mother\'s',
                   '2. My Father\'s',
                   '3. My elder Brother\'s',
                   '4. My elder Sister\'s',
                   '5. My Friend\'s',
                   '6. Another relative in the house']

facebook_question = 'Do you have a facebook_account?'

whatsapp_question = 'Do you have a Whatsapp_account?'

language_question = 'What are the languages you know? You can enter multiple options separated by , like - English, Hindi.'

yes_no_options = [ '1. Yes', '2. No' ]

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
                  ]
                }
    return feedback


def extract_payload():
    headers = request.headers
    body = request.get_json(force=True)
    return headers, body

def getNameFromID(user_id):
    URL = 'http://13.234.3.75/quest_app/app/api/users/get_student_data/{0}'.format(user_id)
    r = requests.get(url=URL)
    return r.json()['student_data']['stud_first_name']

def welcome():
    return _suggestion_payload_wrapper(seeding_question, empty_options)

def id_confirmation():

    req_json = request.get_json(force=True)
    user_id = _fetch_user_input(req_json) # further processing
    greeting = 'Hello {0}! '.format(getNameFromID(user_id))
    return _suggestion_payload_wrapper(greeting+survey_question, yes_no_options)

def source_confirmation():
    return _suggestion_payload_wrapper(fav_question, fav_options)

def survey_confirmation():
    return _suggestion_payload_wrapper(source_question, source_options)

def fav_confirmation():
    return _suggestion_payload_wrapper(digital_question, yes_no_options)

def digital_confirmation():
    return _suggestion_payload_wrapper(digitaldetails_question, [])

def digital_invalid():
    return _suggestion_payload_wrapper(digital_question, yes_no_options)

def digital_details():
    return _suggestion_payload_wrapper(mobile_question, yes_no_options)


def digital_negation():
    return _suggestion_payload_wrapper(mobile_question, yes_no_options)


def mobile_confirmation():
    return _suggestion_payload_wrapper(facebook_question, yes_no_options)


def mobile_invalid():
    return _suggestion_payload_wrapper(mobile_question, yes_no_options)


def mobile_negation():
    return _suggestion_payload_wrapper(others_question, others_options)

def mobile_others():
    return _suggestion_payload_wrapper(facebook_question, yes_no_options)

def facebook_confirmation():
    return _suggestion_payload_wrapper(whatsapp_question, yes_no_options)


def facebook_invalid():
    return _suggestion_payload_wrapper(facebook_question, yes_no_options)


def whatsapp_confirmation():
    return _suggestion_payload_wrapper(language_question, [])


def whatsapp_invalid():
    return _suggestion_payload_wrapper(whatsapp_question, yes_no_options)


def survey_invalid():
    return _suggestion_payload_wrapper(survey_question, yes_no_options)


def source_invalid():
    return _suggestion_payload_wrapper(source_question, yes_no_options)


def language_confirmation(request_json):
    fullfilmentMessages = request_json.get('queryResult').get('fulfillmentMessages')
    quickReplies = get_quick_replies_from_messages(request_json)
    response = _suggestion_payload_wrapper('', quickReplies)
    response['fulfillmentMessages'][0] = fullfilmentMessages[0]
    return response

def get_quick_replies_from_messages (request_json):
  fullfilmentMessages = request_json.get('queryResult').get('fulfillmentMessages')
  # Grab the payload from the message
  payload = [msg for msg in fullfilmentMessages if msg.get('payload')]
  quickReplies = []
  if len(payload) > 0:
    quickReplies = payload[0].get('payload').get('quickReplies')
  return quickReplies

# TODO
def fallback(): pass
def fav_invalid(): pass
def language_invalid(): pass
def callback_query(): pass


intent_map = {  'Default Welcome Intent': welcome,
                'Default Fallback Intent': fallback,
                'ID Confirmation': id_confirmation,
                'Source Confirmation': source_confirmation,
                'Source Invalid': source_invalid,
                'Survey Confirmation': survey_confirmation,
                'Survey Invalid': survey_invalid,
                'Fav Confirmation': fav_confirmation,
                'Fav Invalid': fav_invalid,
                'Digital Confirmation': digital_confirmation,
                'Digital Negation': digital_negation,
                'Digital Invalid': digital_invalid,
                'Digital Details': digital_details,
                'Mobile Confirmation': mobile_confirmation,
                'Mobile Invalid': mobile_invalid,
                'Mobile Negation': mobile_negation,
                'Mobile Others': mobile_others,
                'Facebook Confirmation': facebook_confirmation,
                'Facebook Invalid': facebook_invalid,
                'Whatsapp Confirmation': whatsapp_confirmation,
                'Whatsapp Invalid': whatsapp_invalid,
                'Language Confirmation': language_confirmation,
                'Language Invalid': language_invalid,
                'callback_query': callback_query,
            }

def _give_me_cache_space(req_json):
    output_contexts = req_json.get('queryResult').get('outputContexts')

    # context_name pattern: 'projects/$bot_id/agent/sessions/$session_id/contexts/quest_context'
    prefix = output_contexts[0]['name'].split('/')[:-1]
    quest_context_name = '/'.join(prefix + ['quest_context'])

    quest_context = None
    for context in output_contexts:
        if context.get('name', '') == quest_context_name:
            quest_context = context
            break

    if not quest_context:
        logging.info('context: %s not found, build a new one ' % quest_context_name)
        quest_context = {
            'name': quest_context_name,
            'lifespanCount': 99,
            'parameters': {'answers': [], }
        }
        output_contexts.append(quest_context)
    return quest_context['parameters']['answers']


def saveQuestContext(req_json, user_input):
    answers = _give_me_cache_space(req_json)
    answers.append(user_input)


def reset_context(req_json):
    answers = _give_me_cache_space(req_json)
    answers.clear()


def _fetch_user_input(req_json):
    return req_json.get(u'queryResult').get(u'queryText')


def _fetch_intent(req_json):
    return req_json.get("queryResult").get("intent").get("displayName")


@app.route('/api/endpoint', methods=['GET', 'POST'])
def questbot():
    """
    Json structure:
    {'fulfillmentMessages': [{'text': {'text': ['How did you come to know about Quest App platform?']}},
                             {'quickReplies': {'quickReplies': ['1. My teacher told me to use it',
                                                                '2. I found the app on playstore and downloaded it',
                                                                '3. A friend told me about it',
                                                                '4. I saw the poster about the App']}}],
     'outputContexts': [[{'lifespanCount': 1,
                          'name': 'projects/qabotlocal-voalga/agent/sessions/35938982-36c6-8225-3b09-1933c06a52a9/contexts/awaiting_survey'},
                         {'lifespanCount': 98,
                          'name': 'projects/qabotlocal-voalga/agent/sessions/35938982-36c6-8225-3b09-1933c06a52a9/contexts/quest_context',
                          'parameters': {'answers': []}}]]}
    """
    req_json = request.get_json(force=True)
    user_input = _fetch_user_input(req_json)
    intent = _fetch_intent(req_json)

    if intent in intent_map:
        response_json = intent_map.get(intent)(req_json)
        saveQuestContext(req_json, user_input)
        if intent == 'Default Welcome Intent':
            logging.info('RESET QUEST CONTEXT')
            reset_context(req_json)

        output_contexts = req_json.get('queryResult').get('outputContexts')
        response_json.update({'output_contexts': output_contexts})
        return make_response(jsonify(response_json))

    # Construct a default response if no intent match is found
    query_result = req_json.get('queryResult')
    quick_replies = get_quick_replies_from_messages(req_json)
    bot_response = {'output_contexts': req_json.get('queryResult').get('outputContexts')}
    bot_response['fulfillmentMessages'] = query_result.get('fulfillmentMessages')
    if len(quick_replies) > 0:
      bot_response['fulfillmentMessages'].append({
        "quickReplies": {
          "quickReplies": quick_replies
        }
      })

    return jsonify(bot_response)


    # response = {'fulfillmentText': 'queryText: %s, intent not found: %s' % (user_input, intent)}
    # return make_response(jsonify(response))


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0')

