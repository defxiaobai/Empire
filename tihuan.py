#/usr/bin/env python
#coding:utf-8

import urllib2
import re


# 获取页面内容 指定网站编码
def get_page( url, charcode):
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

def get_urls(page):
    pattern = re.compile('<div id="content">.*?(.*?).*?</div>',re.S)
    result = re.search(pattern,page)
    if not result:
        print '没有找到内容'
    else:
        page = result.group(0).strip()
        pattern = re.compile('<li><a href="(.*?)".*?>.*?</a>.*?</li>',re.S)
        items = re.findall(pattern,page)
        if not items:
            print '没有匹配到'
        else:
            for item in items:
               print '<a href="'+item+'">'+item+'</a>'

page = get_page('http://www.bayuad.com/sitemap.html','utf-8')
get_urls(page)