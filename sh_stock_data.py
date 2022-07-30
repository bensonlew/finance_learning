import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
import datetime
import os

sh_list = ak.stock_info_sh_name_code()
sh_del_list = ak.stock_info_sh_delist()

sh_code_list = sh_list["证券代码"]

if os.path.exists("sh_data"):
    pass
else:
    os.mkdir("sh_data")

for sh_code in sh_code_list:
    print("{} data".format(sh_code))
    try:
        stock_zh_a_hist_163_df = ak.stock_zh_a_hist_163(symbol="sh" + sh_code, start_date="20060101", end_date="20220101")
        stock_zh_a_hist_163_df.to_csv("sh_data/sh{}.tsv".format(sh_code), sep="\t")
    except Exception as e:
        print("{} data not get successful".format(sh_code))
        print(e)

for sh_code in sh_del_list["公司代码"]:
    try:
        stock_zh_a_hist_163_df = ak.stock_zh_a_hist_163(symbol="sh" + sh_code, start_date="20060101", end_date="20220101")
        stock_zh_a_hist_163_df.to_csv("sh_data/sh{}.tsv".format(sh_code), sep="\t")
    except Exception as e:
        print("{} del data not get successful".format(sh_code))
        print(e)



