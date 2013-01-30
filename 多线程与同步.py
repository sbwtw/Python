#!/usr/bin/python
#coding=utf-8

import threading
import time
import os
import random

# 每个线程执行的函数
class boothThread(threading.Thread):
	def __init__(self,tid,monitor):
		self.tid=tid
		self.monitor=monitor
		self.count=0
		# 继承了thread.Thread类
		threading.Thread.__init__(self)
	# run函数,自动调用
	def run(self):
		while True:
			# 锁和数量是共享的
			monitor['lock'].acquire()
			if monitor['tick']!=0:
				monitor['tick']-=1
				self.count+=1
				print self.tid,'buy',self.count,'now left:',monitor['tick']
			else:
				print 'Thread id',self.tid,'no more tickets'
				os._exit(0)
			# 解锁,随机延时
			monitor['lock'].release()
			time.sleep(random.random()/5)

monitor={'tick':300,'lock':threading.Lock()}

# 创建线程
for k in range(10):
	newThread=boothThread(k,monitor)
	newThread.start()

## 面向过程的版本
## 每个线程运行的函数,传入线程ID
#def booth(tid):
#	# 全局的变量记录次数,共享线程锁
#	global i
#	global lock
#	while True:
#		# 开启线程锁
#		lock.acquire()
#		if i!=0:
#			i=i-1
#			print tid,'now left',i
#		else:
#			print 'Thread id',tid,'no more tikets'
#			os._exit(0)
#		# 关闭线程锁
#		lock.release()
#		# 随机等待
#		time.sleep(random.random()*10)
#
#
#i=100;
## 共享线程锁
#lock=threading.Lock()
#
## 创建10个线程
#for k in range(10):
#	new_thread=threading.Thread(target=booth,args=(k,))
#	# 开启线程
#	new_thread.start()




















