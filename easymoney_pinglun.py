# -*- coding: utf-8 -*-
# __author__ = '刘彬旭'
# lastupdate by liubinxu
# 用于知识星球提示

from decimal import ROUND_DOWN
from email.errors import StartBoundaryNotFoundDefect
from weakref import ref
import requests
import time
import random
import os
import datetime
import pandas as pd
from lxml import html
import sys
import json

stop_list  = None

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "qgqp_b_id=cc8a83d26671596ed29186a7a5acc8ee; em-quote-version=topspeed; HAList=ty-1-603777-%u6765%u4F0A%u4EFD%2Cty-1-601888-%u4E2D%u56FD%u4E2D%u514D%2Cty-1-513220-%u5168%u7403%u4E92%u8054ETF%2Cty-1-561560-%u7535%u529BETF%2Cty-1-510050-%u4E0A%u8BC150ETF%2Cty-1-600072-%u4E2D%u8239%u79D1%u6280%2Cty-1-000852-%u4E2D%u8BC11000%2Ca-sh-603777-%u6765%u4F0A%u4EFD%2Cty-1-000001-%u4E0A%u8BC1%u6307%u6570%2Cty-0-000016-%u6DF1%u5EB7%u4F73%uFF21; st_si=09950028364816; listtype=0; st_asi=delete; st_pvi=78563919313765; st_sp=2022-12-10%2018%3A01%3A45; st_inirUrl=http%3A%2F%2Fquote.eastmoney.com%2Fzs000016.html; st_sn=28; st_psi=20230825202309458-117001356556-8762507110",  # 替换成你的 Cookie
    "Host": "guba.eastmoney.com",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
}

def refresh(page, old_list= []):
    new_list = []
    url2 = "http://guba.eastmoney.com/list,zssh000001_{}.html".format(page)

    global stop_list
    r=requests.get(url2, headers=headers)
    aa = html.fromstring(r.content)
    rows = aa.xpath('//*[@id="articlelistnew"]/div')
    for row in rows:
        l = []
        href = None
        for ele in row.getchildren():
            try:
                for ele_sub1 in ele.getchildren():
                    if "title" in ele_sub1.attrib:
                        # l.append(ele_sub1.attrib["title"])
                        href = ele_sub1.attrib["href"]
                        break
                # print("href")
                # href = l.append(ele_sub1.attrib["data-postid"])
            except:
                pass
            l.append(str(ele.text_content()).replace("\t", " ") )
        if "\t".join(l[2:]) in old_list:
            pass
        else:
            # print("\t".join(l))
            # print("href {}".format(href))
            if len(l) != 5:
                continue
            all_data = {
                "reading": l[0],
                "comment": l[1],
                "title": l[2],
                "author": l[3],
                "last_updated": l[4]
            }
            # try:
            #     if int(l[1]) > 3 and href:
            #         if href.startswith("//"):
            #             # detail_data = parse_data("https:{}".format(href))
            #             detail_data = {
            #                 "last_updated": href.split("news/")[1][:12]
            #             }
            #             all_data.update(detail_data)
            #         elif href.startswith("/"):
            #             # print(href)
            #             detail_data = parse_data("https://guba.eastmoney.com{}".format(href))

            #             all_data.update(detail_data)
            # except Exception as e:
            #     pass
                # print(e)
            print(json.dumps(all_data, ensure_ascii=False))

        if stop_list and len(l)>3:
            if l[-2] == stop_list[-1] and l[-3] == stop_list[-2]:
                sys.exit(0)

        new_list.append("\t".join(l[2:]))

    return new_list

def parse_data(url):
    time.sleep(random.randint(1,10))
    # print(url)
    rp=requests.get(url)
    ap = html.fromstring(rp.content)
    script_ele = ap.xpath('//script')
    clean_json = None
    for script in script_ele:
        if not script.text:
            continue
        text = script.text.split('\n')
        for line in text:
            if " var post_article = " in line:
                clean_json = line.split("var post_article = ")[1].rstrip(";\r")
    if clean_json:
        clean_dict = json.loads(clean_json)
        return clean_dict["post"]
    else:
        return {}
    
                

def parse_pinglun(url):
    rp=requests.get(url)
    ap = html.fromstring(rp.content)
    a = ap.xpath('//*[@class="post_time fl"]')

    date_str = a[0].text
    # //*[@id="comment_all_content"]/div/div[1]
    replys = ap.xpath('//*[@id="comment_all_content"]/div/div')

    for reply in replys:
        reply_name = reply.xpath('//*[@class="replyer_name"]')
        reply_nme = reply_name[0].text
        time = reply.xpath('//*[@class="publish_time"]/span')
        tme = time[0].text
        text = reply.xpath('//*[@class="full_text"]')
        txt =  text.text
        pinlun = ["pinlun", "0", txt, reply_name , tme]
        print("\t".join(pinlun))




def multi_refresh(n):
    old_list = []
    for page in range(n, m):
        if page % 20 == 1:
            time.sleep(random.randint(15,30))
        else:
            pass
            # time.sleep(random.randint(2,10))
        old_list = refresh(str(page + 1), old_list)



if __name__ == '__main__':
    # page = sys.argv[1]
    # if len(sys.argv) > 2:
    #     stop_list = [sys.argv[2], sys.argv[3]]
    page = 2
    # print("stop {}".format(stop_list))
    multi_refresh(int(page))
