# -*- coding: utf-8 -*-
# __author__ = '刘彬旭'
# lastupdate by liubinxu
# 用于知识星球提示

import requests
import time
import random
import os
import datetime
# from win10toast import ToastNotifier
from urllib.parse import quote
import json
import shutil
import sys



def get_all_data(data):
    pub_last = ""
    err = False
    before_time = ""
    with open(data, 'r') as f:
        for line in f:
            line_str = line.strip()
            if line_str.startswith('{'):
                data_dict = json.loads(line)
                pubtime = data_dict['post_last_time']
                bar = data_dict['stockbar_name']
                if bar == "上证指数吧":
                    pub_last = pubtime
                    bar_last = bar
                if err:
                    if bar == "上证指数吧" and pub_last < before_time:
                        print("now time{}".format(pub_last))
                        err = False
            elif line_str.startswith('#'):
                print("last time {}".format(pub_last))
                before_time = pub_last
                print(line_str)
                err = True
            
                
                


if __name__ == '__main__':

    get_all_data(sys.argv[1])
