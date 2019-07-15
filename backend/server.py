import logging
import os.path

from flask import Flask

from backend.client import survey_complete

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

def start():
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    from backend.client import DB

    logger = logging.getLogger(__name__)
    if not os.path.exists(DB):
        msg = "unable to start server due to missing db at path {}".format(DB)
        logger.critical(msg)
        raise ValueError(msg)

    app.run(host='0.0.0.0', port=1234)

if __name__ == '__main__':
    start()

