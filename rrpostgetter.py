#encoding=utf-8
import urllib, urllib2, cookielib, re
from BeautifulSoup import BeautifulSoup

myCookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(myCookie)
post_data = {
		'email':'email here',
		'password':'password here',
		'origURL':'http://www.renren.com/home',
		'domain':'renren.com'
		}
req = urllib2.Request('http://www.renren.com/PLogin.do', urllib.urlencode(post_data))
html_src = opener.open(req).read()
#print html_src
posts = []
pattern = re.compile(r'.*href="(.*?)".*?', re.I | re.X)
for i in range(18):
	theURL = 'http://share.renren.com/share/hotlist?curpage=' + str(i) + '&t=1&__view=async-html-reload' if i < 6 else 'http://share.renren.com/share/friend?curpage=' + str(i - 6) + '&type=1&__view=async-html'
	req = urllib2.Request(theURL)
	html_src = opener.open(req).read()
	#print "get page " + theURL
	#print html_src
	parser = BeautifulSoup(html_src)
	posts_list = parser.findAll('li','share') if i < 6 else parser.findAll('div', 'share-content')
	for post in posts_list:
		#print post
		post = post.h3.a.__str__('GB18030') if i < 6 else post.h4.a.__str__('GB18030')
		m = pattern.match(post)
		if m:
			#print m.groups(0)[0]
			posts.append(m.groups(0)[0])

print "Got all posts"

statistic = {}
i = 0

def doStatistic(txt):
	for i in range(len(txt) - 1):
		word = txt[i] + txt[i + 1]
		#print word
		if statistic.get(word) != None:
			statistic[word] += 1
		else:
			statistic[word] = 1

for post in posts:
	#i += 1
	if i > 10:
		break
	req = urllib2.Request(post)
	html_src = opener.open(req).read()
	parser = BeautifulSoup(html_src)
	title = parser.find('h3','title-article')
	if title != None:
		title = title.strong.text
		content = parser.find('div', 'text-article').text
		doStatistic(title)
		doStatistic(content)

print "Statistic Finished"

word_list = statistic.keys()
word_list.sort(cmp = lambda x, y: cmp(statistic[y], statistic[x]))

for word in word_list:
	if statistic[word] > 4:
		print word + ": " + str(statistic[word])

print "Finished"
