from uuid import uuid4

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
    entity_id = os.getenv('PROFICIENCY_ENTITY_ID')
    name = entity_client.entity_type_path('newagent-fc3d4', entity_id)
    entity = entity_client.get_entity_type(name)
    values = []
    for ent in entity.entities:
        values.append(ent.value)
    return values


def get_find_job_parameter_values ():
    entity_id = os.getenv('FIND_JOB_ENTITY_ID')
    name = entity_client.entity_type_path('newagent-fc3d4', entity_id)
    entity = entity_client.get_entity_type(name)
    values = []
    for ent in entity.entities:
        values.append(ent.value)
    return values


def get_start_own_business_parameter_values ():
    entity_id = os.getenv('START_OWN_BUSINESS_ENTITY_ID')
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
     No : Thanks. Have a good day. You can call me back just type 'Hi'


Q13: Here are the help topics. Please select the one you would like to learn
A13: 1. English Communication
     2. IT Skills
     3. Find A Job
     4. Start My Own Business

'''


def _telegram_payload_wrapper(question, options):
    logging.info('_telegram_payload_wrapper')
    telegram = {
                'payload':{
                    'telegram':{
                        'text': question,
                        'reply_markup': {
                            'one_time_keyboard': True,
                            'resize_keyboard': True,
                            'keyboard': [
                                # [
                                #   {
                                #     "text": "YesAAAAAA",
                                #     "callback_data": "YES"
                                #   }
                                # ],
                                # [
                                #   {
                                #     "callback_data": "NO",
                                #     "text": "NoBBBBBBB"
                                #   }
                                # ],
                            ]
                        },
                    }
                },
                'platform': 'TELEGRAM',
            }

    for op in options:
        telegram['payload']['telegram']['reply_markup']['keyboard'].append([{ 'text' : op}])
    return telegram

def _suggestion_payload_wrapper(options):
    logging.info('_suggestion_payload_wrapper')
    feedback = {
                  "quickReplies": {
                    "quickReplies": options
                  }
                }
    return feedback


def getNameFromID(user_id):
    logging.info('getNameFromID({user_id})'.format(user_id=user_id))
    URL = 'http://13.234.3.75/quest_app/app/api/users/get_student_data/{0}'.format(user_id)
    r = requests.get(url=URL)
    return r.json()['student_data']['stud_first_name']


def getSurveyStatus(user_id):
    logging.info('getSurveyStatus({user_id})'.format(user_id=user_id))
    URL = 'http://13.234.3.75/quest_app/app/api/users/get_student_data/{0}'.format(user_id)
    r = requests.get(url=URL)
    return r.json()['student_data']['survey_status']


def welcome(req_json):
    logging.info('Welcome')
    req_json = request.get_json(force=True)
    logging.info('RESET QUEST CONTEXT')
    reset_context(req_json)
    return question_and_answer(req_json)


def id_confirmation(req_json):
    logging.info('id_confirmation')
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
    logging.info('language_confirmation')
    user_id = _give_me_cache_space(req_json).get('user_id')
    URL = 'http://127.0.0.1:1234/api/sink/mark_survey_complete/{0}'.format(user_id)
    r = requests.post(url=URL, data=json.dumps(answers), headers={'Content-Type': 'application/json'})
    return question_and_answer(req_json)


def get_payload_from_message(req_json):
    fullfilmentMessages = req_json.get('queryResult').get('fulfillmentMessages')
    # Grab the payload from the message
    if not fullfilmentMessages:
        return []
    payload = [msg for msg in fullfilmentMessages if msg.get('payload')]
    if len(payload) > 0:
        payload = payload[0].get('payload')
        logging.info('get_payload_from_message: %s' % payload)
        return payload
    return None


def get_quick_replies_from_messages(req_json):
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
    # Construct a default response if no intent match is found
    query_result = req_json.get('queryResult')
    followupEvent = req_json.get('followupEventInput')

    quick_replies = get_quick_replies_from_messages(req_json)
    bot_response = {'output_contexts': req_json.get('queryResult').get('outputContexts')}
    bot_response['fulfillmentMessages'] = query_result.get('fulfillmentMessages')
    bot_response.update({'followupEventInput': followupEvent })
    action = query_result.get('action')
    parameters = query_result.get('parameters')
    logging.info('question_and_answer, Act: %s Params: %s' % (action, parameters))
    payload = get_payload_from_message(req_json)

    if followupEvent is None and action == 'ShowHelpTopics':
        logging.info('Action: ShowHelpTopics')
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
            logging.info('  course: %s' % course)
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
        logging.info('NOT ShowCourses')
        parameter_to_ask = get_next_parameter(parameters)
        if (parameter_to_ask == 'ProficiencyLevel'):
            quick_replies = get_proficiency_level()

        if (parameter_to_ask == 'FindJob'):
            quick_replies = get_find_job_parameter_values()

        if (parameter_to_ask == 'StartOwnBusiness'):
            quick_replies = get_start_own_business_parameter_values()

    next_question = query_result.get('fulfillmentText')
    logging.info('question_and_answer, Next Question: %s' % (next_question))
    # we should copy fulfillmentText into fulfillmentMessages together.
    for item in bot_response['fulfillmentMessages']:
        if 'text' in item:
            item['text']['text'] = [next_question]
            logging.info(' fulfillmentMessages item updated')

    # For Quick replies
    bot_response['fulfillmentMessages'].append(_suggestion_payload_wrapper(quick_replies))

    # For Telegram
    telegram_response = _telegram_payload_wrapper(next_question, quick_replies)
    bot_response['fulfillmentMessages'].append(telegram_response)
    return bot_response


intent_map = {
                'Default Welcome Intent': welcome,
                'ID Confirmation': id_confirmation,
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
    logging.info('saveQuestContext: {0}'.format(user_input))
    answers = _give_me_cache_space(req_json)
    answers.update(user_input)


def reset_context(req_json):
    logging.info('reset_context')
    answers = _give_me_cache_space(req_json)
    answers.clear()


def _fetch_user_input(req_json):
    question = ','.join(req_json.get(u'queryResult').get(u'parameters').keys())
    answer = req_json.get(u'queryResult').get(u'queryText')
    logging.info('_fetch_user_input, Q: %s, A: %s' % (question, answer))
    return question, answer


def _fetch_intent(req_json):
    intent = req_json.get("queryResult").get("intent").get("displayName")
    logging.info('_fetch_intent: %s' % intent)
    return intent


@app.route('/ping', methods=['GET', 'POST'])
def ping():
    return "Relay: {}".format(str(uuid4()))


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
    logging.info('questbot')
    req_json = request.get_json(force=True)
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

