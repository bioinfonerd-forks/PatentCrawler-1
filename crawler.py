#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <blackhatdwh@gmail.com>
#
# Distributed under terms of the MIT license.

import subprocess
import json
import pymysql
from time import sleep
import sys
from json.decoder import JSONDecodeError
from utils import clean_html, notify, get_index, commit_progress, save_result
from login import login

WEE_SID = ""
JSESSIONID = ""

def update_cookies():
    global WEE_SID
    global JSESSIONID
    cookies = login()
    WEE_SID = cookies['WEE_SID']
    JSESSIONID = cookies['JSESSIONID']

'''
try:
    conn = pymysql.connect(host='localhost', database='Patent', user='root', password='wohenhaoqi', charset='utf8mb4', autocommit=True)
    cur = conn.cursor()
except:
    print("fail to connect to mysql!")
    sys.exit()
'''

index = get_index()
outer_fail_time = 0
max_fail_time = 3

update_cookies()

for idx in index:
    i = 0
    while i != 100:
        if outer_fail_time > max_fail_time:
            notify('翻页循环处挂掉了！')
            sys.exit(1)
        commit_progress(idx, i)

        command = "curl -s 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showSearchResult-startWa.shtml' -H 'Pragma: no-cache' -H 'Origin: http://www.pss-system.gov.cn' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: WEE_SID=" + WEE_SID + "; IS_LOGIN=true; avoid_declare=declare_pass; JSESSIONID=" + JSESSIONID + "' -H 'Connection: keep-alive' -H 'Referer: http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showNavigationClassifyNum-showBasicClassifyNumPageByIPC.shtml?params=D7B3D1618C9AC685055FF6612F62529676324C8B6E7F921902B2C40318E0E7BB' -H 'DNT: 1' --data $'resultPagination.limit=10&resultPagination.sumLimit=10&resultPagination.start=" + str(i * 10) + "&resultPagination.totalCount=3968603&searchCondition.sortFields=-APD%2C%2BPD&searchCondition.searchType=Sino_foreign&searchCondition.originalLanguage=&searchCondition.extendInfo%5B\'MODE\'%5D=MODE_IPC&searchCondition.extendInfo%5B\'STRATEGY\'%5D=&searchCondition.searchExp=IPC%E5%88%86%E7%B1%BB%E5%8F%B7%3D(" + idx + ")&searchCondition.executableSearchExp=VDB%3A(ICST%3D\'" + idx + "\')&searchCondition.dbId=&searchCondition.literatureSF=IPC%E5%88%86%E7%B1%BB%E5%8F%B7%3D(" + idx + ")&searchCondition.targetLanguage=&searchCondition.resultMode=SEARCH_MODE&searchCondition.strategy=&searchCondition.searchKeywords=%5BA%5D%5B+%5D%7B0%2C%7D%5B0%5D%5B+%5D%7B0%2C%7D%5B1%5D%5B+%5D%7B0%2C%7D' --compressed"
        result = subprocess.getoutput(command)
        try:
            result = json.loads(result)
        except JSONDecodeError as ex:
            print(ex)
            print('-------------list-----------')
            print(result)
            update_cookies()
            outer_fail_time += 1
            sleep(outer_fail_time ** 2)
            continue
        try:
            result = result['searchResultDTO']['searchResultRecord']
        except KeyError as ex:
            print(ex)
            print('-------------list--key---------')
            outer_fail_time += 1
            sleep(outer_fail_time ** 2)
            continue
        for r in result:
            pub_state = r['lawStatus']  # 公开状态
    
            field = r['fieldMap']
    
            title = field['TIVIEW']     # 专利名
            app_num = field['APO']      # 申请号
            app_date = field['APD']     # 申请日
            pub_num = field['PN']       # 公开号
            pub_date = field['PD']      # 公开日
            IPC = field['IC']           # IPC分类号
            app_person = field['PAVIEW']        # 申请人
            invent_person = field['INVIEW']     # 发明人
            agent_person = field['AGT']         # 代理人
            agent_inst = field['AGY']           # 代理机构
            app_addr = field['AA']      # 申请地址
            similar = field['FNUM']     # 同族
            reference = field['PNUM']   # 引证
            cited = field['CPNUM']      # 被引
            priority_num = field['PR']  # 优先权号
            priority_date = field['PRD']    # 优先权日
            zip_code = field['AZ']      # 邮编
    
            ID = field['ID']
            VID = field['VID']
    
            not_finished = True
            inner_fail_time = 0
            while not_finished:
                if inner_fail_time > max_fail_time:
                    notify('摘要获取挂掉了！')
                    sys.exit(1)
                abstract_command = "curl -s 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/viewAbstractInfo0529-viewAbstractInfo.shtml' -H 'Pragma: no-cache' -H 'Origin: http://www.pss-system.gov.cn' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: IS_LOGIN=true; WEE_SID=" + WEE_SID + "; avoid_declare=declare_pass; JSESSIONID=" + JSESSIONID + "' -H 'Connection: keep-alive' -H 'Referer: http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml' -H 'DNT: 1' --data 'nrdAn=" + VID + "&cid=" + ID + "&sid=" + ID + "' --compressed"
                abstract_result = subprocess.getoutput(abstract_command)
                try:
                    abstract_result = json.loads(abstract_result)
                except JSONDecodeError as ex:
                    print(ex)
                    print('-----------abs--------')
                    print(abstract_result)
                    update_cookies()
                    inner_fail_time += 1
                    sleep(inner_fail_time ** 2)
                    continue
    
                try:
                    abstract = abstract_result['abstractInfoDTO']['abIndexList'][0]['value']        # 摘要
                    abstract = clean_html(abstract)
                    is_CPC = abstract_result['abstractInfoDTO']['abstractItemList'][11]['indexCode']    # CPC
                    if is_CPC == 'CPC':
                        CPC = abstract_result['abstractInfoDTO']['abstractItemList'][11]['value']
                    else:
                        for item in abstract_result['abstractInfoDTO']['abstractItemList']:
                            if item['indexCode'] == 'CPC':
                                CPC = item['value']

                    #figure_id = abstract_result['abstractInfoDTO']['figureRid']
                except KeyError as ex:
                    print(ex)
                    print('---------abs--key-------')
                    inner_fail_time += 1
                    sleep(inner_fail_time ** 2)
                    continue
                '''
                if figure_id != None:
                    figure_command = "curl -s 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/retrieveUrls.shtml' -H 'Pragma: no-cache' -H 'Origin: http://www.pss-system.gov.cn' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: IS_LOGIN=true; WEE_SID=" + WEE_SID + "; avoid_declare=declare_pass; JSESSIONID=" + JSESSIONID + "' -H 'Connection: keep-alive' -H 'Referer: http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml' -H 'DNT: 1' --data '&figureUrl=" + str(figure_id) + "&rids[0]= " + str(figure_id) + "' --compressed"
                    figure_url = subprocess.getoutput(figure_command)
                    try:
                        figure_url = json.loads(figure_url)['figureUrls'][0]
                    except JSONDecodeError as ex:
                        print(ex)
                        print('------------figure----------')
                        print(figure_url)
                        update_cookies()
                        continue
                    except KeyError as ex:
                        print(ex)
                        print('------------figure-key---------')
                        print(figure_url)
                        continue
    
                    figure_url = "http://www.pss-system.gov.cn/sipopublicsearch" + figure_url       # 摘要图片url
                    download_figure_command = "curl -s '" + figure_url + "' -H 'Pragma: no-cache' -H 'DNT: 1' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Accept: image/webp,image/apng,image/*,*/*;q=0.8' -H 'Referer: http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml' -H 'Cookie: avoid_declare=declare_pass; JSESSIONID=" + JSESSIONID + "' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > %s.jpg" % app_num
                    subprocess.getoutput(download_figure_command)
                else:
                    pass
                '''
    
                content_command = "curl -s 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showFullText0529-viewFullText.shtml' -H 'Pragma: no-cache' -H 'Origin: http://www.pss-system.gov.cn' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Cache-Control: no-cache' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: IS_LOGIN=true; WEE_SID=" + WEE_SID + "; avoid_declare=declare_pass; JSESSIONID=" + JSESSIONID + "' -H 'Connection: keep-alive' -H 'Referer: http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showViewList-jumpToView.shtml' -H 'DNT: 1' --data 'nrdAn=" + VID + "&cid=" + ID + "&sid=" + ID + "' --compressed"
                content_result = subprocess.getoutput(content_command)
                try:
                    content = json.loads(content_result)['fullTextDTO']['literaInfohtml']      # 全文
                    content = clean_html(content)
                except JSONDecodeError as ex:
                    print(ex)
                    print('--------content---------')
                    print(content)
                    update_cookies()
                    inner_fail_time += 1
                    sleep(inner_fail_time ** 2)
                    continue
                except KeyError as ex:
                    print(ex)
                    print('--------content---------')
                    print(content)
                    inner_fail_time += 1
                    sleep(inner_fail_time ** 2)
                    continue
    
                #print('INSERT INTO Patent VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % ('A', title, app_num, app_date, pub_num, pub_date, IPC, app_person, invent_person, agent_person, agent_inst, priority_num, priority_date, app_addr, abstract, content, pub_state, similar, reference, cited))
                #cur.execute('INSERT INTO Patent VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");' % ('A', title, app_num, app_date, pub_num, pub_date, IPC, app_person, invent_person, agent_person, agent_inst, priority_num, priority_date, app_addr, abstract, content, pub_state, similar, reference, cited))
                #cur.commit()
                final_result = {
			'apply_number': app_num,
			'apply_date': app_date,
			'public_number': pub_num,
			'patent_name': title,
			'patent_author': invent_person,
			'ipc_number': IPC,
			'priority_number': priority_num,
			'abstract': abstract,
			'introduction': content,
			'public_date': pub_date,
			'priority_date': priority_date,
			'apply_address': app_addr,
			'apply_mail': zip_code,
			'cpc_number': CPC,
                        }
                final_result_json = json.dumps(final_result)
                save_result(idx, ID, final_result_json)
                not_finished = False
                outer_fail_time = 0
                inner_fail_time = 0
    
        i += 1
