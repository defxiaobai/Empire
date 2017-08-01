#/usr/bin/env python
#coding:utf-8
import urllib2
import urllib
import re
import TentTool
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Ten(object):

    def __init__(self,domain,username,classid):
        self.tentTool = TentTool.TentTool()
        self._jiekouurl = 'http://' + domain + '/e/admin/jiekou.php'
        self._username = username
        self._classid = classid


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

    def get_urls(self,page):
        prefix = 'https://guanjia.qq.com'
        urls = []
        pattern = re.compile('<div class="news_list">.*?<ul>(.*?)</ul>.*?</div>',re.S)
        result = re.search(pattern,page)
        if not result:
            print '没有匹配到对应的ul'
            return None
        pattern = re.compile('<a href="(.*?)".*?</a>',re.S)
        items = re.findall(pattern,result.group(1).strip())
        if not items:
            print '没有匹配到链接'
            return None
        for url in items:
            url = prefix + url
            urls.append(url)
        return urls

    def get_contents(self,urls):
        contents = []
        for url in urls:
            print url
            page = self.get_page(url,'utf-8')
            pattern = re.compile('<h1>(.*?)</h1>')
            result = re.search(pattern,page)
            if not result:
                print '没有匹配到title'
                title = ''
            title = result.group(1).strip()
            pattern = re.compile('<span id="desc">(.*?)</span>')
            result = re.search(pattern,page)
            if not result:
                print '没有匹配到摘要'
                smalltext = ''
            smalltext = result.group(1).strip()
            pattern = re.compile('<div class="news_content">.*?(.*?)<div class="news_bar">',re.S)
            result = re.search(pattern,page)
            if not result:
                print '没有匹配到内容'
                newstext = ''
            newstext = result.group(1).strip()
            newstext = self.tentTool.remove_tags(newstext)
            pattern = re.compile(' ')
            titls = re.split(pattern,title)
            if len(titls) >= 2:
                keyboard = titls[1]
            else:
                keyboard = titls[0]

            contents.append({'title':title,'smalltext':smalltext,'newstext':newstext,'keyboard':keyboard})
        return contents

    # 登陆
    def postData(self,title,smalltext,text,keyboard):
        data = urllib.urlencode({
            'username': self._username,
            'classid': self._classid,
            'title': title,
            'keyboard':keyboard,
            'smalltext':smalltext,
            'infotags':'腾讯电脑管家电脑版,最新电脑管家官方下载',
            'newstext': text,
            'pw': '123456'

        })
        # 创建request
        request = urllib2.Request(self._jiekouurl, data)
        resp = urllib2.urlopen(request)
        if '成功' in resp.read():
            print '成功'


    def grap_data(self,startNo,endNo):
        for x in range(startNo,endNo+1):
            if x == 1:
                url = 'https://guanjia.qq.com/news/n3/index.html'
            else:
                url = 'https://guanjia.qq.com/news/n3/list_3_'+str(x)+'.html'
            print url
            page = self.get_page(url,'utf-8')
            urls = self.get_urls(page)
            contents = self.get_contents(urls)
            for content in contents:
                print content['title'],content['smalltext'],content['newstext'],content['keyboard']
                print '------------'
                self.postData(content['title'],content['smalltext'],content['newstext'],content['keyboard'])

# 指定域名，用户名，栏目id
ten = Ten('www.bayuad.com','hsmw',2)
ten.grap_data(2,10)