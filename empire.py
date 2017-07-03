#!/usr/local/env python
#coding:utf-8

import urllib
import urllib2
import cookielib

class Empire(object):

    # 构造方法初始化输入
    def __init__(self,domian,username):
        self._jiekouurl = 'http://' + domian + '/e/admin/jiekou.php'
        self._username = username

    # 登陆
    def postData(self):
        data = urllib.urlencode({
            'username':self._username,
            'classid':1,
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
        print resp.read()

empire = Empire('www.bayuad.com','hsmw')
empire.postData()
