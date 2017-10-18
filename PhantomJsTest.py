#/usr/bin/python
#-*-coding:utf-8-*-

from selenium import webdriver
import base64
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

service_args = [
    #
    '--proxy=http-pro.abuyun.com:9010',
    '--proxy-type=http',
    '--ssl-protocol=any',
    "--web-security=no",
    # "--ssl-protocol=tlsv1",
    "--ignore-ssl-errors=yes",
    "--ignore-ssl-errors=true"


    ]
authentication_token = "Basic " + base64.b64encode('H26S5KQ146UAT20P:6F50BEE835E407ED')
capa = DesiredCapabilities.PHANTOMJS.copy()
capa['phantomjs.page.customHeaders.Proxy-Authorization'] = authentication_token
capa["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36 QIHU 360SE",

browser = webdriver.PhantomJS(desired_capabilities=capa,service_args=service_args)
browser.set_page_load_timeout(100)
browser.set_script_timeout(100)

browser.get("http://m.so.com/")
page = browser.page_source
print browser.current_url
print page
browser.quit()
