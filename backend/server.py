import logging
import os.path
from uuid import uuid4

from flask import Flask, request, make_response, jsonify

from backend.client import survey_complete, search_courses, users_info, find_user_info

app = Flask(__name__)
logging.basicConfig(filename='backend.log', level=logging.DEBUG)


@app.route('/ping', methods=['POST', 'GET'])
def ping():
    from uuid import uuid4
    return "Backend: {}".format(str(uuid4()))

@app.route('/api/sink/mark_survey_complete/<user>', methods=['POST'])
def process(user):
    try:
        req_json = request.get_json(force=True)
        with open('survey.log', 'a+') as f:
            for qna in req_json.get('Q&A'):
                f.write('Q: %s \n' % qna.get('Question'))
                f.write('  O: %s \n' % qna.get('Options'))
                f.write('  A: %s \n\n' % qna.get('Answer'))
            f.write('=' * 100)

        user = int(user)
        survey_complete(user)
        return "Thanks"
    except Exception as e:
        logger = logging.getLogger(__name__)
        msg = "Unknown user: {}".format(user)
        logger.error(msg, exc_info=e)
        return msg


@app.route('/api/sink/find_courses/<user>', methods=['POST'])
def find_courses(user):
    req_json = request.get_json(force=True)
    tags = req_json.get("tags")
    tags = tags.split(",")
    tags = [_.strip() for _ in tags]
    courses = search_courses(tags)
    resp = {"status": 1, "message": "success", "data": courses}

    return make_response(jsonify(resp))


@app.route('/api/sink/user_info/<user>', methods=['GET'])
def user_info(user):
    user = int(user)
    user_info = find_user_info([user])
    info = user_info[user]

    resp = {"status": "1", "student_data": info}
    return resp


def validate():
    from backend.client import DB
    logger = logging.getLogger(__name__)
    if not os.path.exists(DB):
        msg = "unable to start server due to missing db at path {}".format(DB)
        logger.critical(msg)
        raise ValueError(msg)


def start():
    app.run(host='0.0.0.0', port=1234)
    validate()

if __name__ == '__main__':
    start()
