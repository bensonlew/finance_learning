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



        



def get_all_data():
    with open("all_data.json", 'r') as f, open("all_data.md", 'w') as fo:
        for line in f:
            data_dict = json.loads(line)
            # print(data_dict)
            fo.write("-----------\n")
            fo.write("* {}\n\n".format(data_dict["create_time"]))
            if data_dict["type"] == "talk":
                fo.write(data_dict['talk'].get("text", "") + "\n\n")
                if "images" in data_dict["talk"]:
                    for image in data_dict["talk"]["images"]:
                        image_id = image["image_id"]
                        fo.write("![](images/{}.png)\n\n".format(image_id))
            else:
                fo.write(data_dict['question'].get("text", "") + "\n")
                fo.write(data_dict['answer'].get("text", "") + "\n\n")



if __name__ == '__main__':

    get_all_data()
