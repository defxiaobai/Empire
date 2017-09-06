#/usr/bin/env python
#-*-coding:utf-8-*-


import requests
import threadpool
import re
import time
import Mysql
from threading import Lock
from datetime import datetime
lock = Lock()


tbname = 'domains' + datetime.now().strftime('%Y%m%d')

mysql = Mysql.tomsql()
mysql.createTable(tbname)


def grap_domains(pagenum):
    lock.acquire()
    print pagenum
    insertDatas = []
    url = 'http://www.juming.com/6/index.htm?cha=1&page='+str(pagenum)+'&scsj=yi&ymcd_1=1&ymcd_2=7&ymhz=com,org,cn'
    print url
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    jmsession = requests.session()
    resp = jmsession.get(url,cookies = cookies,headers=headers).text
    pattern = re.compile('<input value="(.*?)".*?type="checkbox">',re.S)
    items = re.findall(pattern,resp)
    if not items:
        print '没有匹配到列表'
    else:
        for item in items:
            insertDatas.append({'domain':item})
        mysql.insertData(tbname,insertDatas)
    lock.release()


f=open(r'juming.txt','r')#打开所保存的cookies内容文件
cookies={}#初始化cookies字典变量
for line in f.read().split(';'):   #按照字符：进行划分读取
    #其设置为1就会把字符串拆分成2份
    name,value=line.strip().split('=',1)
    cookies[name]=value  #为字典cookies添加内容
f.close()


l = [x for x in range(358,483)]


pool = threadpool.ThreadPool(5)
rqs = threadpool.makeRequests(grap_domains,l)

[pool.putRequest(req) for req in rqs]
pool.wait()
pool.dismissWorkers(5,do_join=True)
