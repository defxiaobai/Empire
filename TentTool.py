#!/usr/bin/env python
#coding:utf-8
import re

class TentTool(object):
    divPattern = re.compile('<div.*?>|</div>')
    pPattern = re.compile('<p.*>')
    spanPattern = re.compile('<span.*?>|</span>')
    h1Pattern = re.compile('<h1.*?>')
    imgPattern = re.compile('<img.*?src="(.*?)".*?>')

    def remove_tags(self,content):
        content = re.sub(self.divPattern,'',content)
        content = re.sub(self.pPattern,'<p>',content)
        content = re.sub(self.spanPattern,'',content)
        content = re.sub(self.h1Pattern,'<h1>',content)
        content = re.sub(self.imgPattern,'<img src="https://guanjia.qq.com\g<1>">',content)
        return content



