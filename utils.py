#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 weihao <blackhatdwh@gmail.com>
#
# Distributed under terms of the MIT license.
import re
import os
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def notify(content):
    host_server = 'smtp.zju.edu.cn'
    sender_qq = 'dwh@zju.edu.cn'
    pwd = '007dwhfrms'
    sender_qq_mail = 'dwh@zju.edu.cn'
    receiver = '729918410@qq.com'
    
    mail_content = content
    mail_title = '爬虫挂掉了'
    
    smtp = SMTP(host_server, 25)
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)
    
    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

def get_index():
    return [
        'A01', 
        'A21',
        'A22',
        'A23',
        'A24',
        'A41',
        'A42',
        'A43',
        'A44',
        'A45',
        'A46',
        'A47',
        'A61',
        'A62',
        'A63',
        'A99',
        'B01',
        'B02',
        'B03',
        'B04',
        'B05',
        'B06',
        'B07',
        'B08',
        'B09',
        'B21',
        'B22',
        'B23',
        'B24',
        'B25',
        'B26',
        'B27',
        'B28',
        'B29',
        'B30',
        'B31',
        'B32',
        'B33',
        'B41',
        'B42',
        'B43',
        'B44',
        'B60',
        'B61',
        'B62',
        'B63',
        'B64',
        'B65',
        'B66',
        'B67',
        'B68',
        'B81',
        'B82',
        'B99',
        'C01',
        'C02',
        'C03',
        'C04',
        'C05',
        'C06',
        'C07',
        'C08',
        'C09',
        'C10',
        'C11',
        'C12',
        'C13',
        'C14',
        'C21',
        'C22',
        'C23',
        'C25',
        'C30',
        'C40',
        'C99',
        'D01',
        'D02',
        'D03',
        'D04',
        'D05',
        'D06',
        'D07',
        'D21',
        'D99',
        'E01',
        'E02',
        'E03',
        'E04',
        'E05',
        'E06',
        'E21',
        'E99',
        'F01',
        'F02',
        'F03',
        'F04',
        'F15',
        'F16',
        'F17',
        'F21',
        'F22',
        'F23',
        'F24',
        'F25',
        'F26',
        'F27',
        'F28',
        'F41',
        'F42',
        'F99',
        'G01',
        'G02',
        'G03',
        'G04',
        'G05',
        'G06',
        'G07',
        'G08',
        'G09',
        'G10',
        'G11',
        'G12',
        'G16',
        'G21',
        'G99',
        'H01',
        'H02',
        'H03',
        'H04',
        'H05',
        'H99',
        ]

def commit_progress(idx, page):
    f = open('progress.txt', 'w')
    progress = 'index: %s, page: %s' % (idx, str(page))
    f.write(progress)
    f.close()

def save_result(idx, ID, result):
    dir_name = './results/%s' % idx
    file_name = '%s/%s.json' % (dir_name, ID)

    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    f = open(file_name, 'w')
    f.write(result)
    f.close()
    
