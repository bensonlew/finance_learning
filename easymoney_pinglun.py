# -*- coding: utf-8 -*-
# __author__ = '刘彬旭'
# lastupdate by liubinxu
# 用于知识星球提示

from decimal import ROUND_DOWN
from weakref import ref
import requests
import time
import random
import os
import datetime
import pandas as pd
from lxml import html
import sys



def refresh(page, old_list= []):
    new_list = []
    url2 = "http://guba.eastmoney.com/list,zssh000001_{}.html".format(page)


    r=requests.get(url2)
    aa = html.fromstring(r.content)
    rows = aa.xpath('//*[@id="articlelistnew"]/div')
    for row in rows:
        l = []
        for ele in row.getchildren():
           l.append(str(ele.text_content()) )
        if "\t".join(l[2:]) in old_list:
            pass
        else:
            print("\t".join(l))
        new_list.append("\t".join(l[2:]))

    return new_list
    
def multi_refresh(n, m):
    old_list = []
    for page in range(n, m):
        if page % 20 == 1:
            time.sleep(random.randint(15,30))
        else:
            time.sleep(random.randint(4,10))
        old_list = refresh(str(page + 1), old_list)

if __name__ == '__main__':
    page_from = sys.argv[1]
    page_to = sys.argv[2]
    multi_refresh(int(page_from), int(page_to))
