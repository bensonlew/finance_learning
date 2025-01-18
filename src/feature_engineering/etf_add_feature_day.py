# coding:utf-8
#  给etf数据添加feature

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.feature_engineering.autoregressive_features import *
# from window_ops.rolling import seasonal_rolling_mean
from scipy.stats import pearsonr
import sys
import os
import talib as ta
from gs_quant.timeseries.technicals import exponential_std


def caculate_pearson_corr(data_choose_Kall, code):
    pass


def day_rank2min_rank(feature_rank, fearure_origin):
    # 确保两个DataFrame的date列类型一致
    feature_rank['date'] = pd.to_datetime(feature_rank['date'])
    fearure_origin['date'] = pd.to_datetime(fearure_origin['date'])
    
    # 选择需要的列
    fearure_origin_choose = fearure_origin
    # fearure_origin_choose = fearure_origin[['date', 'open', 'close', 'high', 'low', 'vol', 'amount']]
    
    # 合并数据
    return pd.merge(fearure_origin_choose, feature_rank, on="date", how="left")


def day_future_relation(future_data, fearure_origin, future_code):
    day_df = fearure_origin[47::48]
    day_df_choose = day_df[["date", "close"]]
    merge_df = pd.merge(day_df_choose, future_data, on="date", how="left")
    merge_df, add_corr_future = add_corr_feature(merge_df, rolls=[20, 60], column="close", column2=future_code + "_now")
    
    print(add_corr_future)
    # 获取昨天的数据

    merge_df["date"] = merge_df["date"].shift(-1)
    merge_df.drop(columns=["close", "table_name"], inplace=True)
    return pd.merge(fearure_origin, merge_df, on="date", how="left")

def run(code=None):
    # 获取文件后缀
    suffix = sys.argv[2]

    fdata_dir = os.environ.get('FDATA', '/data/finance/')
    data = pd.read_parquet(fdata_dir + "/{}.{}".format(code, suffix))

    print(data.columns)
    # 合并排序数据
    rank_file = "{}/{}.rank.parquet".format(fdata_dir, code)
    if os.path.exists(rank_file):

        feature_rank = pd.read_parquet(rank_file)        
        data = day_rank2min_rank(feature_rank, data)

    
    furure_dict = {
        "000300": "IF",
        "000016": "IH",
        "000905": "IC",
        "000852": "IM"
    }
    for future in furure_dict:
        future_code = furure_dict[future]
        future_file = "{}/future_data_{}.csv".format(fdata_dir, future)
        if os.path.exists(future_file):
            future_data = pd.read_csv(future_file)
            future_data["date"] = pd.to_datetime(future_data["date"])
            data = day_future_relation(future_data, data, future_code)
            print(len(data.columns))
    data.to_parquet(fdata_dir + "/{}.qfq.kdj.day.parquet".format(code))
  
if __name__ == "__main__":
    if len(sys.argv) < 2:
        code  = "510050"
    else:
        code = sys.argv[1]
    run(code)



