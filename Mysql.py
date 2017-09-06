#!/usr/bin/env python
#-*-coding:utf-8-*-

import MySQLdb
import time

class tomsql(object):

    def __init__(self):
        try:
            self._db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='Aliexpress',db='taiyang',charset='utf8', port=3306)
            self._cursor = self._db.cursor()

        except MySQLdb.Error as e:
            print(self.getCurrentTime(),'链接数据库失败，原因%d：%s'%(e.args[0],e.args[1]))

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))


    def createTable(self,t_name):
        sql = """CREATE TABLE """+ t_name +""" (
                 id int(11) unsigned not null AUTO_INCREMENT,
                 domain  CHAR(20) NOT NULL,
                 PRIMARY KEY(id)
                )ENGINE=INNODB DEFAULT charset = UTF8;"""

        try:
            self._cursor.execute(sql)
        except MySQLdb.Error as e:
            self._db.rollback()
            if 'already exists' in e.args[1]:
                print t_name + '的表已经存在了'


    def createTableTfCf(self,t_name):
        sql = """CREATE TABLE """+ t_name +""" (
                 id int(11) unsigned not null AUTO_INCREMENT,
                 domain  CHAR(20) NOT NULL,
                 tf char(5) not null,
                 cf char(5) not null,
                 PRIMARY KEY(id)
                )ENGINE=INNODB DEFAULT charset = UTF8;"""

        try:
            self._cursor.execute(sql)
        except MySQLdb.Error as e:
            self._db.rollback()
            if 'already exists' in e.args[1]:
                print t_name + '的表已经存在了'


    def totalCount(self,table):
        sql = 'select count(*) from %s' % (table)
        try:
            self._cursor.execute(sql)
            return self._cursor.fetchone()
        except MySQLdb.Error as e:
            print(self.getCurrentTime(), '查旬数据失败，原因%d: %s' % (e.args[0], e.args[1]))

    def insertData(self,table,D_dict):
        for k,my_dict in enumerate(D_dict):
            if not my_dict:
                continue
            print my_dict
            keys = ','.join(my_dict.keys())
            if not my_dict.values():
                continue
            print my_dict.values()
            values = '","'.join(my_dict.values())
            sql = "insert into %s (%s) values (%s)" % (table,keys,'"'+values+'"')
            try:
                result = self._cursor.execute(sql)
                self._db.commit()
                print result
            except MySQLdb.Error as e:
                self._db.rollback()
                if 'key "PRIMARY"' in e.args[1]:
                    print(self.getCurrentTime(),'数据已经存在了，未插入')
                else:
                    print(self.getCurrentTime(),'插入数据失败，原因%d: %s' %(e.args[0],e.args[1]))
                exit()

    def queryData(self,table):
        sql = 'select title,content from %s' % (table)
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
            return result
        except MySQLdb.Error as e:
            print(self.getCurrentTime(), '插入数据失败，原因%d: %s' % (e.args[0], e.args[1]))

    #查询分页
    def queryDataPage(self, table,index):
        pnum = 100
        start = (index -1) * pnum
        sql = 'select domain from '+ table +' limit '+str(start) +','+ str(pnum)
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
            return result
        except MySQLdb.Error as e:
            print(self.getCurrentTime(), '插入数据失败，原因%d: %s' % (e.args[0], e.args[1]))

    def closeDb(self):
        self._db.close()
