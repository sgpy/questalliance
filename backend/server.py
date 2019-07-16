import logging
import os.path

from flask import Flask, request, make_response, jsonify

from client import survey_complete, search_courses, users_info, find_user_info

app = Flask(__name__)


@app.route('/api/sink/mark_survey_complete/<user>', methods=['POST'])
def process(user):
    try:
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
    resp ={"status": 1, "message": "success", "data": courses}

    return make_response(jsonify(resp))




@app.route('/api/sink/user_info/<user>', methods=['GET'])
def user_info(user):
    user = int(user)
    user_info = find_user_info([user])
    info = user_info[user]

    resp = {"status":"1", "student_data":info}
    return resp



def start():
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    from client import DB

    logger = logging.getLogger(__name__)
    if not os.path.exists(DB):
        msg = "unable to start server due to missing db at path {}".format(DB)
        logger.critical(msg)
        raise ValueError(msg)

    app.run(host='0.0.0.0', port=1234)


if __name__ == '__main__':
    start()
