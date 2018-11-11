import socket
import struct
import threading
import time
import traceback

def btdebug( msg ):
    """ Prints a messsage to the screen with the name of the current thread """
    print("[%s] %s" % (str(threading.currentThread().getName()), msg))

class Peer:
	def __init__(self, maxpeers, port, pid=None, host=None):
		self.debug = 0;

		self.maxpeers = int(maxpeers)
		self.port = int(port)
		self.id = pid

		if host:
			self.host = host
		else:
			self.__initHost()
		# endif

		self.peers = {}

		self.shutdown = False	

		self.handlers = {}
		self.router = None

	def __debug(self, msg):
		if self.debug:
			btdebug(msg)

	def makeServerSocket(self, port, backlog=5):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		s.bind(('', port))
		s.listen(backlog)
		return s

	def mainloop(self):
		s = self.makeServerSocket(self.port)
		s.settimeout(2)
		self.__debug('Server started: %s (%s:%d)' % ( self.id, self.host, self.port ))

		while not self.shutdown:
			try:
				self.__debug('Listening for connections...')
				clientsock, clientaddr = s.accept()
				clientsock.settimeout(None)
				t = threading.Thread(target = self.__handlePeer, args = [clientsock] )
				t.start()
			except KeyboardInterrupt:
				self.shutdown = True
				continue
			except:
				if self.debug:
					traceback.print_exc()
					continue
		# endwhile

		self.__debug("Main loop exiting")
		s.close()

	def __handlePeer(self, clientsock):
		self.__debug('Connected: ' + str(clientsock.getpeername()))

		host, port = clientsock.getpeername()
		peercon = BTPeerConnection(None, host, port, clientsock, debug=False)

		try:
			msgtype, msgdata = peercon.recvdata()
			if msgtype:
				msgtype = msgtype.upper()
			if msgtype not in self.handlers:
				self.__debug('Not handled: %s: %s' % (msgtype, msgdata))
			else:
				self.__debug('Handling peer msg: %s: %s' % (msgtype, msgdata))
				self.handlers[msgtype](peerconn, msgdata)
		except KeyboardInterrupt:
			raise
		except:
			if self.debug:
				traceback.print_exc()

		self.__debug('Disconnecting ' + str(clientsock.getpeername()))
		peerconn.close()


	def sendtopeer(self, peerID, msgType, msgData, waitReply = True):
		if self.router:
			nextpid, host, port = self.router(peerid)
		if not self.router or not nextpid:
			self.__debug('Unable to route %s to %s' % (msgtype, peerid))
			return None
		return self.connectandsend(host, port, msgtype, msgdata, pid=nextpid, waitreply=waitreply)

	def connectandsend(self, host, port, msgType, msgData, pid = None, waitreply = True):
		msgreply = []
		try:
			peerconn = BTPeerConnection(pid, host, port, debug=self.debug)
			peerconn.senddata(msgtype, msgdata)
			self.__debug('Sent %s: %s' % (pid, str(msgreply)))

			if waitreply:
				onereply = peerconn.recvdata()
				while(onereply != (None, None)):
					msgreply.append(onereply)
					self.__debug('Got reply %s: %s' % (pid, str(msgreply)))
				onereply = peerconn.recvdata()
			peerconn.close()
		except KeyboardInterrupt:
			raise
		except:
			if self.debug:
				traceback.print_exc()

		return msgreply

def app():
	mypeer = Peer(5, 5050, 1, '127.0.0.1')
	mypeer.mainloop()

if __name__ == '__main__':
	app()