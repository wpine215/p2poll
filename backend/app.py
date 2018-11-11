from flask import Flask, request, jsonify
import json
from twilio.rest import Client
from random import *
from creds import *

account_sid = creds()[0]
auth_token = creds()[1]
client = Client(account_sid, auth_token)
 
# global auth?Code
# authCode = -1

# def setAuthCode(code):
# 	global authCode
# 	authcode = code

# def getAuthCode():
# 	global authCode
# 	return authCode

app = Flask(__name__)

@app.route('/')
def index():
	return "Homepage"

@app.route('/lookup')
def lookup():
	voteid = request.args.get('voteid', default = 1, type = int)
	if voteid == 1:
		return jsonify({'date': 123, 'voted_for': 456})
	return jsonify({'voteid': voteid})

@app.route('/twofact', methods=['POST'])
def twofact():
	setAuthCode(randint(10000,99999)) 
	msgBody = "Your Two Factor Auth Code is: " + str(authCode)
	rec = '+18184371804'
	# message = client.messages.create(body=msgBody,from_='+16178556948',to=rec)
	print(msgBody)
	return "Hello"

@app.route('/vote')
def vote():
	print(authCode)
	token = request.args.get('token', default = 0, type = int)
	if token != authCode: 
		return jsonify({'auth':False})
	else:
		return jsonify({'auth':True})
			
@app.route('/login',methods=['GET','POST'])
def login():
	username = request.args.get('')


