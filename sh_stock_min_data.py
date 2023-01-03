import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
import datetime
import os
import sys

start_date = sys.argv[1]
now = datetime.datetime.now().strftime("%y%m%d")

index_stock_info_df = ak.index_stock_info()

index_stock_info_df.to_csv("index_stock_info.csv", sep="\t")
index_list = list(index_stock_info_df["index_code"])
# index_list = ["000016", "000300", "000905"]


for index in index_list:
    if index.startswith("000"):
        if os.path.exists("sh_index_data" + "/" + index + "_" + now + ".5.tsv"):
            continue
        try:
            print(index)
            stock_zh_index_5_min_df = ak.index_zh_a_hist_min_em(
                symbol=index, period="5", start_date=start_date)
            stock_zh_index_5_min_df.to_csv(
                "sh_index_data" + "/" + index + "_" + now + ".5.tsv", sep="\t")
            stock_zh_index_1_min_df = ak.index_zh_a_hist_min_em(
                symbol=index, period="1", start_date=start_date)
            stock_zh_index_1_min_df.to_csv(
                "sh_index_data" + "/" + index + "_" + now + ".1.tsv", sep="\t")
        except Exception as e:
            print(e)
