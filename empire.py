#!/usr/local/env python
#coding:utf-8

import urllib
import urllib2
import re

class Empire(object):

    # 构造方法初始化输入 需要传入域名，网站用户名，关键词，栏目id
    def __init__(self,domian,username,keyword,classid):
        self._jiekouurl = 'http://' + domian + '/e/admin/jiekou.php'
        self._username = username
        self._keyword = urllib.quote(keyword)
        self._classid = classid


    # 获取页面内容 指定网站编码
    def get_page(self,url,charcode):
        header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1'}
        try:
            request = urllib2.Request(url,headers=header)
            page = urllib2.urlopen(request)
        except urllib2.URLError as e:
            if hasattr(e,'reason'):
                print '获取页面错误，错误原因：%s' % e.reason
                return None
            if hasattr(e,'code'):
                print '获取页面错误，错误代码：%s' % e.code
                return None
        else:
            return page.read().decode(charcode)

    #返回百度知道的总页数
    def zhiDaoTotalPage(self,page):
        # 判断一共有多少页内容 如果包含了最后一页 则直接读取最后一页 否则下一页之前的链接数字为总的页数
        pattern = re.compile('<a class="pager-last" href="(.*?)">.*?</a>')
        result = re.search(pattern, page)
        if not result:
            print u'不存在最后一页的链接,抓取全部分页，提取总页数'
            # 匹配下一页之前的页数
            pattern = re.compile(
                '<div class="pager" alog-alias="pager">(.*?)<a class="pager-next" href=".*?">.*?</a>.*?</div>', re.S)
            result = re.search(pattern, page)
            if not result:
                print u'没有匹配到下一页之前的页数'
                return None
            else:
                page = result.group(1).strip()
                pattern = re.compile('<a href=".*">(.*?)</a>')
                items = re.findall(pattern, page)
                if not items:
                    return None
                else:
                    totalPage = items.pop().strip()
                    return totalPage
        else:
            lastUrl = 'https://zhidao.baidu.com' + result.group(1).strip()
            lastPage = self.get_page(lastUrl, 'gbk')
            pattern = re.compile('<b>(.*?)</b>')
            result = re.se(pattern, lastPage)
            if not result:
                print u'错误没有匹配到最后一页'
                return None
            else:
                totalPage = result.lastgroup.strip()
                return totalPage

    # 获取内容页的url
    def zhiDaoContentUrls(self,page):
        pattern = re.compile('<dl class="dl.*?".*?>.*?<dt.*?>.*?<a href="(.*?)".*?>.*?</dl>',re.S)
        items = re.findall(pattern,page)
        urls = []
        if not items:
            print u'没有找到对应的内容链接'
            return None
        else:
            for item in items:
                print item
                urls.append(item)
            return urls

    # 获取百度知道所有的相关url
    def zhiDaoUrls(self,page,startPage):
        totalPage = self.zhiDaoTotalPage(page)
        urls = []
        if not totalPage:
            print u'获取总页数错误'
            return None

        for n in range(int(startPage),int(totalPage) + 1):
            print '正在抓取第'+ str(n) + '页的url'
            url = 'https://zhidao.baidu.com/search?word=' + self._keyword + '&ie=utf-8&site=-1&sites=0&date=0&pn=' + str((n - 1) * 10)
            page = self.get_page(url,'gbk')
            urls.append(self.zhiDaoContentUrls(page))

        return urls

    # 百度知道标题
    def zhiDaoTitle(self,page):
        pattern = re.compile('<span class="ask-title.*?">(.*?)<img.*?>.*?</span>',re.S)
        result = re.search(pattern,page)
        if not result:
            return None
        else:
            return result.group(1).strip()


    # 百度知道问答答案
    def zhiDaoAnswer(self,page):
        pass

    # 获取内容
    def zhiDaoContent(self,urls):
        for k,v in enumerate(urls):
            print '准备抓取第'+ str(k) +'页链接的内容'
            for url in v:
                page = self.get_page(url,'gbk')
                title = self.zhiDaoTitle(page)
                print title
                exit()



    # 抓取百度知道的内容,指定第几页开始抓取
    def grabZhiDao(self,startPage = 1):
        startPage = int(startPage)
        url = 'https://zhidao.baidu.com/search?word='+ self._keyword +'&ie=utf-8&site=-1&sites=0&date=0&pn=' + str((startPage -1 ) * 10)
        print url
        page = self.get_page(url,'gbk')
        urls = self.zhiDaoUrls(page,startPage)
        if not urls:
            print u'没有获取到内容链接'
        else:
            self.zhiDaoContent(urls)



    def grabWeiBo(self):
        pass
    def grabToutiao(self):
        pass

    # 登陆
    def postData(self):
        data = urllib.urlencode({
            'username':self._username,
            'classid':self._classid,
            'title':'this is a title',
            'newstext':'this a news text',
            'pw':'123456',
            'keyboard':'keyword1,keyword2',
            'filename':'file1',
            'infotags':'tag1,tag2'

        })
        #创建request
        request = urllib2.Request(self._jiekouurl,data)
        resp = urllib2.urlopen(request)
        if '成功' in resp.read():
            print '成功'

empire = Empire('www.bayuad.com','hsmw','北京太阳城',1)
# empire.postData()
empire.grabZhiDao()