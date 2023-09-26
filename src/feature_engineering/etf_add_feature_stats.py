# coding:utf-8
#  给etf数据添加feature

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.feature_engineering.autoregressive_features import *
# from window_ops.rolling import seasonal_rolling_mean
from scipy.stats import pearsonr
import sys

def calculate_kdj(df, n=9, k_period=3, d_period=3):
    # 计算最高价的 n 天最高价和最低价的 n 天最低价
    df['H_n'] = df['high'].rolling(window=n).max()
    df['L_n'] = df['low'].rolling(window=n).min()
    
    # 计算 RSV 值
    df['RSV'] = (df['close'] - df['L_n']) / (df['H_n'] - df['L_n']) * 100
    
    # 计算 K 值和 D 值
    df['K'] = df['RSV'].ewm(com=k_period-1).mean()
    df['D'] = df['K'].ewm(com=d_period-1).mean()
    
    # 计算 J 值
    df['J'] = 3 * df['K'] - 2 * df['D']
    
    # 删除中间计算的列
    df.drop(['H_n', 'L_n', 'RSV'], axis=1, inplace=True)
    
    return df

def calculate_adx(df, n=14):
    # 计算动态范围（True Range）
    df['H-L'] = df['high'] - df['low']
    df['H-PC'] = abs(df['high'] - df['close'].shift(1))
    df['L-PC'] = abs(df['low'] - df['close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    # 计算方向线指标（Directional Movement Indicator）
    df['DM+'] = np.where(df['high'].diff() > df['low'].diff(), df['high'].diff(), 0)
    df['DM-'] = np.where(df['low'].diff() > df['high'].diff(), df['low'].diff(), 0)

    # 计算动态范围和方向线指标的平滑移动平均值
    df['ATR'] = df['TR'].rolling(window=n).mean()
    df['DM+MA'] = df['DM+'].rolling(window=n).mean()
    df['DM-MA'] = df['DM-'].rolling(window=n).mean()

    # 计算动态范围和方向线指标的方向性指标（Directional Indicator）
    df['DI+'] = (df['DM+MA'] / df['ATR']) * 100
    df['DI-'] = (df['DM-MA'] / df['ATR']) * 100

    # 计算动态范围和方向线指标的方向性指标差值和比值
    df['DI_diff'] = abs(df['DI+'] - df['DI-'])
    df['DI_sum'] = df['DI+'] + df['DI-']
    df['DX'] = (df['DI_diff'] / df['DI_sum']) * 100

    # 计算ADX指标
    df['ADX_{}'.format(n)] = df['DX'].rolling(window=n).mean()

    # 删除中间计算的列
    df.drop(['H-L', 'H-PC', 'L-PC', 'TR', 'DM+', 'DM-', 'ATR', 'DM+MA', 'DM-MA', 'DI+', 'DI-', 'DI_diff', 'DI_sum', 'DX'],
            axis=1, inplace=True)

    return df

def calculate_spectrum_energy(data):
    close = np.array(data["close"])
    fft_result= np.fft.fft(close)
    spectrum_energy = np.abs(fft_result) ** 2
    data["spectrum_energy"] = np.log(spectrum_energy)
    return data


def caculate_pearson_corr(data_choose_Kall, code):
    data_choose_K3_rmnan = data_choose_Kall.dropna(axis=0)
    data_choose_K3_rmnan1 = data_choose_K3_rmnan[data_choose_K3_rmnan["K_choose"] == "type1"]
    data_choose_K3_rmnan3 = data_choose_K3_rmnan[data_choose_K3_rmnan["K_choose"] == "type3"]
    print(len(data_choose_K3_rmnan1))
    print(len(data_choose_K3_rmnan3))
    for data_choose_type in ["up_24_96", "down_24_96", "up_24_480", "down_24_480", "up_96_480", "down_96_480"]:
        print(data_choose_type)
        # data_choose_K3_choose = data_choose_K3_rmnan[data_choose_K3_rmnan["K_choose"] == data_choose_type]
        choose_list = data_choose_type.split("_")
        fast = "close_rolling_{}_mean".format(choose_list[1])
        slow = "close_rolling_{}_mean".format(choose_list[2])
        if choose_list == "up":
            data_choose_K3_choose = data_choose_K3_rmnan[data_choose_K3_rmnan[fast] > data_choose_K3_rmnan[slow]]
        else: 
            data_choose_K3_choose = data_choose_K3_rmnan[data_choose_K3_rmnan[fast] < data_choose_K3_rmnan[slow]]

        for close1 in ["target_close1", "target_close2", "target_close5"]:
            target_close = data_choose_K3_choose[close1]
            print(close1)
            clean_col = [ 'datetime', 'code',
                'date', 'date_stamp', 'time_stamp', 'type', 'volume', 'suogu',
                'preclose', 'adj', "type", "target_close2", "target_close1",
                "K_choose", "target_close5", "K_choose_last", "date", "k_last", "k_last3", "datetime"]
            col_list = list(data_choose_K3_choose.columns)
            
            with open("{}_{}_{}.statcorr.tsv".format(code, data_choose_type, close1), 'w') as fo:

                for col in col_list:  
                    if col in clean_col:
                        continue
                    try:
                        a = pearsonr(target_close, data_choose_K3_choose[col])
                        fo.write("\t".join([code, data_choose_type, close1, col, str(a[0]), str(a[1])]) + "\n")
                        if a[1] < 0.05:
                            print(col, a[0], a[1])
                    except Exception as e:
                        print (col)
                        pass

def run(code=None):


    data = pd.read_parquet("/liubinxu/liubinxu/finance/learning/data/{}.qfq.kdj.parquet".format(code))


    # 择时策略
    data["k_last"] = data["K"].shift(1)
    data["k_last3"] = data["K"].shift(3)
    data["K_choose"] = "none"
    data["K_choose"][(data["k_last"] < 20) & (data["K"] >= 20) & (data["k_last3"] < 19)] = "type1"
    data["K_choose"][(data["k_last"] > 80) & (data["K"] < 80)] = "typen"
    data["K_choose"][(data["k_last"] < 50) & (data["K"] >= 50) & (data["k_last3"] < 45)]= "type2"

    data_choose = data[(data["K_choose"] !="none")]
    data_choose["K_choose_last"] = data_choose["K_choose"].shift()
    data_choose["K_choose"][(data_choose["K_choose"] == "type2") & (data_choose["K_choose_last"] == "type2")] = "type3"

    data_choose_K = data[(data["K_choose"] == "type1")]
    data_choose_K3 = data_choose[(data_choose["K_choose"] == "type3")]
    data_choose_Kall = data_choose[(data_choose["K_choose"] == "type1") |  (data_choose["K_choose"] == "type3")]

    caculate_pearson_corr(data_choose_Kall, code)

if __name__ == "__main__":
    code = sys.argv[1]
    run(code)



