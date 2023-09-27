# coding:utf-8
# 初始化通达信下载的历史数据


from QUANTAXIS.QASU.main import (QA_SU_save_etf_transaction,
                                 QA_SU_save_index_transaction,
                                 QA_SU_save_stock_transaction)
from QUANTAXIS.QASU.save_tdx import QA_SU_save_etf_xdxr

# QA_SU_save_etf_xdxr()     
QA_SU_save_stock_transaction("tdx")

QA_SU_save_index_transaction("tdx")

QA_SU_save_etf_transaction("tdx")