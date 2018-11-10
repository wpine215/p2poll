# main.py
from block import *
import datetime as date


def app():
	firstBlock = Block(0,date.datetime.now(),"0","Genesis Block")
	secondBlock = Block(1,date.datetime.now(),firstBlock.hash,"Trump")
	thirdBlock = Block(2,date.datetime.now(),secondBlock.hash,"Trump")
	
	print(secondBlock.hash)
	print(thirdBlock.hash)

if __name__ == '__main__':
	app()