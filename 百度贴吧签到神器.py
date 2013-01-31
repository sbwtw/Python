#!/usr/bin/python
#coding=utf-8

#
#	Author: 石博文 <sbwtws@gmail.com>
#	
#	Android 下运行需要安装 PythonForAndroid.apk sl4a.apk
#

import os
import re
import time
import urllib
import urllib2
import cookielib

# headers
headers={}
headers['User-Agent']=''

# 绑定cookie到opener
cookie=cookielib.MozillaCookieJar('cookie')
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

# 返回10位数的时间戳
def getTime():
	return int(time.time())

# 登陆函数,登陆贴吧,获得cookie
def login(usr,pwd):
	# 首页
	urllib2.urlopen('http://wapp.baidu.com')
	# 分离cookie => uid
	ck=re.search(r'wapp_[_0-9]{17}',str(cookie))
	if ck:
		ck=ck.group()
		print '打开首页成功.'
	else:
		print '打开首页失败.'
		return None
	# 构造数据
	postData={
		'aaa':'登录',
		'bd_page_type':'1',
		'can_input':'0',
		'from':'',
		'login':'yes',
		'login_loginpass':pwd,
		'login_start_time':getTime(),
		'login_username':usr,
		'login_username_input':'0',
		'pu':'',
		'ssid':'',
		'tn':'bdIndex',
		'tpl':'tb',
		'type':'',
		'u':'http://wapp.baidu.com/',
		'uid':ck
	}
	# 登录
	print '尝试登录.'
	req=urllib2.Request(
		url='http://wappass.baidu.com/passport/',
		data=urllib.urlencode(postData),
		headers=headers
	)
	res=urllib2.urlopen(req)
	res=res.read()
	# 分离登录url
	passUrl=re.search(r'http:\/\/wapp\.baidu\.com\/\?errno=0[\w&;=\.]+(?=")',res)
	if passUrl:
		passUrl=passUrl.group()
		print '分离登陆url.'
	# 验证码 !==未完成==!
	elif re.search('验证码',res):
		print '遭遇验证码!地址为:'
		yzm=re.search(r'http:\/\/wappass\.baidu\.com\/cgi-bin\/genimage\?[^"]+',res)
		print yzm.group()
		return None
	else:
		print '登录失败'
		return None
	# 验证登录,得到cookie
	req=urllib2.Request(
		url=passUrl,
		headers=headers
	)
	res=urllib2.urlopen(req)
	res=res.read()
	# 若返回页面中含有用户名,说明登陆成功
	submit=re.search(usr,res)
	if submit:
		print '登陆成功.'
	else:
		print '验证失败.'
		return None
	cookie.save()
	return True
	# 	== init End ==

# 拉取'我喜欢的吧'列表
def getBars():
	print '拉取贴吧列表.'
	req=urllib2.Request(
		url='http://wapp.baidu.com/m?tn=bdFBW&tab=favorite',
		headers=headers
	)
	res=urllib2.urlopen(req)
	bars=re.findall(r'(?:\d+\.<a href="[^"]+">)([^<]+)(?:</a>)',res.read())
	if bars:
		print '读取完毕,共%d个吧需要签到' % len(bars)
	else:
		print '贴吧列表读取失败.'
		return None
	return bars

# 签到函数,因为此函数经常访问网络,所以加上超时处理
def sign(bar):
	print '进入%s吧' % bar
	headers['Referer']='http://wapp.baidu.com/f/m?kw='+bar
	req=urllib2.Request(
		url='http://wapp.baidu.com/f/?kw='+urllib.quote(bar),
		headers=headers
	)
	try:
		res=urllib2.urlopen(req,timeout=10)
		res=res.read()
	except urllib2.URLError:
		print '访问超时!'
		sign(bar)
		return True
	# 签到地址
	addr=re.search(r'(?<=<a href=")[^"]+(?=">签到)',res)
	if not addr:
		print '已签到\n'
		return True
	# 替换 'amp;' 不然无法签到
	addr=re.sub(r'amp;','',addr.group())
	url='http://wapp.baidu.com'+addr
	req=urllib2.Request(
		url=url,
		headers=headers
	)
	try:
		res=urllib2.urlopen(req,timeout=10)
		res=res.read()
	except urllib2.URLError:
		print '访问超时!'
		sign(bar)
		return True
	success=re.search(r'(?<="light">)\d(?=<\/span>)',res)
	if not success:
		print '%s吧,未知错误' % bar
		return None
	print '%s吧签到成功,经验+%s\n' % (bar,success.group())
	return True
	#	sign End

# 启动函数
def init():
	print 'start working...'
	# 读取配置信息
	if os.path.exists('cookie'):
		cookie.load('cookie')
	# 新建配置
	else:
		usr=raw_input('输入用户名: ')
		pwd=raw_input('输入密码:   ')
		if not login(usr,pwd):
			return None
	# 拉取吧列表
	bars=getBars()
	if bars:
		# 开始签到
		for bar in bars:
			sign(bar)
	else:
		return None



init()
















