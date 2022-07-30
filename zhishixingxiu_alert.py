# -*- coding: utf-8 -*-
# __author__ = '刘彬旭'
# lastupdate by liubinxu
# 用于知识星球提示

import requests
import time
import random
import os
import datetime
# url = 'https://wx.zsxq.com/dweb2/index/group/51284524541124'
# strhtml = requests.get(url)        #Get方式获取网页数据
# print(strhtml.text)
last20 = []

def alert(intertime = 60):
    while True:
        now = datetime.datetime.now()
        if now.hour == 9:
            intertime = 60
        elif now.hour == 15:
            intertime = 60 * 60
        time.sleep(intertime + random.randint(1,40))
        refresh(last20)


def refresh(last20):
    url2 = "https://api.zsxq.com/v2/groups/51284524541124/topics?scope=all&count=20"

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookie": "abtest_env=product; zsxq_access_token=593F36AE-A62B-3131-BF06-58328CD50734_B829825041D6BAEB",
        "origin": "https://wx.zsxq.com",
        "referer": "https://wx.zsxq.com/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
    }

    r=requests.get(url2, headers=headers)
    now_data = r.json()
    # print(now_data)
    if "resp_data" in now_data and "topics" in now_data["resp_data"]:
        pass
    else:
        return
    for l in now_data["resp_data"]["topics"][:5]:
        # print(l)
        if l['topic_id'] in last20:
            pass
        else:
            last20.append(l['topic_id'])
            if len(last20) > 20:
                last20 = last20[:21]
            if 'talk' in l:
                print(l['topic_id'], l['talk']["text"])
                os.system('/usr/bin/notify-send -u critical {}'.format(l['talk']["text"]))
            if 'question' in l:
                print(l['topic_id'], l['question']["text"], l['answer']["text"])
                os.system('/usr/bin/notify-send -u critical {}'.format(l['question']["text"])) 
                os.system('/usr/bin/notify-send -u critical {}'.format(l['answer']["text"]))

if __name__ == '__main__':
    alert(200)
