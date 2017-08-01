#/usr/bin/env python
#coding:utf-8
import urllib2
import urllib
import re
import ContentTool
import Mysql


class ZhiDao(object):

    def __init__(self,keyword):
        self._contentTool = ContentTool.ContentTool()
        self._keyword = urllib.quote(keyword)
        self.Mysqldb = Mysql.tomsql()

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
            return page.read().decode(charcode,'ignore').encode('utf-8')

    #通过lastpage获取总的totalPages
    def last_page(self,lastUrl):
        lastPage = self.get_page(lastUrl, 'gbk')
        pattern = re.compile('<b>(.*?)</b>')
        result = re.search(pattern, lastPage)
        if not result:
            print u'错误没有匹配到最后一页'
            return None
        else:
            totalPage = result.group(1).strip()
            return totalPage

    # 返回百度知道的总页数
    def zhiDaoTotalPage(self, page):
        # 判断一共有多少页内容 如果包含了最后一页 则直接读取最后一页 否则下一页之前的链接数字为总的页数
        lastPattern = re.compile('<a class="pager-last" href="(.*?)">.*?</a>')
        result = re.search(lastPattern, page)
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
                    preNum = items.pop().strip()
                    if int(preNum) > 9:
                        url = 'https://zhidao.baidu.com/search?word=' + self._keyword + '&ie=utf-8&site=-1&sites=0&date=0&pn=10'
                        page = self.get_page(url,'gbk')

                        lastPattern = re.compile('<a class="pager-last" href="(.*?)">.*?</a>')
                        result = re.search(lastPattern, page)
                        if not result:
                            print '没有获取尾页'
                            totalPage = preNum
                            return totalPage
                        else:
                            lastUrl = 'https://zhidao.baidu.com'+result.group(1).strip()
                            return self.last_page(lastUrl)

        else:
            lastUrl = 'https://zhidao.baidu.com' + result.group(1).strip()
            totalPage = self.last_page(lastUrl)
            return totalPage
    # 获取内容页的url
    def zhiDaoContentUrls(self, page):
        pattern = re.compile('<dl class="dl.*?".*?>.*?<dt.*?>.*?<a href="(.*?)".*?>.*?</dl>', re.S)
        items = re.findall(pattern, page)
        f = open('zdurls.txt', 'a')
        if not items:
            print u'没有找到对应的内容链接'
            return None
        else:
            for item in items:
                print '写入url：'+ item
                f.write(item)
                f.write('\n')
            f.close()


    # 获取百度知道所有的相关url
    def zhiDaoUrls(self, page, startPage):
        totalPage = self.zhiDaoTotalPage(page)
        print '一共多少页面：'+ totalPage
        if not totalPage:
            print u'获取总页数错误'
            return None

        for n in range(int(startPage), int(totalPage) + 1):
            print '正在抓取第' + str(n) + '页的url'
            url = 'https://zhidao.baidu.com/search?word=' + self._keyword + '&ie=utf-8&site=-1&sites=0&date=0&pn=' + str(
                (n - 1) * 10)
            page = self.get_page(url, 'gbk')
            self.zhiDaoContentUrls(page)


    # 百度知道标题
    def zhiDaoTitle(self, page):
        pattern = re.compile('<span class="ask-title.*?">(.*?)</span>')
        result = re.search(pattern, page)
        if not result:
            return None
        else:
            return result.group(1).strip()

    # 百度知道问答答案
    def zhiDaoAnswer(self, page):
        pattern = re.compile('<div class="line content">.*?(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        content = ''
        if not items:
            print u'没有匹配到内容'
            return None
        else:
            for item in items:
                content += self._contentTool.replace(item) + '---'
            return content

    # 获取内容 标题和问答内容
    def zhiDaoContent(self, urls,startPage):
        contents = []
        i= 0
        for url in urls:
            i = i + 1
            print '抓取第' + str(i) + '条链接'
            page = self.get_page(url, 'gbk')
            if not page:
                continue
            page = self._contentTool.pageReplace(page)
            title = self.zhiDaoTitle(page)
            content = self.zhiDaoAnswer(page)
            if not content:
                continue
            if not title:
                continue
            contents.append({'title':title,'content':content,'url':url})
            print content
            if len(contents) == 10 or i == len(urls) :
                self.Mysqldb.insertData('zhidao',contents)
                print '插入链接  的数据'
                contents = []

    #读取文件
    def readUrls(self):
        try:
            f = open('zdurls.txt','r')
            urls = f.readlines()
        except IOError as e:
            print '文件读取错误，错误原因',e.args[0],e.args[1]
        else:
            return urls
    # 抓取百度知道的内容,指定第几页开始抓取
    def grabZhiDao(self,startPage = 1,fromText = 0):
        startPage = int(startPage)
        url = 'https://zhidao.baidu.com/search?word='+ self._keyword +'&ie=utf-8&site=-1&sites=0&date=0&pn=' + str((startPage -1 ) * 10)
        page = self.get_page(url,'gbk')
        if fromText == 1:
            urls = self.readUrls()
        else:
            urls = self.zhiDaoUrls(page,startPage)
        if not urls:
            print u'没有获取到内容链接'
            return None
        else:
            self.zhiDaoContent(urls,startPage)
