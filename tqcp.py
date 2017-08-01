#/usr/local/env python
#coding:utf-8
import urllib2
import re

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

def get_urls(start,end):
    url = 'http://www.tqcp.net/index.php?m=content&c=index&a=lists&catid=6&page='
    for x in range(start,end+1):
        url = url + str(x)
        page = get_page(url,'gbk')
        pattern = re.compile('<ul class="font_14">(.*?)</ul>',re.S)
        print page
        items = re.findall(pattern,page)
        for item in items:
            print item


get_urls(1,2)