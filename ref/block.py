import hashlib as hasher

class Block:
	def __init__(self, index, timestamp, previous_hash, voteData, pollData = None, voterData = None):
		self.index = index
		self.timestamp = timestamp
		self.previous_hash = previous_hash

		self.votes = voteData
		self.polls = pollData
		self.voters = voterData

		self.hash = self.hash_block()

	def hash_block(self):
		sha = hasher.sha256()
		sha.update((str(self.index) + str(self.timestamp) + str(self.votes) + str(self.polls) + str(self.voters) + str(self.previous_hash)).encode('utf-8'))
		return sha.hexdigest()







