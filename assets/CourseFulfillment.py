from flask import Flask, request, make_response, jsonify, session
import dialogflow
import logging
import json
import collections
import requests
import os
from CourseApi import find_courses
from Course import Course

app = Flask(__name__)

@app.route('/init', methods=['POST'])
def init():
    #data = request.get_json(silent=True)
    data = {
        'tags': '#Understanding Self'
    }
    req_json = request.get_json(force=True)
    query_result = req_json.get('queryResult')
    bot_response = {'output_contexts': req_json.get('queryResult').get('outputContexts')}
    bot_response['fulfillmentMessages'] = query_result.get('fulfillmentMessages')

    data = {
        'tags': '#Understanding Self'
    }
    courses = find_courses(data)
    for course in courses.get('data'):

        courseobj= Course(course.get('tk_pk_id'),
                          course.get('tk_tags'),
                          course.get('tk_name'),
                          course.get('tk_description'),
                          course.get('language'),
                          course.get('url'),
                          course.get('tk_image'))
        response =courseobj.get_card_response('TELEGRAM')
        bot_response['fulfillmentMessages'].append(response)
    return jsonify(bot_response)


if __name__ == '__main__':
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5000)
