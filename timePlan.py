#/usr/bin/env python
#coding:utf-8
import time
import sys
import urllib2
#定时任务来审核

def autoCheck():

    while True:
        try:
            page = urllib2.urlopen('http://www.taiyangchengyule.cn/e/autocheck/check.php')
        except urllib2.URLError,e:
            if hasattr(e,'reason'):
                print '链接打开错误原因: ' + e.reason
            if hasattr(e,'code'):
                print '链接打开错误代码：'+ e.code
        else:
            print page.read()
            
        time.sleep(1800)

autoCheck()