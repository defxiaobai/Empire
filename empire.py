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
reload(sys)
sys.setdefaultencoding('utf-8')

class Empire(object):

    # 构造方法初始化输入 需要传入域名，网站用户名，关键词，栏目id
    def __init__(self,domian,username,keyword,classid):
        self._jiekouurl = 'http://' + domian + '/e/admin/jiekou.php'
        self._username = username
        self._keyword = keyword
        self._classid = classid
        self.Mysqldb = Mysql.tomsql()

    def grabDatas(self):
        # zhidao = ZhiDao.ZhiDao(self._keyword)
        # contents = zhidao.grabZhiDao(2)
        # self.Mysqldb.insertData('zhidao',contents)
        toutiao = TouTiao.TouTiao('太阳城',500)
        contents = toutiao.grapTouTiao()
        print contents
        self.Mysqldb.insertData('toutiao',contents)

    def mixedData(self):
        zd = self.Mysqldb.queryData('zhidao')
        tt = self.Mysqldb.queryData('toutiao')
        for index,zddata in enumerate(zd):
            if index < len(tt):
               ttile = ''
               tcontents = []
               title = tt[index][0]
               content = tt[index][1]
               if u'，' in title:
                   ttile = title.split(u'，')[0]
               elif ' ' in title:
                   ttile = title.split(' ')[0]
               else:
                   ttile = title
               conts = content.split('\n')
               num = len(conts) // 6
               if num == 0:
                   tcontents.append(content)

               for x in range(0,num):
                  tconts = []
                  if(x+1)*6 > len(conts):
                      last = len(conts)
                  else:
                      last = (x+1) * 6

                  for idx in range(x * 6,last):
                    cont = conts[idx]
                    tconts.append(cont)
                  tcontents.append(''.join(tconts))

            else:
                ttile = ''
                tcontents = []
            mixtitle = ttile + ' ' +zddata[0]
            zcontents = zddata[1].split('---')
            if not tcontents:
                mixcontent = '\n'.join(zcontents)
            else:
                mixcontents = list(chain(*zip(zcontents, tcontents)))
                mixcontent = '\n'.join(mixcontents)
            print '标题：\n'
            print mixtitle
            print '内容：\n'
            print mixcontent
            self.postData(mixtitle,mixcontent)



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

empire = Empire('www.taiyangchengyule.cn','yeqiu','北京太阳城',3)
empire.mixedData()
# empire.postData()
# empire.grabDatas()