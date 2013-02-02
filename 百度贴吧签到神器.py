#!/usr/bin/python
#coding=utf-8

#
#	Author: 石博文 <sbwtws@gmail.com>
#
# Android使用说明:
#	1.先安装"sl4a_r6.apk"
#	2.把"百度贴吧签到神器.py"丢进sl4a下面一个叫script的文件夹
#	3.安装PythonForAndroid_r4.apk
#	4.打开PythonForAndroid,点击最上面的install
#	5.打开sl4a,点击"百度贴吧签到神器"运行.
#

import os
import re
import time
import urllib
import urllib2
import cPickle
import cookielib

# headers
headers={}
headers['User-Agent']=''

# 共享的数据
bars={}
cookie=None

# 初始化,绑定cookie到opener
def setCookie(usr):
	global cookie
	cookie=cookielib.MozillaCookieJar(usr+'.cookie')
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	urllib2.install_opener(opener)

# 返回当前几号
def getDay():
	return time.gmtime().tm_mday

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
	submit=re.search('我爱逛的贴吧',res)
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
	barList=re.findall(r'(?:\d+\.<a href="[^"]+">)([^<]+)(?:</a>)',res.read())
	if barList:
		print '读取完毕,共%d个吧需要签到' % len(barList)
		# 将列表转换为字典
		global bars
		for bar in barList:
			bars[bar]=True
	else:
		print '贴吧列表读取失败.'
		return None
	return True

# 签到函数,因为此函数经常访问网络,所以加上超时处理
def sign(bar):
	global bars
	print '进入%s吧' % bar
	headers['Referer']='http://wapp.baidu.com/f/m?kw='+bar
	req=urllib2.Request(
		url='http://wapp.baidu.com/f/?kw='+urllib.quote(bar),
		headers=headers
	)
	try:
		res=urllib2.urlopen(req,timeout=5)
		res=res.read()
	except:
		print '%s吧访问超时!' % bar
		return sign(bar)
	# 签到地址
	addr=re.search(r'(?<=<a href=")[^"]+(?=">签到)',res)
	if not addr:
		bars[bar]=False
		return '%s吧已签到\n' % bar
	# 替换 'amp;' 不然无法签到
	addr=re.sub(r'amp;','',addr.group())
	url='http://wapp.baidu.com'+addr
	req=urllib2.Request(
		url=url,
		headers=headers
	)
	try:
		res=urllib2.urlopen(req,timeout=5)
		res=res.read()
	except:
		print '%s吧访问超时!' % bar
		return sign(bar)
	success=re.search(r'(?<="light">)\d(?=<\/span>)',res)
	if not success:
		return '%s吧,未知错误\n' % bar
	bars[bar]=False
	return '%s吧签到成功,经验+%s\n' % (bar,success.group())
	#	sign End

# 启动函数
def init():
	print 'start working...'
	usr=raw_input('输入用户名:')
	# 查询对应的用户配置文件
	if os.path.exists(usr+'.conf'):
		f=file(usr+'.conf')
		day=cPickle.load(f)
		global bars
		bars=cPickle.load(f)
		f.close()
		# 如果日期不相等,bars需要重新抓取
		if day!=str(getDay()):
			bars={}
	# 设置cookie
	setCookie(usr)
	global cookie
	if os.path.exists(usr+'.cookie'):
		cookie.load(usr+'.cookie')
	else:
		pwd=raw_input('输入密码:  ')
		if not login(usr,pwd):
			return None
	# 如果bars为空,则要重新抓取贴吧列表
	if not bars:
		getBars()
	if bars:
		# 开始签到
		for bar in bars:
			if bars[bar]:
				print sign(bar)
	else:
		return None
	# 写配置文件
	f=file(usr+'.conf','w')
	cPickle.dump(str(getDay()),f)
	cPickle.dump(bars,f)
	f.close()
	print '签到完成!\n'
	# 对签到情况检查
	err=False
	for bar in bars:
		if bars[bar]:
			print '%s吧签到失败!' % bar
			err=True
	if err:
		print '\n已记录签到失败的吧,请重新运行补签.'
	os._exit(0)



init()
















