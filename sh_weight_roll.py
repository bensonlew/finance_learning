# -*- coding: utf-8 -*-
# 大盘小盘周期轮动
from tracemalloc import start
from turtle import st
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
import datetime
import os
import math
import numpy as np

trade_rate = 0.6/10000

sh500 = ak.stock_zh_index_daily(symbol="sh000905")
sh50 = ak.stock_zh_index_daily(symbol="sh000016")
sh300 = ak.stock_zh_index_daily(symbol="sh000300")
sh1000 = ak.stock_zh_index_daily(symbol="sh000852")


sh300["big_amp"] = sh300["close"].pct_change()
sh1000["small_amp"] = sh1000["close"].pct_change()
sh500["middle_amp"] = sh500["close"].pct_change()
sh50["top_amp"] = sh50["close"].pct_change()


sh300.rename(columns={"open":"big_open", "close": "big_close"}, inplace=True)
sh1000.rename(columns={"open":"small_open", "close": "small_close"}, inplace=True)
sh500.rename(columns={"open":"middle_open", "close": "middle_close"}, inplace=True)
sh50.rename(columns={"open":"top_open", "close": "top_close"}, inplace=True)


df = pd.merge(left=sh300[["date", "big_open", "big_close", "big_amp"]],
             right=sh1000[["date", "small_open", "small_close", "small_amp"]],
             left_on=["date"], right_on=["date"])

df = df.merge(sh500, on=["date"])
df = df.merge(sh50, on=["date"])

def two_pass_method(start_time = "2014", first_index = "big", second_index = "small", short_time=10, long_time=60, change=0.0):
     
    df2 = df[df["date"].map(str)>start_time]
    df2["big_small"] = df2[first_index + "_amp"] - df2[second_index + "_amp"]
    df2["big+small"] = abs(df2[first_index + "_amp"] * df2[first_index + "_amp"] + df2[second_index + "_amp"] * df2[second_index + "_amp"])
    df2["big+small"] = df2["big+small"].map(math.sqrt)
    df2["big2small"] = df2["big_small"]/df2["big+small"]
    df2["big2small_roll"] = df2["big2small"].rolling(short_time, min_periods=1).mean()
    # df2["big2small_roll"] = df2["big2small"].rolling(short_time, min_periods=1).mean()-df2["big2small"].rolling(long_time, min_periods=1).mean()
    df2["big_roll"] = df2[first_index + "_close"].rolling(5, min_periods=1).mean()-df2[first_index + "_close"].rolling(20, min_periods=1).mean()
    df2["small_roll"] = df2[second_index + "_close"].rolling(5, min_periods=1).mean()-df2[second_index + "_close"].rolling(20, min_periods=1).mean()
    df2["style"] = "none"


    style_list = ["stop"]
    r_last = 0
    big_roll_yes = 0
    small_roll_yes = 0
    style = "big"
    # change = 0.0
    large_area = 0
    small_area = 0
    for l in df2.iterrows():
        r = l[1]["big2small_roll"]
        big_roll = l[1]["big_roll"]
        small_roll = l[1]["small_roll"]
        # big_roll = 1
        # small_roll = 1
        #     style = "nochange"

        
        if big_roll <0 and small_roll<0 and big_roll < big_roll_yes and small_roll < small_roll_yes:
            style = "stop"
        else:
            if r_last < - change and r > - change and style != "big":

                large_area = r
            if r_last > change and r < change and style != "small":
                style = "small"


            
            if style == "stop":
                if r > 0:
                    style = "big"
                else:
                    style = "small"

        r_last = r
        style_list.append(style)

        big_roll_yes = big_roll
        small_roll_yes = small_roll

        
    # style_list
    df2["style"] = style_list[:-1]

    df2["amp_s"] = 0
    df2.loc[df2["style"]=="big", "amp_s"] = df2["big_amp"]
    df2.loc[df2["style"]=="small", "amp_s"] = df2["small_amp"]
    df2.loc[df2["style"]=="stop", "amp_s"] = 0.0
    yestoday_style =  df2["style"].shift(-1)
    df2.loc[df2["style"] != yestoday_style, "amp_s"] -= 0.6/10000
    # df2.loc[df2["style"]=="change2big", "amp_s"] = df2["small_amp"] - 0.6/10000
    # df2.loc[df2["style"]=="change2small", "amp_s"] = df2["big_amp"] - 0.6/10000
    # df2.loc[df2["style"]=="stop", "amp_s"] = 0.0

    df2["strate_small_big"] = (df2["amp_s"] +1).cumprod()
    # df2.to_csv("tmp/{}_{}_{}_{}_{}_{}.tsv".format(start_time, first_index, second_index,short_time, long_time, change), sep="\t")
    return df2["strate_small_big"].iloc[-1]

if __name__ == "__main__":
    # print("f\ts\tshort_time\tlong_time\tchange\tresult")
    # for f in ["big", "top"]:
    #     for s in ["middle", "small"]:
    #         for short_time in [4, 5, 10, 20]:
    #             for long_time in [30, 60, 180]:
    #                 for change in [0, 0.05, 0.1, 0.2]:
    #                     result = two_pass_method(start_time = "2022", first_index = f, second_index = s, short_time=short_time, long_time=long_time, change=change)
    #                     result_list = [f, s, short_time, long_time, change, result]
    #                     result_str = [str(x) for x in result_list]
    #                     print("\t".join(result_str))


    print("f\ts\tshort_time\tlong_time\tchange\tresult")
    for f in ["big", "top"]:
        for s in ["middle", "small"]:
            for short_time in [2, 5, 10]:
                for long_time in [30, 60, 180]:
                    for change in np.arange(0.01, 0.2, 0.01):
                        result = two_pass_method(start_time = "2014", first_index = f, second_index = s, short_time=short_time, long_time=long_time, change=change)
                        result_list = [f, s, short_time, long_time, change, result]
                        result_str = [str(x) for x in result_list]
                        print("\t".join(result_str))

    # result = two_pass_method(start_time = "2014", first_index = "big", second_index = "small", short_time=10, long_time=60, change=0)