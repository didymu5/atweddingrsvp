from flask import Flask, jsonify, request, json, Response
from datetime import *


app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
	return 'hello my love Angela'

if __name__ == '__main__':
	app.run()