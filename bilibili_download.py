# -*- coding: utf-8 -*-
# __author__ = '刘彬旭'
# lastupdate by liubinxu
# 用于知识星球提示

from decimal import ROUND_DOWN
import requests
import time
import random
import os
import datetime
import pandas as pd


user_dict = {
    "kangshao": "https://api.bilibili.com/x/space/wbi/arc/search?mid=509401159&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=caa91842ca5644bb19875c17fb7fa686&wts=1672145705",
    "yangtongxue": "https://api.bilibili.com/x/space/wbi/arc/search?mid=396327539&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=935e5b8209fe01125351c3f39c56ddcb&wts=1672148521",
    "wangansong": "https://api.bilibili.com/x/space/wbi/arc/search?mid=697048631&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=77731523573f88c630b9d1a8e23ba7e5&wts=1672148736",
    "badaoguping": "https://api.bilibili.com/x/space/wbi/arc/search?mid=254240848&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=9ad5abebac5a76808973546825e5fa48&wts=1672148793",
    "wangtianyu": "https://api.bilibili.com/x/space/wbi/arc/search?mid=488285015&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=62d97a2de55e50fe4e03a0c1a7765fcb&wts=1672148863",
    "haogelungu": "https://api.bilibili.com/x/space/wbi/arc/search?mid=307610125&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=e2ecc4faacf92bdeecd8c079b3df13ed&wts=1672148965",
    "husandu": "https://api.bilibili.com/x/space/wbi/arc/search?mid=302630035&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=4c384b27a6cbc9d26c35c70726415f34&wts=1672149016",
    "taoshaboshi": "https://api.bilibili.com/x/space/wbi/arc/search?mid=289706107&pn=1&ps=25&index=1&order=pubdate&order_avoided=true&w_rid=b2b363a484ba5891ff355ac5d90bba09&wts=1672149065"
}


def refresh(user, page):
    url2 = user_dict[user].replace("pn=1", "pn={}".format(page))

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cookie": "_uuid=2D2DD8DF-85B5-EA510-41CC-C65B312B2A9322391infoc; buvid3=6C5E2050-7C65-AD69-D86C-F72C5435699C25165infoc; b_nut=1647495825; buvid4=82BDE2EB-2DCF-159E-D312-2449D081E30925165-022031713-36Cjv9pGbYz6DSePOGmnjw%3D%3D; CURRENT_FNVAL=4048; blackside_state=1; CURRENT_BLACKGAP=1; PVID=1; sid=7q2ser2x; fingerprint=832993a408a3f570769a36c63e64748b; buvid_fp_plain=undefined; buvid_fp=832993a408a3f570769a36c63e64748b; DedeUserID=352917291; DedeUserID__ckMd5=58aacbd8c0cb6a9d; SESSDATA=06a53579%2C1673870605%2Cf7694*71; bili_jct=42454fb2708e25225b8a68a2adf90114; CURRENT_QUALITY=80; i-wanna-go-back=-1; b_ut=5; bsource=search_baidu; b_lsid=1038B58C4_18553A0F35A; bp_video_offset_352917291=744335016766472300; innersign=1; rpdid=|(J~lkJ|)J||0J'uY~kuRlJml",
        "origin": "https://space.bilibili.com",
        "referer": "https://space.bilibili.com/509401159/?spm_id_from=333.999.0.0",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Linux",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"

    }

    r=requests.get(url2, headers=headers)
    now_data = r.json()

    vl = now_data["data"]["list"]['vlist']
    df = pd.DataFrame.from_records(vl)
    df_choose = df[['comment', 'play', 'title', 'subtitle', 'description', 'created']]
    df_choose["created"] = df["created"].apply(lambda x:time.strftime("%Y-%m-%d", time.localtime(x)))
    df_choose.to_csv("{}_{}.tsv".format(user, page), sep="\t", index=False)
    # print(now_data)


if __name__ == '__main__':
    for user in user_dict.keys():
        for page in ["1", "2", "3"]:
            refresh(user, page)
