import hashlib as hasher

class Block:
	def __init__(self, index, timestamp, voteData, pollData = None, voteData = None, previous_hash):
		self.index = index
		self.timestamp = timestamp
		self.votes = voteData
		self.polls = pollData
		self.voters = voteData
		self.previous_hash = previous_hash
		self.hash = self.hash_block()

	def hash_block(self):
		sha = hasher.sha256()
		sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
		return sha.hexdigest()







