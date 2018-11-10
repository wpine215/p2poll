# main.py
from block import *
import datetime as date


def app():
	firstBlock = Block(0,date.datetime.now(),"Genesis Block", "0")
	secondBlock = Block(1,date.datetime.now(),"Trump",firstBlock.hash)
	thirdBlock = Block(1,date.datetime.now(),"Trump",secondBlock.hash)
	
	print(secondBlock.hash)
	print(thirdBlock.hash)

if __name__ == '__main__':
	app()