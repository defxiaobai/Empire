# -*- coding: utf-8 -*-
#find title and href
import re
import math
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

urllib2.socket.setdefaulttimeout(30)
# 获取页面内容
def get_page(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1'}
    try:
        request = urllib2.Request(url, headers=header)
        page = urllib2.urlopen(request,timeout=30)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print '获取页面错误，错误原因：%s' % e.reason
            return None
        if hasattr(e, 'code'):
            print '获取页面错误，错误代码：%s' % e.code
            return None
    else:
        return page.read().decode('utf-8')

#查询出来搜索结果
def search(key,limit=10):
    search_url='http://www.baidu.com/s?wd=key&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391'
    search_url=search_url.replace('key',key)
    html=get_page(search_url)
    soup=BeautifulSoup(html,"html.parser")
    resultNumPattern = re.compile("<b>找到相关结果数约(.*?)个</b>")
    resultNumDiv = soup.find('div',attrs={'class':'c-span21 c-span-last'})
    re_num = resultNumPattern.findall(str(resultNumDiv))
    if not re_num:
        print '没有找到相关结果'
        exit()
    reNum = re_num[0]
    rePNum = int(math.ceil(float(reNum) / 10))
    re_dict = {}
    for x in range(1,rePNum+1):
        print x
        url = search_url + '&pn='+str((x-1) * 10)
        print url
        html = get_page(url)
        soup = BeautifulSoup(html, "html.parser")
        linkpattern = re.compile("href=\"(.+?)\"")
        r_next = soup.find('a',attrs={'class':'n'})
        if not r_next:
            print '没有下一页'
            continue
        div=soup.find('div',id='wrapper').find('div',id='wrapper_wrapper').find('div',id='container').find('div',id='content_left')
        for i in range(1,limit+1):
            a=div.find('div',attrs={'class':'result c-container '}).find('h3').find('a')
            re_link=linkpattern.findall(str(a))
            re_title=a.text
            re_dict[re_title]=re_link[0]
    for r in re_dict:
        target_url = re_dict[r]
        print target_url
        response = urllib2.urlopen(target_url)
        realurl = response.geturl()
        print(realurl)
        print '....................\n'


if __name__=='__main__':
        key='site:www.safeken.com'
        search(key)