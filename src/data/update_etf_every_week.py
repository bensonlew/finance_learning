# coding:utf-8
# 初始化通达信下载的历史数据

import pandas as pd
from QUANTAXIS.QAFetch import QA_fetch_get_security_bars
from QUANTAXIS.QASU.main import (QA_SU_save_etf_min, QA_SU_save_index_min,
                                 QA_SU_save_single_index_min,
                                 QA_SU_save_stock_block, QA_SU_save_stock_min)
from QUANTAXIS.QASU.save_tdx import QA_SU_save_etf_xdxr

# QA_SU_save_etf_xdxr()
QA_SU_save_index_min("tdx")
QA_SU_save_etf_min("tdx")

QA_SU_save_stock_block("tdx")

index =  "/liubinxu/liubinxu/finance/learning/index_stock_info.csv"
index_df = pd.read_table(index, sep="\t", header=0, dtype="str")

for code in index_df["index_code"]:
    if code.startswith("000"):
        print("code {}".format(code))
        QA_SU_save_single_index_min(code=code,  engine = "tdx")

QA_SU_save_stock_min("tdx")

# codes = ["930598",
#         "930601",
#         "930608",
#         "930614",
#         "930632",
#         "930633",
#         "930641",
#         "930651",
#         "930652",
#         "930697",
#         "930707",
#         "930713",
#         "930721",
#         "930726",
#         "930851",
#         "930901",
#         "930902",
#         "930965",
#         "930997",
#         "931009",
#         "931066",
#         "931071",
#         "931079",
#         "931087",
#         "931151",
#         "931152",
#         "931160",
#         "931456",
#         "931521",
#         "931637",
#         "931643",
#         "931719",
#         "931775",
#         "931866",
#         "980017",
#         "980032",
#         "990001"]
# for codea in codes:
#     QA_SU_save_single_index_min(code=codea, engine = "tdx")







