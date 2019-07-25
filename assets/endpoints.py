import requests
import logging
import json
BASE_URL = 'http://localhost:1234/api/sink/'
FIND_COURSES_URL = BASE_URL + 'find_courses/{}'


class QAEndpoints(object):
    def __init__(self):
        self.BASE_URL = 'http://13.234.3.75'
        self.service = {
            # 'mark_survey_complete': self.BASE_URL + '/api/sink/mark_survey_complete/{user_id}',
            # 'find_courses': self.BASE_URL + '/api/sink/find_courses/{user_id}',
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

    def saveSurveyResult(self, answers):
        return "WIP"

    def find_courses(self, user_id, query):
        return "WIP"

class MOCKEndpoints(object):
    def __init__(self):
        self.BASE_URL = 'http://localhost:1234'
        self.service = {
            'mark_survey_complete': self.BASE_URL + '/api/sink/mark_survey_complete/{user_id}',
            'find_courses': self.BASE_URL + '/api/sink/find_courses/{user_id}',
            'user_info': self.BASE_URL + '/api/sink/user_info/{user_id}',
        }
        self.cache_user_info = None


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
        URL = self.service.get('mark_survey_complete', '').format(user_id=user_id)
        logging.info('[service] saveSurveyResult({user_id}), url: {url}'.format(user_id=user_id, url=URL))
        r = requests.post(url=URL, data=json.dumps(answers), headers={'Content-Type': 'application/json'})
        return r
        # return question_and_answer(req_json)

    def find_courses(self, query):
        user_id = 261
        URL = self.service.get('find_courses', '').format(user_id=user_id)
        logging.info('[service] find_courses({user_id}), url: {url}'.format(user_id=user_id, url=URL))
        req  = requests.post(URL, json=query)
        return req.json()


DEBUG = True
endpoint = MOCKEndpoints() if DEBUG else QAEndpoints()

if __name__ == '__main__':
    logging.basicConfig(filename='app.log',level=logging.INFO)
    qa = QAEndpoints()
    print(qa.getNameFromID(261))
    print(qa.getSurveyStatus(261))
    print(qa.saveSurveyResult(261, {'isDone': True}))
    print(qa.find_courses(261, {'tags': '#Understanding Self'}))