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
from cemotion import Cemotion
from bson.son import SON
c = Cemotion()
import pymongo

uri = 'mongodb://localhost:27017'

client = pymongo.MongoClient(uri)
coll = client.quantaxis.easymoney_sentiment


def get_all_data(data):
    pub_last = ""
    err = False
    before_time = ""
    line_num = 0
    insert_data = list()
    with open(data, 'r') as f:
        for line in f:
            line_num += 1
            line_str = line.strip()
            if line_str.startswith('{'):
                try:
                    data_dict = json.loads(line)
                except:
                    print("load json err".format(line))
                    continue
                # pubtime = data_dict['post_last_time']
                bar = data_dict['stockbar_name']
                if bar == "上证指数吧":
                    post_title = data_dict["post_title"]
                    if find2mongo({'post_id': data_dict['post_id']}):
                        continue
                    else:
                        print("post id {} not find".format(data_dict['post_id']))
                    cemotion_sentiment = c.predict(post_title)
                    # print("cemotion_sentiment {}".format(cemotion_sentiment))
                    data_dict["cemotion_sentiment"] = float(cemotion_sentiment)
                    try:
                        insert_data.append(SON(data_dict))
                    except:
                        print("son data error".format(line))

            elif line_str.startswith('#'):
                pass

            if line_num % 1000 == 0:
                insert2mongo(insert_data)
                insert_data = list()

                print("insert line {}".format(line_num))
    
    insert2mongo(insert_data)
    print("insert last")

def find2mongo(query):
    record = coll.find_one(query)
    return record

def insert2mongo(insert_list):
    try:

        coll.create_index(
            [('post_id',
              pymongo.ASCENDING),
             ('post_publish_time',
              pymongo.ASCENDING)],
            unique=True
        )

        coll.insert_many(
            insert_list,
            ordered=False
        )
    except Exception as e:
        print(e)

    pass          
                
                


if __name__ == '__main__':

    get_all_data(sys.argv[1])
