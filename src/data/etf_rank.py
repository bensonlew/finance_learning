# coding:utf-8
# 东方财富基金热度排序数据

import pandas as pd
import requests
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
from QUANTAXIS.QASU.save_tdx import QA_SU_save_etf_rank


def etf_hot_rank_detail_em(symbol: str = "SH510050") -> pd.DataFrame:
    """
    东方财富-个股人气榜-历史趋势及粉丝特征
    http://guba.eastmoney.com/rank/stock?code=000665
    :param symbol: 带市场表示的证券代码
    :type symbol: str
    :return: 个股的历史趋势及粉丝特征
    :rtype: pandas.DataFrame
    """
    url_rank = "https://emappdata.eastmoney.com/fundrank/getHisETFList"
    payload = {
        "appId": "appId01",
        "globalId": "786e4c21-70dc-435a-93bb-38",
        "marketType": "etf",
        "srcSecurityCode": symbol,
    }
    r = requests.post(url_rank, json=payload)
    data_json = r.json()
    # print(data_json)
    temp_df = pd.DataFrame(data_json["data"])
    temp_df["证券代码"] = symbol
    # print(temp_df)
    temp_df.columns = ["date", "rank", "code"]
    temp_df = temp_df[["date", "rank", "code"]]
    return temp_df


if __name__ == "__main__":
    # import sys
    # etf_hot_rank_detail_em(sys.argv[1])
    
    
    etf_list_df = QA_fetch_get_stock_list(type_="etf")
    # etf_list_df = etf_list_df[:3]
    for etf_tupe in etf_list_df.iterrows():
        etf = dict(etf_tupe[1])
        
        etf_code = etf["sse"] + etf["code"]
        try:
            etf_rank = etf_hot_rank_detail_em(etf_code)
            print(etf_rank)
            QA_SU_save_etf_rank(data_df = etf_rank)
        except:
            print("获取数据失败 {}".format(etf_code))

        






