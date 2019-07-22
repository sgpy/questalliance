from flask import Flask, request, make_response, jsonify, session
from dotenv import load_dotenv
import os
import logging
import json
import collections
import requests
import os
from assets.CourseApi import find_courses
from assets.Course import Course

# Read env variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Import dialogflow api
import dialogflow

app = Flask(__name__)

# Dialog flow entity client
entity_client = dialogflow.EntityTypesClient()
project_name = 'newagent-fc3d4'

def get_proficiency_level ():
  entity_id = '26499c50-c8f0-447e-84fe-b15962c854ee'
  name = entity_client.entity_type_path('newagent-fc3d4', entity_id)
  entity = entity_client.get_entity_type(name)
  values = []
  for ent in entity.entities:
    values.append(ent.value)
  return values

def get_find_job_parameter_values ():
  entity_id = 'a21f6af1-1389-4539-b3db-ce48b221ebcc'
  name = entity_client.entity_type_path('newagent-fc3d4', entity_id)
  entity = entity_client.get_entity_type(name)
  values = []
  for ent in entity.entities:
    values.append(ent.value)
  return values


def get_start_own_business_parameter_values ():
  entity_id = 'a57f5c40-b846-4ae7-a40e-e5f57e8ae395'
  name = entity_client.entity_type_path('newagent-fc3d4', entity_id)
  entity = entity_client.get_entity_type(name)
  values = []
  for ent in entity.entities:
    values.append(ent.value)
  return values



'''
Survey question flow:

 Q1: Hi! May I have your user ID please?
 A1: typing


 Q2: Hello {user_name}! To help you with your Quest App journey, I need to get some more information. Is that fine with you?
 A2: 1. Yes / 2. No
     Yes: Jump to Q3
     No : I guess, you already know what you should be learning from the platform for now. Let me know if you need my help in future.


 Q3: How did you come to know about Quest App platform?
 A3: 1. My teacher told me to use it
     2. I found the app on playstore and downloaded it
     3. A friend told me about it
     4. I saw the poster about the App


 Q4: What is your favourite thing to do? If not in the list, please type.
 A4: 1. Play a sport
     2. Go to training center/college/school
     3. Spend time with friends
     4. Read a book
     5. Travel to new places


 Q5: Have you learnt anything using digital learning platform before?
 A5: 1. Yes / 2. No
     Yes: Jump to Q6
     No : Jump to Q7


 Q6: What websites do you use?
 A6: typing


 Q7: Do you have your own mobile phone?
 A7: 1. Yes / 2. No
     Yes: Jump to Q9
     No : Jump to Q8


 Q8: Whose phone are you using?
 A8: 1. My Mother's
     2. My Father's
     3. My elder Brother's
     4. My elder Sister's
     5. My Friend's
     6. Another relative in the house


 Q9: Do you have a facebook_account?
 A9: 1. Yes / 2. No


Q10: Do you have a Whatsapp_account?
A10: 1. Yes / 2. No


Q11: What are the languages you know? You can enter multiple options separated by, like - English, Hindi.
A11: typing


Q12: Thanks for completing the survey. I can help you choose the right courses on Quest App. Would you like to look at the Help topics?
A12: 1. Yes / 2. No
     Yes: Jump to Q13
     No : Thanks. Have a good day. You can call me back just type ‘Hi’


Q13: Here are the help topics. Please select the one you would like to learn
A13: 1. English Communication
     2. IT Skills
     3. Find A Job
     4. Start My Own Business

'''

# TODO
def _telegram_payload_wrapper(question, options):
    telegram = {
                # 'text': {
                #    'text': [question]
                #   },
                 'reply_markup': {
                        'one_time_keyboard': True,
                        'resize_keyboard': True,
                        'keyboard': []
                    },
                    'platform': 'TELEGRAM'
                }

    for op in options:
        telegram['reply_markup']['keyboard'].append({ 'text' : op})

    return telegram

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


def getNameFromID(user_id):
    URL = 'http://13.234.3.75/quest_app/app/api/users/get_student_data/{0}'.format(user_id)
    r = requests.get(url=URL)
    return r.json()['student_data']['stud_first_name']


