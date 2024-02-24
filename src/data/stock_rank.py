# coding:utf-8
# 东方财富基金热度排序数据

from time import sleep
import pandas as pd
import requests
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
from QUANTAXIS.QASU.save_tdx import QA_SU_save_stock_rank
from akshare.stock.stock_hot_rank_em import stock_hot_rank_detail_em




if __name__ == "__main__":
    # import sys
    # etf_hot_rank_detail_em(sys.argv[1])
    
    
    etf_list_df = QA_fetch_get_stock_list(type_="stock")
    # etf_list_df = etf_list_df[:3]
    a = 0
    # etf_list_df = etf_list_df[140:]
    for etf_tupe in etf_list_df.iterrows():
        etf = dict(etf_tupe[1])
        # if(etf["code"]< "000901"):
        #     continue
        etf_code = etf["sse"] + etf["code"]
        # if etf["sse"] == "sz" and (etf["code"] < "000650" and etf["code"] != "000507"):
        #     continue
        print(etf_code)
        a += 1
        if a == 100:
            sleep(600)
            a = 0
        try:
            etf_rank = stock_hot_rank_detail_em(etf_code)
            print(etf_rank)
            etf_rank.columns = ["date", "rank", "code", "new_fans_num", "old_fas_num"]
            QA_SU_save_stock_rank(data_df = etf_rank)
        except Exception as e:
            print("获取数据失败 {}".format(etf_code))
            print(e)

        






