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

# 获取页面内容 指定网站编码
def get_page(url, charcode):
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1'}
    try:
        request = urllib2.Request(url, headers=header)
        page = urllib2.urlopen(request)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print '获取页面错误，错误原因：%s' % e.reason
            return None
        if hasattr(e, 'code'):
            print '获取页面错误，错误代码：%s' % e.code
            return None
    else:
        return page.read().decode(charcode)

def get_content(url):
    global tentTool
    page = get_page(url,'gbk')
    pattern = re.compile('<div class="font_14" style="line-height:180%;">(.*?)</div>',re.S)
    result = re.search(pattern,page)
    if not result:
        text = ''
    else:
        content = result.group(1).strip()
        text = tentTool.remove_tags(content)
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
        'classid': 1,
        'title': title,
        'keyboard': keyboard,
        'smalltext': smalltext,
        'infotags': '南国特区彩票,特区彩票七星彩论坛',
        'newstext': text,
        'pw': '123456'

    })
    # 创建request
    request = urllib2.Request(jiekou, data)
    resp = urllib2.urlopen(request)
    if '成功' in resp.read():
        print '成功'

# 获取urls
def get_urls(start,end):
    url = 'http://www.tqcp.net/index.php?m=content&c=index&a=lists&catid=6&page='
    for x in range(start,end+1):
        url = url + str(x)
        page = get_page(url,'gbk')
        pattern = re.compile('<div class="General_News">(.*?)<div class="Content_shixian">',re.S)
        result = re.search(pattern,page)
        if not result:
            print None
        else:
            pattern = re.compile('<a target=_blank href="(.*?)">.*?</a>')
            items = re.findall(pattern,result.group(1).strip())
            for item in items:
                get_content(item)
                # exit()
            print '-------'


get_urls(1,2)