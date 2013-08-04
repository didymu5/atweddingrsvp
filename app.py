from functools import wraps
from ast import literal_eval
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
    # if request.headers['Accept'] in 'application/json':
    #     return jsonify(status=200, daysleft=days_until())
    # else:
    #     # print datetime.datetime.strptime(yyyymmdd,'%Y%m%d').date()
    #     if yyyymmdd == None:
    return jsonify({'daysleft': days_until()})


@app.route('/rsvp/', methods=['GET','POST'])
@support_jsonp
def rsvp():
    a = []
    sender='tommy.angico@gmail.com'
    host_email = ''
    # print request.args
# {u'email': u'cord.of.three@gmail.com', u'firstname': u'Angela', u'isAttending': True, u'lastname': u'Hsieh', u'timeStamp': datetime.datetime(2013, 6, 27, 16, 1, 58, 534000), u'guestOf': u'', u'_id': ObjectId('51ccbbedb181d7b90ccbf74c')}
    if request.args:
        alist = []
        
        # catches just the first host
        if request.args.get('email_of_host'):
            aperson = {'email':request.args.get('email_of_host'), 'guestOf':''}
            aperson['firstname'] = request.args.get('firstname').title().strip()
            aperson['timeStamp'] = datetime.now()
            aperson['lastname'] = request.args.get('lastname').title().strip()
            aperson['isAttending'] = request.args.get('is_attending')
            print '\n'
            print aperson
            print '\n'
            obj_id = collection.insert(aperson)
            
            host_email = aperson['email']
            
            if obj_id and aperson['isAttending'] == 'true':
                msg = Message('Thank you for RSVPing', sender = 'tommy.angico@gmail.com', recipients=[host_email])
                msg.body = "So happy that you are coming!\n\nCeremony @ 3pm\nMessiah Lutheran Church\n4861 Liverpool St\nYorba Linda, CA 92886\n\n\nCocktail hour and Reception @ 5pm\nSummit House\n2000 E Bastanchury Rd\nFullerton, CA 92835\n\n\nPlease feel free to email us if you have any questions. Check back at wedding.happygrunt.com for updates."
                mail.send(msg)
            

        # When there is a guest list
        if request.args.get('guestlist'):
            guestlist = request.args.get('guestlist')
            
            for aguest in guestlist.split('|'):
                bperson = {'email':'', 'guestOf':request.args.get('guest_of'), 'isAttending':'true'}
                bperson['firstname'] = aguest.split(',')[0].split('firstname=')[1]
                bperson['timeStamp'] = datetime.now()
                bperson['lastname'] = aguest.split(',')[1].split('lastname=')[1]
                alist.append(bperson)
                
            print '\n\ninserting this list of objects\n\n', alist , '\n\n\n'
            # print guestlist.split('|')[0]
            # print literal_eval(guestlist.split('|')[0])
            collection.insert(alist)

        if host_email and len(alist) != 0:
            names = ''
            for guest in alist:
                names += guest['firstname']+' '+guest['lastname']+' '
            msg = Message('RSVP - Guest', sender = 'tommy.angico@gmail.com', recipients=[host_email])
            msg.body = "These people are coming as your guests: "+ names
            mail.send(msg)
        
        return jsonify(firstname='test')
    # print request.headers['Accept']
    for guest in collection.find():
        a.append(guest)
    
    return render_template('rsvp.html', guestList=a)
    # return str(collection)

#curl -i -H "Content-tjson" -X GET -d {"firstName":"Tommy", "lastName":"Wu","attending":true} http://localhost:5000/rsvp/
@app.route('/edit/')
@app.route('/edit/<int:obj_id>')
def edit_doc(obj_id):
    return obj_id

# @app.route('/killdata/')
# def killall():
#     test = collection.remove()
#     print test
#     return 'data killed'

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
    app.run(debug=True)