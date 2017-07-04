#!/usr/local/env python
#coding:utf-8

import urllib
import urllib2
import cookielib

class Empire(object):

    # 构造方法初始化输入 需要传入域名，网站用户名，关键词，栏目id
    def __init__(self,domian,username,keyword,classid):
        self._jiekouurl = 'http://' + domian + '/e/admin/jiekou.php'
        self._username = username
        self._keyword = keyword
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

    # 获取百度知道所有的相关url
    def zhiDaoUrls(self,page):
        
        pass

    # 抓取百度知道的内容,指定第几页开始抓取
    def grabZhiDao(self,pageNo):
        word = urllib.quote(self._keyword)
        url = 'https://zhidao.baidu.com/search?word='+ word +'&ie=utf-8&site=-1&sites=0&date=0&pn=' + (pageNo -1 ) * 10
        page = self.get_page(url,'gbk')


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