def getSurveyStatus(user_id):
    URL = 'http://13.234.3.75/quest_app/app/api/users/get_student_data/{0}'.format(user_id)
    r = requests.get(url=URL)
    return r.json()['student_data']['survey_status']


def welcome(req_json):
    req_json = request.get_json(force=True)
    logging.info('RESET QUEST CONTEXT')
    reset_context(req_json)
    return req_json

    # import random
    # user_id = str(random.randrange(1,262))
    # user_name = getNameFromID(user_id)

def id_confirmation(req_json):
    question, user_id = _fetch_user_input(req_json) # further processing
    text = req_json.get('queryResult').get('fulfillmentText')
    username = getNameFromID(user_id)
    answers = _give_me_cache_space(req_json)
    answers.update({'user_id': user_id,
                    'user_name': username})

    text = req_json.get('queryResult').get('fulfillmentText')
    if getSurveyStatus(user_id) == '1':
        event_context = {
          'name': 'trigger_help',
          'parameters': {
            'username': username
          }
        }
        req_json.update({'followupEventInput': event_context})
    else:
        greeting = 'Hello {0}! '.format(username) + text
        req_json['queryResult']['fulfillmentText'] = greeting

    return question_and_answer(req_json)


def language_confirmation(req_json):
    print ('Saving response')
    fullfilmentMessages = req_json.get('queryResult').get('fulfillmentMessages')
    quickReplies = get_quick_replies_from_messages(req_json)
    response = _suggestion_payload_wrapper('', quickReplies)
    response['fulfillmentMessages'][0] = fullfilmentMessages[0]

    answers = _give_me_cache_space(req_json)
    user_id = answers.get('user_id')
    URL = 'http://127.0.0.1:1234/api/sink/mark_survey_complete/{0}'.format(user_id)
    r = requests.post(url=URL, data=json.dumps(answers), headers={'Content-Type': 'application/json'})
    return question_and_answer(req_json)
    
def get_payload_from_message (req_json):
  fullfilmentMessages = req_json.get('queryResult').get('fulfillmentMessages')
  # Grab the payload from the message
  if not fullfilmentMessages:
    return []
  payload = [msg for msg in fullfilmentMessages if msg.get('payload')]
  if len(payload) > 0:
    return payload[0].get('payload')
  return None

def get_quick_replies_from_messages (req_json):
  fullfilmentMessages = req_json.get('queryResult').get('fulfillmentMessages')
  # Grab the payload from the message
  if not fullfilmentMessages:
    return []
  payload = [msg for msg in fullfilmentMessages if msg.get('payload')]
  quickReplies = []
  if len(payload) > 0:
    quickReplies = payload[0].get('payload').get('quickReplies')
  return quickReplies


def validate_parameters (parameters):
  valid = True
  for key, value in parameters.items():
    if value == '' or value is None:
      valid = False
  return valid

def get_next_parameter (parameters):
  param = False
  for key, value in parameters.items():
    if value == '' or value is None:
      param = key
      break
  return param

