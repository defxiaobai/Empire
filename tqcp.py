#/usr/local/env python
#coding:utf-8
import urllib2
import re
import TentTool
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

tentTool = TentTool.TentTool()
urllib2.socket.setdefaulttimeout(30)
# 获取页面内容 指定网站编码
def get_page(url, charcode,num=3):
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1'}
    try:
        request = urllib2.Request(url, headers=header)
        page = urllib2.urlopen(request,timeout=30)
        return page.read().decode(charcode)
    except urllib2.URLError as e:
        print "error", e.reason  # 可以捕获异常
        if num > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                get_page(url,charcode,num - 1)

def get_content(url):
    global tentTool
    page = get_page(url,'gbk')
    pattern = re.compile('<div class="font_14" style="line-height:180%;">(.*?)<div class="height_15"></div>',re.S)
    result = re.search(pattern,page)
    if not result:
        text = ''
    else:
        content = result.group(1).strip()
        text = tentTool.remove_tags(content)
        print text
        print '--------------------------------------'
        # print content
    pattern = re.compile('<div class="font_22 font_b" align="center">(.*?)</div>')
    result = re.search(pattern,page)
    if not result:
        title = ''
    else:
        title = result.group(1).strip()
    pattern = re.compile('<meta name="description" content="(.*?)" />',re.S)
    result = re.search(pattern,page)
    if not result:
        smalltext = ''
    else:
        smalltext = result.group(1).strip()

    postData(title,smalltext,text,title)


# 登陆
def postData(title, smalltext, text, keyboard):
    jiekou = 'http://www.jdms8.com/e/admin/jiekou.php'
    data = urllib.urlencode({
        'username': 'yeqiu',
        'classid': 5,
        'title': title,
        'keyboard': keyboard,
        'smalltext': smalltext,
        'infotags': '彩票预测',
        'newstext': text,
        'pw': '123456'

    })
    # 创建request
    request = urllib2.Request(jiekou, data)
    resp = urllib2.urlopen(request)
    if '成功' in resp.read():
        print '成功'

# 获取urls
def get_urls(catid,start,end,jqnum=0):

    for x in range(start,end+1):
        url = 'http://www.tqcp.net/index.php?m=content&c=index&a=lists&catid=' + str(catid) + '&page='
        print x
        url = url + str(x)
        print url
        page = get_page(url,'gbk')
        pattern = re.compile('<div class="General_News">(.*?)<div class="Content_shixian">',re.S)
        result = re.search(pattern,page)
        if not result:
            print None
            exit()
        else:
            pattern = re.compile('<a target=_blank href="(.*?)">.*?</a>')
            items = re.findall(pattern,result.group(1).strip())
            if jqnum != 0:
                items = items[0:jqnum]
            for item in items:
                # print item
                get_content(item)
                print str(x) + '-------'
                # exit()



get_urls(11,1771,3874)




