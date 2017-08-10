#/usr/local/env python
#coding:utf-8
import urllib2
import re
import sys

class Jb51(object):

    def __init__(self,dir):
        self._dir = dir
        self._prefix = 'http://www.jb51.net/'

    # 获取页面内容
    def get_page(self, url):
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
            return page.read().decode('gbk')

    #获取列表
    def get_urls(self,start,end):
        urls = []
        for x in range(start,end+1):
            url = 'http://www.jb51.net/os/list682_'+str(x)+'.html'
            print url
            page = self.get_page(url)
            pattern = re.compile('<dl>.*?<dt>.*?<a href="(.*?)" target="_blank">.*?</a>.*?</dt>.*?</dl>',re.S)
            items = re.findall(pattern,page)
            if not items:
                print '没有匹配到网址'
                continue
            for item in items:
                url = 'http://www.jb51.net'+item
                urls.append(url)
        return urls

    #获取内容
    def get_content(self,url):
        jianjie = ''
        neirong = ''
        page = self.get_page(url)
        pattern = re.compile('<div class="art_desc mt10">(.*?)</div>')
        result = re.search(pattern,page)
        if not result:
            print '没有匹配到简介'
            jianjie = ''
        else:
            jianjie = result.group(1).strip()
        content_pattern = re.compile('<div id="content">(.*?)</div>',re.S)
        result = re.search(content_pattern,page)
        if not result:
            print '没有匹配到内容'
            neirong = ''
        else:
            neirong = result.group(1).strip()
        pattern = re.compile('<div class="cupage">(.*)',re.S)
        result = re.search(pattern,neirong)
        if not result:
            print '没有匹配到'
        else:
            cupage = result.group(1).strip()
            pattern = re.compile("<a href='(.*?)'>.*?</a>")
            pageurls = re.findall(pattern,cupage)
            if not pageurls:
                print '没有匹配到'
            allurl = self._prefix + self._dir + '/'+ pageurls.pop()
            page = self.get_page(allurl)
            result = re.search(content_pattern,page)
            if not result:
                print '没有匹配到内容'
            else:
                result.group(1).strip()



jb51 = Jb51('os')
jb51.get_content('http://www.jb51.net/os/1722.html')