from functools import wraps
from flask import Flask, jsonify, request, json, Response, Request
import csv


from flask.ext.mail import Mail, Message
# from pymongo import Connection

from datetime import *
import time

app = Flask(__name__)

mail=Mail(app)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'tommy.angico@gmail.com',
	MAIL_PASSWORD = 'healinghope3'
	)
mail=Mail(app)

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return app.response_class(content,
                    mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello():
    return 'hello my love, Angela'


@app.route('/countdown/')
@support_jsonp
def show_countdown_days(yyyymmdd=None):
# curl -i -H "Content-type: application/json" -X POST -d 'firstName=Tommy&lastName=Wu&attending=true' http://localhost:5000/rsvp/
    content_type = request.headers['Content-Type']
    if content_type == 'application/json':
        return jsonify(status=200, daysleft=days_until())
    else:
        return jsonify(request.headers['Content-Type'])


@app.route('/rsvp/', methods=['GET','POST'])
@support_jsonp
def rsvp():
	
    if request.headers['Content-Type'] == 'application/json':
        test_data = '{firstname:"tommy", "lastname":"Wu", "email":"wu.thomas@gmail.com", "timestamp":"%s"}'%datetime.now()
        return test_data

    return 'why not'



@app.route('/email/')
@support_jsonp
def send_email():
	# b1e78df7be8c36337dd3197d03b16d10
	if request.method == 'GET':
		# msg = Message('Hello there', sender=("Angela & Tommy", "tommg.angico@gmail.com"), recipients=['wu.thomas@gmail.com'])
		# msg.body = "This is the email body"
		# mail.send(msg)
		# print request['headers']+'..................'
		return jsonify(msg='it works')
	print request.mimetype


def days_until():
    weddingDay = date(2013, 9, 15)
    diff = weddingDay - date.today()
    return abs(diff.days)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
