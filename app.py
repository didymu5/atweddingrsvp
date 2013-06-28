from functools import wraps
from flask import Flask, jsonify, request, json, Response, Request, render_template
from pymongo import MongoClient

from flask.ext.mail import Mail, Message
# from pymongo import Connection

from datetime import *
import time

app = Flask(__name__)


mURI = 'mongodb://wed_us:iloveangela@dharma.mongohq.com:10035/app16186982'
app.config['SECRET_KEY'] = 'ILOVEYOUangela'
client = MongoClient(mURI)

db = client.app16186982

collection = db.guests


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
@app.route('/countdown/<yyyymmdd>', methods=['GET'])
@support_jsonp
def show_countdown_days(yyyymmdd=None):
# curl -i -H "Content-type: application/json" -X POST -d 'firstName=Tommy&lastName=Wu&attending=true' http://localhost:5000/rsvp/
    if request.headers['Accept'] in 'application/json':
        return jsonify(status=200, daysleft=days_until())
    else:
        # print datetime.datetime.strptime(yyyymmdd,'%Y%m%d').date()
        if yyyymmdd == None:
            return jsonify({'dayslefts': days_until()})


@app.route('/rsvp/', methods=['GET','POST'])
@support_jsonp
def rsvp():
    a = []
    # print request.args

    if request.args:
        return request.args
    # print request.headers['Accept']
    for guest in collection.find():
        a.append(guest)
    
    return render_template('rsvp.html', guestList=a)
    # return str(collection)

#curl -i -H "Content-tjson" -X GET -d {"firstName":"Tommy", "lastName":"Wu","attending":true} http://localhost:5000/rsvp/

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
    app.run(port=5000, debug=True)