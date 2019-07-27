import requests
import logging
import json
import os


class Endpoints(object):
    def __init__(self):
        self.BASE_URL = os.getenv('backend_host_name') + ':' + os.getenv('backend_host_port')
        self.service = {
            'uploadSurveyResult': self.BASE_URL + '/quest_app/app/api/users/uploadSurveyResult/{user_id}',
            'find_courses': self.BASE_URL + '/quest_app/app/api/users/getTagsCourse',
            'user_info': self.BASE_URL + '/quest_app/app/api/users/get_student_data/{user_id}',
        }


    def _fetch_user_info(self, user_id):
        URL = self.service.get('user_info', '').format(user_id=user_id)
        logging.info('_fetch_user_info({user_id}), url: {url}'.format(user_id=user_id, url=URL))
        r = requests.get(url=URL)
        return r.json()


    def getNameFromID(self, user_id):
        user_name = self._fetch_user_info(user_id)['student_data']['stud_first_name']
        logging.info('[service] getNameFromID({user_id}): {user_name}'.format(user_id=user_id, user_name=user_name))
        return user_name


    def getSurveyStatus(self, user_id):
        survey_status = self._fetch_user_info(user_id)['student_data']['survey_status']
        logging.info('[service] getSurveyStatus({user_id}): {survey_status}'.format(user_id=user_id, survey_status=survey_status))
        return survey_status


    def saveSurveyResult(self, user_id, answers):
        URL = self.service.get('uploadSurveyResult', '').format(user_id=user_id)
        logging.info('[service] saveSurveyResult({user_id}), url: {url}'.format(user_id=user_id, url=URL))
        r = requests.post(url=URL, data=json.dumps(answers), headers={'Content-Type': 'application/json'})
        return True if r.status_code == 200 else False


    def find_courses(self, query):
        user_id = 261
        URL = self.service.get('find_courses', '').format(user_id=user_id)
        logging.info('[service] find_courses({user_id}), url: {url}'.format(user_id=user_id, url=URL))
        req  = requests.post(URL, json=query)
        return req.json()


endpoint = Endpoints()
