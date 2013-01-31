#!/usr/bin/python
#coding=utf-8

#import httplib
#
#print 'working'
#
#conn=httplib.HTTPConnection('http://www.baidu.com',80,False)
#conn.request('get','/','',{'Host':'www.google.com',
#						'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5',
#						'Accept':'text/plain'})
#res=conn.getresponse()
#print 'version:',res.version
#print 'reason:',res.reason
#print 'status:',res.status
#print 'msg:',res.msg
#print 'headers:',res.getheaders()
#print 'content:',res.read()
#conn.close()

import urllib
import urllib2
print 'working'

#req=urllib2.Request('http://www.baidu.com')
#res=urllib2.urlopen(req)
#print res.read()

#	post
#values={'body':'test body','via':'xxx'}
#data=urllib.urlencode(values)
#					url,data,headers
#req=urllib2.Request('http://wap.baidu.com/')
#res=urllib2.urlopen(req)
#print res.read()

#req=urllib2.Request('http://python.org/ff.html')
#try:
#	urllib2.urlopen(req)
#except URLError,e:
#	print e.code
#	print e.read()
import cookielib
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
urllib2.urlopen('http://wapp.baidu.com/')
for ck in cookie:
	print ck
print cookie

import time
print int(time.time())

import re
res=re.search(r'wapp_[_0-9]{17}',str(cookie))
if res:
	res=res.group()
print res

postData={}
postData['aaa']='登录'
postData['bd_page_type']='1'
postData['can_input']='0'
postData['from']=''
postData['login']='yes'
postData['login_loginpass']=''
postData['login_start_time']=int(time.time())
postData['login_username']='o丨Reborn'
postData['login_username_input']='0'
postData['pu']=''
postData['ssid']=''
postData['tn']='bdIndex'
postData['tpl']='tb'
postData['type']=''
postData['u']='http://wapp.baidu.com/'
postData['uid']=res
postData=urllib.urlencode(postData)
headers={
	'User-Agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
}
req=urllib2.Request(
	url='http://wappass.baidu.com/passport/',
	data=postData,
	headers=headers
)

res=urllib2.urlopen(req)
res=res.read()
rr=re.search(r'http:\/\/wapp\.baidu\.com\/\?errno[\w&;=\.]+(?=")',res)
if rr:
	res=rr.group()

req=urllib2.Request(
	url=res,
	headers=headers
)
rr=urllib2.urlopen(req)
print rr.read()
















