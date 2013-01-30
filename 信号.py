#!/usr/bin/python
#coding=utf-8

import signal
print signal.SIGALRM
print signal.SIGCONT

def myHandler(signum,frame):
	print 'I received:',signum

#signal.signal(signal.SIGTSTP,myHandler)
#signal.pause()
#print 'End of signal demo'

def  handler(signum,frame):
	print 'now, it is the time'
	exit()

signal.signal(signal.SIGALRM,handler)
signal.alarm(5)

while True:
	print 'not yet'





















