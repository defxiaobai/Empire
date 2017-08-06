#!/usr/bin/env python
#coding:utf-8
import re

class TentTool(object):
    divPattern = re.compile('<div.*?>|</div>')
    pPattern = re.compile('<p.*?>')
    spanPattern = re.compile('<span.*?>|</span>')
    h1Pattern = re.compile('<h1.*?>')
    figurePattern = re.compile('<figure.*?>|</figure>')
    wordPattern = re.compile(u'彩票')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    figcaptionPattern = re.compile('<figcaption.*?>|</figcaption>')
    def remove_tags(self,content):
        content = re.sub(self.divPattern,'',content)
        content = re.sub(self.pPattern,'<p>',content)
        content = re.sub(self.spanPattern,'',content)
        content = re.sub(self.h1Pattern,'<h1>',content)
        content = re.sub(self.figurePattern,'',content)
        content = re.sub(self.figcaptionPattern,'',content)
        content = re.sub(self.removeAddr,'',content)
        #匹配替换两个
        content = re.sub(self.wordPattern, '<a href="http://www.jdms8.com">特区彩票七星彩论坛</a>', content,2)
        return content



