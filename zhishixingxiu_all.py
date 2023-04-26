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
# url = 'https://wx.zsxq.com/dweb2/index/group/51284524541124'
# strhtml = requests.get(url)        #Get方式获取网页数据
# print(strhtml.text)
last20 = []
# toaster = ToastNotifier()

def alert(intertime = 60):
    while True:
        now = datetime.datetime.now()
        if now.hour >= 9 and now.hour < 15:
            intertime = 20
        else:
            intertime = 60 * 60
        time.sleep(intertime + random.randint(1,40))
        print("now {}".format(now))
        refresh(last20)


def refresh(url):
    print("refresh")
    # url2 = "https://api.zsxq.com/v2/groups/51284524541124/topics?scope=all&count=20"
    # urladd = "https://api.zsxq.com/v2/groups/51284524541124/topics?scope=all&count=20&end_time=2023-04-11T14:29:09.804+0800"
    #  https://api.zsxq.com/v2/groups/51284524541124/topics?scope=all&count=20&end_time=2023-04-11       T14%3A29%3A09.804%2B0800
                                                                                            #  2023-04-07T10:02:53.197+0800
    # https://images.zsxq.com/Fuhh24k2OuYd61CT7Uv-dENgqTMp?imageMogr2/auto-orient/thumbnail/750x/format/jpg/blur/1x0/quality/75&e=1685548799&s=vtvmtmjjjvtvmmy&token=kIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD:tBuCdvalRj_dRb_Q8GrBgzngAjs=
    # https://images.zsxq.com/Fs-0rD1roKcrIDwjbnJFx8vITBcs?e=1685548799&token=kIxbL07-8jAj8w1n4s9zv64FuZZNEATmlU_Vm6zD:OHHI3fg2BxRzgzeeNurYOjU6yzc=                                                                               
    
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookie": "zsxqsessionid=33f4581f69dad02f4bea00614f55f8a5; zsxq_access_token=5500F4DE-5D8C-D957-4842-1C487B67CEB6_B829825041D6BAEB; abtest_env=product",
        "origin": "https://wx.zsxq.com",
        "referer": "https://wx.zsxq.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
    }

    r=requests.get(url, headers=headers)
    now_data = r.json() 
    if "topics" in now_data["resp_data"]:
        topics =  now_data["resp_data"]["topics"]
        return topics
    else:
        time.sleep(60)
        r=requests.get(url, headers=headers)
        now_data = r.json() 
        topics =  now_data["resp_data"]["topics"]
        return topics
        

def download_png(url, to_png):
    a = requests.get(url, stream=True)
    with open(to_png, 'wb') as f:
        shutil.copyfileobj(a.raw ,f)


def get_all_data(time_last = None):
    all_data_json = open("all_data.json", 'a')
    url2 = "https://api.zsxq.com/v2/groups/51284524541124/topics?scope=all&count=20"
    topics = refresh(url2)
    if time_last:
        url_new = url2 + "&end_time=" +  quote(time_last, 'utf-8')
        topics = refresh(url_new)

    time.sleep(random.randint(1,4))

    while len(topics) > 0:
        for topic in topics:
            all_data_json.write(json.dumps(topic, ensure_ascii=False) + "\n")
            if "talk" in topic:
                if "images" in topic["talk"]:
                    for image in topic["talk"]["images"]:
                        image_id = image["image_id"]
                        url = image["large"]["url"]
                        download_png(url, "images/{}.png".format(image_id))
                        # os.system("wget {} -O images/{}.png".format(url, image_id))
        time.sleep(random.randint(1,4))
        topics_last = topics[-1]
        time_last = topics_last["create_time"]

        url_new = url2 + "&end_time=" +  quote(time_last, 'utf-8')
        topics = refresh(url_new)

    all_data_json.close()
    

if __name__ == '__main__':
    time_last = sys.argv[1]
    get_all_data(time_last)
