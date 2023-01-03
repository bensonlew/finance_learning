# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
import datetime
import glob
import os

etfs = glob.glob("sh_etf_data/*daily.tsv")
sh000001 = ak.stock_zh_index_daily(symbol="sh000001")
sh000001["sh000001"] = sh000001["close"].pct_change().rolling(5, min_periods=1).mean()
merge_df = sh000001[["date", "sh000001"]]
merge_df["date"] =  merge_df["date"].map(str)

for etf in etfs:
    etf_name = os.path.basename(etf).split("_")[0]
    print(etf_name)
    etf_df = pd.read_table(etf, index_col=0)
    etf_df[etf_name] = etf_df["close"].pct_change().rolling(5, min_periods=1).mean()
    etf_df_choose = etf_df[["date", etf_name]]
    merge_df = pd.merge(left=merge_df, right=etf_df_choose, left_on=["date"], right_on=["date"])

merge_df.to_csv("merge_etf_rolling5.csv", sep="\t", index=False)