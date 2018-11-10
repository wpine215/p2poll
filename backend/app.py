from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
	return "Homepage"

@app.route('/lookup')
def lookup():
	voteid = request.args.get('voteid', default = 1, type = str)
	if voteid == 1:
		return jsonify({'date': 123, 'voted_for': 456})
	return jsonify({'voteid': voteid})

@app.route('/vote', methods=['GET','POST'])
def vote():
	if request.method == 'POST':
		# call twillio api
		pass
	else:
		pass


@app.route('/login',methods=['GET','POST'])
def login():
	username = request.args.get(''