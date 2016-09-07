# !/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'howie'

import pymysql
from config import configDic


class DbConnect(object):
    '''
    connect mysql
    '''

    def __init__(self):
        self.conn = pymysql.connect(**configDic)
        self.cursor = self.conn.cursor()

    def insertData(self, table, field, values):
        sql = "insert into %s%s values %s" % (table, "(" + field + ")", "(" + values + ")")
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        except:
            print(sql)
            self.conn.rollback()
            return False

    def __del__(self):
        self.cursor.close()
        self.conn.close()
