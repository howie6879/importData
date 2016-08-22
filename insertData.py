#!/usr/bin/env python
# -*-coding:utf-8-*-
__author__ = 'howie'

import pandas as pd
import os
import logging
from prettytable import PrettyTable
from db import DbConnect

FILE = os.getcwd()


class insertData(object):
    """
    处理获取的公司数据 csv xls
    标题部分需对应mysql表中列名
    """

    def __init__(self, **kwargs):
        self.path = os.path.join(os.getcwd(), kwargs['<dir>'])
        self.db_table = kwargs['<db>']
        styleDic = {
            "-c": "csv",
            "-x": "xls",
            "-j": "json"
        }
        allStyle = [styleDic[style] for style in styleDic.keys() if kwargs[style]]
        self.db = DbConnect()
        print("正在检测%s目录下文件..." % kwargs['<dir>'])
        self.judge(self.verFile(allStyle))

    def judge(self, allFile):
        """
        判断文件并存储进数据库
        :param allFile: list 全部文件名
        :return:
        """
        order = input("是否继续导入数据(y/n):")
        if order.lower() == "y":
            for file in allFile:
                style = os.path.splitext(file)[1]
                print("正在导入 %s..." % file)
                if 'csv' in style:
                    self.saveCsv(file)
                elif 'xls' in style:
                    self.saveExcel(file)
                else:
                    self.saveJson(file)
        else:
            exit()

    def saveCsv(self, csvFile):
        df = pd.read_csv(csvFile, encoding='utf-8', error_bad_lines=False)
        self.saveData(df)

    def saveExcel(self, excelFile):
        df = pd.read_excel(excelFile,encoding="utf-8")
        self.saveData(df)

    def saveJson(self, jsonFile):
        pass

    def saveData(self,df):
        success, fail = 0, 0
        column = ','.join(list(map(lambda x: x.lower(), df.keys())))
        for num in range(len(df.values)):
            row = ','.join(list(map(lambda x: self.db.conn.escape(str(x)), df.values[num])))
            insert = self.db.insertData(table=self.db_table, field=column.strip(), values=row)
            if insert:
                # print("第%s行插入成功" % (num+1))
                success += 1
            else:
                print("第%s行插入失败" % (num + 1))
                fail += 1
        table = PrettyTable(["log"])
        table.add_row(["%s条数据插入成功" % success])
        table.add_row(["%s条数据插入失败" % fail])
        table.add_row(["共 %s 条数据" % (success + fail)])
        print(table)

    def verFile(self, allStyle):
        """
        验证该目录下是否存在对应格式文件
        :param style: 插入数据库文件格式
        :return: 存在True 反之False
        """
        allFile = []
        table = PrettyTable(["ID", "FILE"])
        for style in allStyle:
            targetFile = [os.path.join(self.path, eachFile) for eachFile in os.listdir(self.path) if
                          style in os.path.splitext(eachFile)[1]]
            if not targetFile:
                logging.warning(style + "文件不存在...")
                exit()
            else:
                allFile += targetFile
        if allFile:
            num = 0
            for file in allFile:
                num += 1
                table.add_row([num, file])
            print(table)
        return allFile


