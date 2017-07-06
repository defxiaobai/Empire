#!/usr/bin/env python
#-*-coding:utf-8-*-

import MySQLdb
import time
class tomsql(object):

    def __init__(self):
        try:
            self._db = MySQLdb.connect(host='127.0.0.1',user='root',passwd='Aliexpress',db='taiyang',charset='utf8', port=3306)
            self._cursor = self._db.cursor()
            print self._cursor
        except MySQLdb.Error as e:
            print(self.getCurrentTime(),'链接数据库失败，原因%d：%s'%(e.args[0],e.args[1]))

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    def insertData(self,table,D_dict):
        for k,my_dict in enumerate(D_dict):
            if not my_dict:
                continue
            keys = ','.join(my_dict.keys())
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

    def queryData(self,table):
        sql = 'select title,content from %s' % (table)
        try:
            self._cursor.execute(sql)
            result = self._cursor.fetchall()
            return result
        except MySQLdb.Error as e:
            print(self.getCurrentTime(), '插入数据失败，原因%d: %s' % (e.args[0], e.args[1]))


    def closeDb(self):
        self._db.close()
