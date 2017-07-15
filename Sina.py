#/usr/bin/env python
#coding:utf-8

import urllib2
import json
import re
import os
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Sina(object):


    # 获取页面内容 指定网站编码
    def get_page(self, url):
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
            return page.read().decode('utf-8')

    def parse_datas(self,pageNo=1):
        pageUrl = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=shxw&cat_2==zqsk||=qwys||=shwx||=fz-shyf&level==1||=2&show_ext=1&show_all=1&show_num=500&tag=1&format=json&page='+ str(pageNo) +'&callback=newsloadercallback&_=1499918282956'
        print pageUrl
        page = self.get_page(pageUrl).strip()
        pattern = re.compile('newsloadercallback\((.*?)\);')
        result = re.search(pattern,page)
        titles = []
        if not result:
            print 'NONE'
        else:
            datas = result.group(1).strip()
            jsonDatas = json.loads(datas)
            news = jsonDatas['result']['data']
            for new in news:
                titles.append(new['title'])
            return titles

    # 字节bytes转化kb\m\g
    def formatSize(self,bytes):
        try:
            bytes = float(bytes)
            kb = bytes / 1024
        except:
            print("传入的字节格式不对")
            return "Error"


        return kb

    # 获取文件大小
    def getDocSize(self,path):
        try:
            size = os.path.getsize(path)
            return self.formatSize(size)
        except Exception as err:
            print(err)

    def write_datas(self):
        try:
            f = open('titles.txt', 'w')
        except IOError, e:
            print '打开文件失败', e.args[0], e.args[1]
        else:
            for n in range(1,80):
                titles = self.parse_datas(n)
                # print '\n'.join(titles)
                txtSize = int(self.getDocSize(f.name))
                print txtSize
                if txtSize >= 200:
                    try:
                        f = open('titles'+str(n)+'.txt','w')
                    except IOError,e:
                        print '创建文件失败',e.args[0],e.args[1]

                for title in titles:
                    txt = ''
                    if title == "":
                        continue
                    else:
                       tlist = list(title)
                       tlist.append('')
                       tlist.append('')
                       tlist = set(tlist)
                       # print str(tlist)
                       title = ''.join(tlist)
                    txt  += title
                    f.write(txt)
                    f.write('\r\n')

            f.close()

sina = Sina()
sina.write_datas()
