from flask import Flask, jsonify, request, json, Response
from datetime import *


app = Flask(__name__)
app.debug = True




if __name__ == '__main__':
	app.run()