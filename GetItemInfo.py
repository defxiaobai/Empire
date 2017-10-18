#/usr/bin/env python
#-*-coding:utf-8-*-

from majesticapi.APIService import *
from datetime import datetime
import Mysql
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if (__name__ == '__main__'):
    endpoint = 'https://api.majestic.com/api_command'
    app_api_key = '9D9562C648C96B404C028123D4ADB91E'
    tbname = 'domains' + datetime.now().strftime('%Y%m%d')
    mysql = Mysql.tomsql()
    mysql.createTableTfCf(tbname)

    itmes = []
    try:
        fp = open('jj.txt','r')
        items = fp.readlines()
        fp.close()
    except IOError as e:
        print 'error:%s' % e.args[1]
        exit()
    # create a hash from the resulting array with the key being
    # 'item0 => first item to query, item1 => second item to query' etc
    num = int(math.ceil(float(len(items)) / 1000))

    for x in range(0,num):
        end = (x + 1) * 1000
        start = x * 1000
        peritems = items[start:end]
        parameters = {}
        for index, item in enumerate(peritems):
            parameters['item' + str(index)] = item

        # add the total number of items to the hash with the key being 'items'
        parameters['items'] = len(items)

        parameters['datasource'] = 'fresh'

        api_service = APIService(app_api_key, endpoint)
        response = api_service.execute_command('GetIndexItemInfo', parameters)

        # check the response code
        if (response.is_ok()):
            # print the results table
            results = response.get_table_for_name('Results')
            print results.rows

            r_dict = []
            for row in results.rows:
                item = row['Item']
                cf = row['CitationFlow']
                tf = row['TrustFlow']
                r_dict.append({'domain':item,'tf':tf,'cf':cf})
            mysql.insertData(tbname,r_dict)
                    # # print row['']
                    # print '\n<' + str(item) + '>'
                    # for key in sorted(row.keys()):
                    #     if ('Item' != key):
                    #         value = row[key]
                    #         print ' ' + str(key) + ' ... ' + str(value)
        else:
            print ('\nERROR MESSAGE:')
            print (str(response.get_error_message()))

            print ('\n\n***********************************************************'
                   + '*****************')

            print ('\nDebugging Info:')
            print ('\n  Endpoint: \t' + endpoint)
            print ('  API Key: \t' + app_api_key)

            if ('https://api.majestic.com/api_command' == endpoint):
                print ('\n  Is this API Key valid for this Endpoint?')

                print ('\n  This program is hard-wired to the Enterprise API.')

                print ('\n  If you do not have access to the Enterprise API, '
                       + 'change the endpoint to: \n  https://developer.majestic.com/api_command.')

            print ('\n***********************************************************'
                   + '*****************')