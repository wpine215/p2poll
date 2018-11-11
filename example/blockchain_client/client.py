from vote import *

import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('./index.html')

@app.route('/cast/vote')
def make_transaction():
	return render_template('./cast_vote.html')

@app.route('/view/votes')
def view_transaction():
	return render_template('./view_votes.html')

@app.route('/wallet/new', methods=['GET'])
def new_wallet():
	random_gen = Crypto.Random.new().read
	private_key = RSA.generate(1024, random_gen)
	public_key = private_key.publickey()
	response = {
		'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
		'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii')
	}

	return jsonify(response), 200

@app.route('/generate/vote', methods=['POST'])
def generate_vote():
	
	#### DATA MODIFIED HERE ####
	voter_id = request.form['voter_id']
	voter_key = request.form['voter_key']
	poll_id = request.form['poll_id']
	value = request.form['value']

	vote = Vote(voter_id, voter_key, poll_id, value)
	############################

	response = {'vote': vote.to_dict(), 'signature': vote.sign_vote()}

	return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)