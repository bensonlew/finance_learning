# coding:utf-8
# 初始化通达信下载的历史数据

from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
import datetime

date_str = str(datetime.datetime.now()).split(" ")[0]
# # QA_SU_save_etf_xdxr()
# etf = QA_fetch_get_stock_list("etf")

# etf.to_csv("etf_{}.tsv".format(date_str), sep="\t")

# index = QA_fetch_get_stock_list("index")

# index.to_csv("index_{}.tsv".format(date_str), sep="\t")

# stock = QA_fetch_get_stock_list("stock")

# stock.to_csv("stock_{}.tsv".format(date_str), sep="\t")


zs = QA_fetch_get_stock_list("gp")

zs.to_csv("gp_{}.tsv".format(date_str), sep="\t")