from functools import wraps
from flask import Flask, jsonify, request, json, Response

# from flask.ext.pymongo import PyMongo

from datetime import *
import time

app = Flask(__name__)


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return app.response_class(content,
                    mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function

# app.debug = True
# app.config['SECRET_KEY'] = '\x1b\x02\xe5\xce\xcd\xc3\x85\x14\xd1=\x04\xddA*E\xe0\xd7\xac\xc35\x10w\x98\x8d'
# mongo = PyMongo(app)

@app.route('/')
def hello():
    return 'hello my love Angela'


@app.route('/countdown/')
@app.route('/countdown/<yyyymmdd>', methods=['GET'])
@support_jsonp
def show_countdown_days(yyyymmdd=None):

# curl -i -H "Content-type: application/json" -X GET -d {"rsvp_email":"tommy@hotmail.com"}' http://localhost:9999/countdown/
    # date_requested = datetime.strptime(yyyymmdd,'%Y%m%d').date()

    if request.mimetype == 'application/json':
        if yyyymmdd == None:
            return jsonify({'status': '200', 'daysleft': days_until()})
    else:

        # print datetime.datetime.strptime(yyyymmdd,'%Y%m%d').date()

        if yyyymmdd == None:
            return jsonify({'daysleft': days_until()})


def days_until():
    weddingDay = date(2013, 9, 15)
    diff = weddingDay - date.today()
    return abs(diff.days)





if __name__ == '__main__':
    app.run(port=5000, debug=True)
