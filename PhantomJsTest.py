#/usr/bin/python
#-*-coding:utf-8-*-

from selenium import webdriver
import base64
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

service_args = [
    '--proxy=http-pro.abuyun.com:9010',
    '--proxy-type=http'
    ]
authentication_token = "Basic" + base64.b64encode('H26S5KQ146UAT20P:6F50BEE835E407ED')
capa = DesiredCapabilities.PHANTOMJS
capa['phantomjs.page.customHeaders.Proxy-Authorization'] = authentication_token
browser = webdriver.PhantomJS(service_args=service_args)
browser.set_page_load_timeout(100)
browser.set_script_timeout(100)

browser.get("http://www.baidu.com")
page = browser.page_source
print page
