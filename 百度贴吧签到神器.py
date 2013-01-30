#!/usr/bin/python
#coding=utf-8

import re
import time
import urllib
import urllib2
import cookielib

# 预定义账号密码
usr=''
pwd=''
# headers
headers={
	'User-Agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7'
}
# 贴吧列表
bars=[]



print 'start working...'

# 绑定cookie到opener
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

# 返回10位数的时间戳
def getTime():
	return int(time.time())

# 启动函数,登陆贴吧,获得cookie
def init(usr,pwd):
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
	return True
	# 	== init End ==

# 拉取'我喜欢的吧'列表
def getBars():
	# 贴吧列表放到全局共享
	global bars
	print '拉取贴吧列表.'
	# 记录拉取了几页
	count=1
	while True:
		req=urllib2.Request(
			url='http://tieba.baidu.com/f/like/mylike?&pn='+str(count),
			headers=headers
		)
		res=urllib2.urlopen(req)
		# 此页面编码为gbk
		res=res.read().decode('gbk','ignore')
		getBars=re.findall(r'(?:<a href="[^"]+" title=")([^"]+)(?:">\1</a>)',res)
		if getBars:
			bars+=getBars
			print '第%d页分析完毕.' % count
			count+=1
		else:
			break
	if bars:
		print '拉取完毕,共%d个吧需要签到' % len(bars)
	else:
		print '拉取贴吧列表失败.'

	print bars



if init(usr,pwd):
	getBars()

















