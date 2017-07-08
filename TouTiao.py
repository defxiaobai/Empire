#!/usr/bin/env python
#coding:utf-8
import urllib2
import json
import re
import ContentTool
import urllib



class TouTiao(object):

    # 采集关键词对应的关键词和要采集的数量
    def __init__(self,keyword,num,offset = 0):
        self._keyword = urllib.quote(keyword)
        self._num = num
        self._contentTool = ContentTool.ContentTool()
        self._offset = offset
        self._urls = []

    # 获取页面内容 指定网站编码
    def get_page(self, url, charcode):
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

    # 获取头条文章链接
    def touTiaoUrls(self,page):
        s = json.loads(page)
        datas = s['data']
        hasmore = s['has_more']
        for data in datas:
           if data.has_key('cell_type'):
               continue
           url = data['share_url']
           self._urls.append(url)
        if hasmore == 1:
            self._offset += 20
            url = 'http://www.toutiao.com/search_content/?offset=' + str(
                self._offset) + '&format=json&keyword=' + self._keyword + '&autoload=true&count=' + str(
                self._num) + '&cur_tab=1'
            page = self.get_page(url,'utf-8')
            self.touTiaoUrls(page)
        if hasmore == 0:
            return None

    # 获取头条标题
    def touTiaoTitle(self,page):
        pattern = re.compile('<h1 class="article-title">(.*?)</h1>')
        result = re.search(pattern,page)
        if not result:
            print '不是文章标题'
            pattern = re.compile('<h1 class="question-name">.*?</a>.*?(.*?)</h1>',re.S)
            result = re.search(pattern,page)
            if not result:
                return None
            return result.group(1).strip()
        return result.group(1).strip()

    # 获取头条内容
    def touTiaoText(self,page):
        pattern = re.compile('<div class="article-content">(.*?)</div>')
        result = re.search(pattern,page)
        if not result:
            pattern = re.compile('<div class="answer-text-full rich-text">(.*?)</div>',re.S)
            result = re.search(pattern,page)
            if not result:
                return None
            return self._contentTool.replaceNoImg(result.group(1).strip())
        content = self._contentTool.replaceNoImg(result.group(1).strip())
        p = re.compile('\n\n',re.S)
        content = '---'.join(p.split(content))
        return content

    # 获取链接标题和文章内容
    def touTiaoContent(self,urls):
        contents = []
        for url in urls:
            print u'抓取' + url
            page = self.get_page(url,'utf-8')
            # 如果没有获取到页面，则跳过
            if not page:
                continue
            title = self.touTiaoTitle(page)
            content = self.touTiaoText(page)
            if not content:
                print '没有采集到文章'
                continue
            contents.append({'title':title,'content':content,'url':url})
        return contents

    # 抓取头条
    def grapTouTiao(self):
        url = 'http://www.toutiao.com/search_content/?offset='+ str(self._offset) +'&format=json&keyword=' + self._keyword + '&autoload=true&count=' + str(self._num) + '&cur_tab=1'
        page = self.get_page(url, 'utf-8')
        self.touTiaoUrls(page)
        if not self._urls:
            print u'没有获取到内容的链接'
            exit()
        return self.touTiaoContent(self._urls)

# toutiao = TouTiao('太阳城',500)
# page = toutiao.get_page('http://www.toutiao.com/a6439166617712574721/','utf-8')
# toutiao.touTiaoText(page)