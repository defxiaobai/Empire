#!/usr/local/env python
#coding:utf-8

import urllib
import urllib2
import re
import ContentTool
import Mysql
import TouTiao
import ZhiDao
from itertools import chain
import sys
import math
import random
reload(sys)
sys.setdefaultencoding('utf-8')
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

class Empire(object):

    # 构造方法初始化输入 需要传入域名，网站用户名，关键词，栏目id
    def __init__(self,domian,username,keyword,classid):
        self._jiekouurl = 'http://' + domian + '/e/admin/jiekou.php'
        self._username = username
        self._keyword = keyword
        self._classid = classid
        self.Mysqldb = Mysql.tomsql()

    def grabDatas(self):
        zhidao = ZhiDao.ZhiDao(self._keyword)
        zhidao.grabZhiDao(1,1)

        # toutiao = TouTiao.TouTiao('天津太阳城',500,20)
        # toutiao.grapTouTiao()
        # print contents
        # self.Mysqldb.insertData('toutiao',contents)

    def mixedData(self):
        p = re.compile('---',re.S)
        pk = re.compile(u'太阳城')
        zd = self.Mysqldb.queryData('zhidao')
        tt = self.Mysqldb.queryData('toutiao')
        for index,zdData in enumerate(zd):
            zdTitle = zdData[0]
            zdAnswer = zdData[1]
            answers = p.split(zdAnswer)
            # for x in range(0,len(tt)):
            #     ttContent = tt[x][1]
            #     contents = p.split(ttContent)
            #     randInt = random.randint(0,len(contents)-1)
            #     content = contents[randInt]
            #     answers.append(content)
            # random.shuffle(answers)
            mixdeanswers = []
            for answer in answers:
                answer = re.sub(pk, u"<strong>太阳城</strong>", answer)
                answer = '<p>'+answer+'</p>'
                print answer
                mixdeanswers.append(answer)

            self.postData(zdTitle,''.join(mixdeanswers))


    # 内容发布
    def postData(self,title,text):
        data = urllib.urlencode({
            'username':self._username,
            'classid':self._classid,
            'title':title,
            'newstext':text,
            'keyboard':title,
            'infotags':'太阳城娱乐,天津太阳城',
            'pw':'123456'


        })
        #创建request
        request = urllib2.Request(self._jiekouurl,data)
        resp = urllib2.urlopen(request)
        if '成功' in resp.read():
            print '成功'

empire = Empire('www.taiyangchengyule.cn','yeqiu','天津太阳城',3)
# empire.grabDatas()
# # empire.postData()
# empire.grabDatas()
empire.mixedData()