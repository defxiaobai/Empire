#!/usr/bin/env python
#coding:utf-8
import re

class ContentTool(object):
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 去除iframe
    removeIframe = re.compile('<iframe.*?>|</iframe>')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将div里的内容全部替换
    replaceDiv = re.compile('<div>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    # 去除iframe
    def pageReplace(self,x):
        x = re.sub(self.removeIframe, "", x)
        return x
    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        # x = re.sub(self.removeIframe,"",x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()
    # 不替换img 保留img
    def replaceNoImg(self,x):
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        # strip()将前后多余内容删除
        return x.strip()