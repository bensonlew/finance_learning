# coding:utf-8
# 初始化通达信下载的历史数据

import pandas as pd
from QUANTAXIS.QASU.main import (QA_SU_save_etf_min, QA_SU_save_index_min,
                                 QA_SU_save_single_index_min)
from QUANTAXIS.QASU.save_tdx import QA_SU_save_etf_xdxr

# QA_SU_save_etf_xdxr()
# QA_SU_save_index_min("tdx")
# QA_SU_save_etf_min("tdx")

index =  "/liubinxu/liubinxu/finance/learning/index_stock_info.csv"
index_df = pd.read_table(index, sep="\t", header=0, dtype="str")

for code in index_df["index_code"]:
    if code.startswith("000"):
        print("code {}".format(code))
        QA_SU_save_single_index_min(code=code,  engine = "tdx")



