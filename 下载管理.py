#!/usr/bin/bython
#coding=utf-8
import os
import re
import shutil

print 'start...'

def move(file):
	# 豆瓣mp3
	if re.match(r'.*_豆瓣_.*\.mp3',file):
		newName=re.sub(r'^(.*)_豆瓣_.*\.mp3',r'\1'+'.mp3',file)
		newName=re.sub(r'_',' ',newName)
		#os.rename('/data/下载/'+file,'/data/下载/'+newName)
		print 'move 豆瓣mp3 %s to %s' % (file,newName)
		shutil.move('/data/下载/'+file,'/data/音乐/'+newName)
	# pdf,chm
	elif re.match(r'.*\.[chm|pdf]',file):
		print 'move %s to documents' % file
		shutil.move('/data/下载/'+file,'/data/文档/')
	# 图片
	elif re.match(r'.*\.[png|jpg|gif]',file):
		print 'move %s to picture' % file
		shutil.move('/data/下载/'+file,'/data/图片/图片/')
	# 韩顺平jsp
	elif re.match(r'韩顺平.*细说jsp.*',file):
		print 'move',file
		shutil.move('/data/下载/'+file,'/data/视频/jsp 韩顺平/')

files=os.listdir('/data/下载')
for file in files:
	if os.path.isfile('/data/下载/'+file):
		move(file)













