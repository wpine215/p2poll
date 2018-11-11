from collections import OrderedDict
from urllib.parse import urlparse

import binascii
'''
title           : blockchain.py
description     : A blockchain implemenation
author          : Adil Moujahid
date_created    : 20180212
date_modified   : 20180309
version         : 0.5
usage           : python blockchain.py
                  python blockchain.py -p 5000
                  python blockchain.py --port 5000
python_version  : 3.6.1
Comments        : The blockchain implementation is mostly based on [1]. 
                  I made a few modifications to the original code in order to add RSA encryption to the transactions 
                  based on [2], changed the proof of work algorithm, and added some Flask routes to interact with the 
                  blockchain from the dashboards
References      : [1] https://github.com/dvf/blockchain/blob/master/blockchain.py
                  [2] https://github.com/julienr/ipynb_playground/blob/master/bitcoin/dumbcoin/dumbcoin.ipynb
'''

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json

from time import time
from uuid import uuid4

MINING_SENDER = "THE BLOCKCHAIN"
MINING_REWARD = 100
MINING_DIFFICULTY = 2

class Blockchain:

    def __init__(self):
        
        self.votes = []
        self.chain = []
        self.nodes = set()
        #Generate random number to be used as node_id
        self.node_id = str(uuid4()).replace('-', '')
        #Create genesis block
        self.create_block(0, '00')

    def register_node(self, node_url):
        """
        Add a new node to the list of nodes
        """
        #Checking node_url has valid format
        parsed_url = urlparse(node_url)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def verify_vote_signature(self, voter_id, signature, vote):
        """
        Check that the provided signature corresponds to vote
        signed by the public key (voter_id)
        """
        public_key = RSA.importKey(binascii.unhexlify(voter_id))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA.new(str(vote).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(signature))

    def submit_vote(self, voter_id, poll_id, value, signature):
        """
        Add a transaction to transactions array if the signature verified
        """
        vote = OrderedDict({'voter_id': voter_id, 
                                    'poll_id': poll_id,
                                    'value': value})

        # Reward for mining a block
        if voter_id == MINING_SENDER:
            self.votes.append(vote)
            return len(self.chain) + 1
        # Manages votess from wallet to another wallet
        else:
            vote_verification = self.verify_vote_signature(voter_id, signature, vote)
            if vote_verification:
                self.votes.append(vote)
                return len(self.chain) + 1
            else:
                return False

    def create_block(self, nonce, previous_hash):
        """
        Add a block of votes to the blockchain
        """
        block = {'block_number': len(self.chain) + 1,
                'timestamp': time(),
                'votes': self.votes,
                'nonce': nonce,
                'previous_hash': previous_hash}

        # Reset the current list of votes
        self.votes = []

        self.chain.append(block)
        return block

    def hash(self, block):
        """
        Create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self):
        """
        Proof of work algorithm
        """
        last_block = self.chain[-1]
        last_hash = self.hash(last_block)

        nonce = 0
        while self.valid_proof(self.votes, last_hash, nonce) is False:
            nonce += 1

        return nonce

    def valid_proof(self, votes, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        """
        Check if a hash value satisfies the mining conditions. This function is used within the proof_of_work function.
        """
        guess = (str(votes)+str(last_hash)+str(nonce)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:difficulty] == '0'*difficulty

    def valid_chain(self, chain):
        """
        Check if a bockchain is valid
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            #print(last_block)
            #print(block)
            #print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            #Delete the reward vote
            votes = block['votes'][:-1]
            # Need to make sure that the dictionary is ordered. Otherwise we'll get a different hash
            vote_elements = ['voter_id', 'poll_id', 'value']
            votes = [OrderedDict((k, vote[k]) for k in vote_elements) for vote in votes]

            if not self.valid_proof(votes, block['previous_hash'], block['nonce'], MINING_DIFFICULTY):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        Resolve conflicts between blockchain's nodes
        by replacing our chain with the longest one in the network.
        """
        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            print('http://' + node + '/chain')
            response = requests.get('http://' + node + '/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False