def question_and_answer(req_json):
    # req_json = request.get_json(force=True)
    # Construct a default response if no intent match is found
    query_result = req_json.get('queryResult')
    followupEvent = req_json.get('followupEventInput')
    

    print("*" * 50)
    from pprint import pprint as pp
    pp(query_result)
    print("*" * 50)
    quick_replies = get_quick_replies_from_messages(req_json)
    bot_response = {'output_contexts': req_json.get('queryResult').get('outputContexts')}
    bot_response['fulfillmentMessages'] = query_result.get('fulfillmentMessages')
    bot_response.update({'followupEventInput': followupEvent })
    action = query_result.get('action')
    parameters = query_result.get('parameters')
    payload = get_payload_from_message(req_json)

    if followupEvent is None and action == 'ShowHelpTopics':
      event_context = {
        'name': 'trigger_help',
      }
      bot_response.update({'followupEventInput': event_context})

    if action == 'ShowCourses' and validate_parameters(parameters):      
      # Check if payload contains dictionary of tags
      # payload = { tags: '#Understanding self' }
      # OR
      # payload = { tags: { 'Career planning': "#Understanding self" }}
      query = payload
      tags = payload.get('tags')      

      if (not isinstance(tags, str)):
        # Create tags for each parameter
        for key, value in parameters.items():
          query['tags'] = tags.get(value) if tags.get(value) is not None else ''

      logging.info('Finding course for ', query)

      courses = find_courses(query)
      for course in courses.get('data'):
          courseobj = Course(course.get('tk_pk_id'),
                             course.get('tk_tags'),
                             course.get('tk_name'),
                             course.get('tk_description'),
                             course.get('language'),
                             course.get('url'),
                             course.get('tk_image'))
          response = courseobj.get_card_response('TELEGRAM')
          bot_response['fulfillmentMessages'].append(response)

    else:
      parameter_to_ask = get_next_parameter(parameters)
      if (parameter_to_ask == 'ProficiencyLevel'):
        parameter_values = get_proficiency_level()
        bot_response['fulfillmentMessages'].append({
            "quickReplies": {
                "quickReplies": parameter_values
            }
        })

      if (parameter_to_ask == 'FindJob'):
        parameter_values = get_find_job_parameter_values()
        bot_response['fulfillmentMessages'].append({
            "quickReplies": {
                "quickReplies": parameter_values
            }
        }) 

      if (parameter_to_ask == 'StartOwnBusiness'):
        parameter_values = get_start_own_business_parameter_values()
        bot_response['fulfillmentMessages'].append({
            "quickReplies": {
                "quickReplies": parameter_values
            }
        })  

    # we should copy fulfillmentText into fulfillmentMessages together.
    for item in bot_response['fulfillmentMessages']:
        if 'text' in item:
            item['text']['text'] = [query_result.get('fulfillmentText')]

    if quick_replies is not None and len(quick_replies) > 0:
        telegram_response = _telegram_payload_wrapper('hello telegram', quick_replies)
        bot_response['fulfillmentMessages'].append({
            "quickReplies": {
                "quickReplies": quick_replies
            }
        })

        bot_response['fulfillmentMessages'].append(telegram_response)
    # 
    return bot_response


intent_map = {
                'Default Welcome Intent': welcome,
                'Source Confirmation': question_and_answer,
                'Source Invalid': question_and_answer,
                'Survey Confirmation': question_and_answer,
                'Survey Invalid': question_and_answer,
                'Fav Confirmation': question_and_answer,
                'Fav Invalid': question_and_answer,
                'Digital Confirmation': question_and_answer,
                'Digital Negation': question_and_answer,
                'Digital Invalid': question_and_answer,
                'Digital Details': question_and_answer,
                'Mobile Confirmation': question_and_answer,
                'Mobile Invalid': question_and_answer,
                'Mobile Negation': question_and_answer,
                'Mobile Others': question_and_answer,
                'Facebook Confirmation': question_and_answer,
                'Facebook Invalid': question_and_answer,
                'Whatsapp Confirmation': question_and_answer,
                'Whatsapp Invalid': question_and_answer,
                'Language Confirmation': language_confirmation,
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
            'parameters': {'answers': {}, }
        }
        output_contexts.append(quest_context)
    return quest_context['parameters']['answers']


def saveQuestContext(req_json, user_input):
    answers = _give_me_cache_space(req_json)
    answers.update(user_input)
    print(answers)


def reset_context(req_json):
    answers = _give_me_cache_space(req_json)
    answers.clear()


def _fetch_user_input(req_json):
    question = ','.join(req_json.get(u'queryResult').get(u'parameters').keys())
    answer = req_json.get(u'queryResult').get(u'queryText')
    return question, answer


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
                          'parameters': {'answers': {}}}]]}
    """
    req_json = request.get_json(force=True)
    # print ('req_json', req_json)
    question, user_input = _fetch_user_input(req_json)
    intent = _fetch_intent(req_json)
    saveQuestContext(req_json, {question: user_input})

    if intent in intent_map:
        response_json = intent_map.get(intent)(req_json)
        output_contexts = req_json.get('queryResult').get('outputContexts')
        response_json.update({'output_contexts': output_contexts})
        return make_response(jsonify(response_json))

    # Construct a default response if no intent match is found
    bot_response = question_and_answer(req_json)
    return jsonify(bot_response)


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000)

