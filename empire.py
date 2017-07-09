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


    def grabDatas(self):
        zhidao = ZhiDao.ZhiDao(self._keyword)
        zhidao.grabZhiDao(1,1)

        # toutiao = TouTiao.TouTiao('太阳城',500)
        # contents = toutiao.grapTouTiao()
        # print contents
        # self.Mysqldb.insertData('toutiao',contents)

    def mixedData(self):
        p = re.compile('---',re.S)
        zd = self.Mysqldb.queryData('zhidao')
        tt = self.Mysqldb.queryData('toutiao')
        for index,zdData in enumerate(zd):
            zdTitle = zdData[0]
            zdAnswer = zdData[1]
            answers = p.split(zdAnswer)
            # for answer in answers:
            #     print answer
            #     print '-----'
            if index < len(tt):
                ttTitle = tt[index][0]
                ttContent = tt[index][1]
                ttConts = p.split(ttContent)

    # 登陆
    def postData(self,title,text):
        data = urllib.urlencode({
            'username':self._username,
            'classid':self._classid,
            'title':title,
            'newstext':text,
            'pw':'123456'

        })
        #创建request
        request = urllib2.Request(self._jiekouurl,data)
        resp = urllib2.urlopen(request)
        if '成功' in resp.read():
            print '成功'

empire = Empire('www.taiyangchengyule.cn','yeqiu','郑州太阳城',3)
# empire.mixedData()
# # empire.postData()
empire.grabDatas()