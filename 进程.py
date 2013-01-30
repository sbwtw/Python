#!/usr/bin/python
#coding=utf-8

import subprocess
import time

print 'start'
rc=subprocess.check_output(['ls','-la'])
print rc

#child=subprocess.Popen(['ping','-c','5','www.google.com'])
#for i in range(1,5):
	#time.sleep(1)
	#print child.pid


child1=subprocess.Popen(['ls','-la'],stdout=subprocess.PIPE)
child2=subprocess.Popen(['cat'],stdin=child1.stdout,stdout=subprocess.PIPE)
print child2.communicate()






import os
print os.getuid()
print os.getgid()



















