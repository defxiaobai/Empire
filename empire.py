#!/usr/local/env python
#coding:utf-8

import urllib
import urllib2
import re
import ContentTool
import Mysql
import TouTiao
import ZhiDao

class Empire(object):

    # 构造方法初始化输入 需要传入域名，网站用户名，关键词，栏目id
    def __init__(self,domian,username,classid):
        self._jiekouurl = 'http://' + domian + '/e/admin/jiekou.php'
        self._username = username
        self._classid = classid
        self._db = Mysql.tomsql()



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