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


def calculate_macd(df, level=1):
    
    short=12 * level
    long=26 * level
    signal=9 * level
    df['macd_{}'.format(level)], df['macdsignal_{}'.format(level)], df['macdhist_{}'.format(level)] = ta.MACD(df['close'], fastperiod=short, slowperiod=long, signalperiod=signal)
    return df

def calculate_bolling(df, level=1):
    
    n = 20 * level

    df['bbands_upper_{}'.format(level)], df['bbands_middle_{}'.format(level)], df['bbands_lower_{}'.format(level)] = ta.BBANDS(df['close'], timeperiod=n, nbdevup=2, nbdevdn=2, matype=0)
    df['bbands_normal_{}'.format(level)] = (df['close'] - df['bbands_middle_{}'.format(level)]) / (df['bbands_upper_{}'.format(level)] - df['bbands_lower_{}'.format(level)])
    return df

def calculate_es(df, level=1):
    
    beta = 1 - (0.9 ** level)
    df['ev_{}'.format(level)] = exponential_std(df["close"], beta)
    df['esv_{}'.format(level)] = exponential_std(df["close"].diff(), beta)

    return df



def calculate_kdj(df, n=9, k_period=3, d_period=3, abr=""):
    # 计算最高价的 n 天最高价和最低价的 n 天最低价
    df['H_n'] = df['high'].rolling(window=n).max()
    df['L_n'] = df['low'].rolling(window=n).min()
    
    # 计算 RSV 值
    df['RSV'] = (df['close'] - df['L_n']) / (df['H_n'] - df['L_n']) * 100
    
    # 计算 K 值和 D 值
    df['K' + abr] = df['RSV'].ewm(com=k_period-1).mean()
    df['D' + abr] = df['K' + abr].ewm(com=d_period-1).mean()
    
    # 计算 J 值
    df['J' + abr] = 3 * df['K' + abr] - 2 * df['D' + abr]
    
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
    for data_choose_type in ["type1", "type3"]:
        # print(data_choose_type)
        data_choose_K3_choose = data_choose_K3_rmnan[data_choose_K3_rmnan["K_choose"] == data_choose_type]
        for close1 in ["target_close1", "target_close2", "target_close5"]:
            target_close = data_choose_K3_choose[close1]
            print(close1)
            clean_col = [ 'datetime', 'code',
                'date', 'date_stamp', 'time_stamp', 'type', 'volume', 'suogu',
                'preclose', 'adj', "type", "target_close2", "target_close1",
                "K_choose", "target_close5", "K_choose_last", "date", "k_last", "k_last3", "datetime"]
            col_list = list(data_choose_K3_choose.columns)
            
            with open("{}_kdj.statcorr.tsv".format(code), 'aw') as fo:

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

def add_kdj_type(data, k_abr):
    data["k_last"] = data[k_abr].shift(1)
    data["K_choose" + "_" + k_abr] = "none"
    data["K_choose" + "_" + k_abr][(data["k_last"] < 20) & (data[k_abr] >= 20)] = "type1"
    data["K_choose" + "_" + k_abr][(data["k_last"] > 80) & (data[k_abr] < 80)] = "typen"
    data["K_choose" + "_" + k_abr][(data["k_last"] < 50) & (data[k_abr] >= 50)]= "type2"

    data_choose = data[(data["K_choose" + "_" + k_abr] !="none")]
    data_choose["K_choose_last"] = data_choose["K_choose" + "_" + k_abr].shift()
    data_choose["K_choose" + "_" + k_abr][(data_choose["K_choose" + "_" + k_abr] == "type2") & (data_choose["K_choose_last"] == "type2")] = "type3"
    data["K_choose" + "_" + k_abr][data_choose.index] = data_choose["K_choose" + "_" + k_abr]
    data.drop(['k_last'], axis=1, inplace=True)
    return data

def run(code=None, tickets=False):
    fdata_dir = os.environ.get('FDATA', '/data/finance/')    
    data = pd.read_parquet(fdata_dir + "/{}.qfq.merge.parquet".format(code))
    if tickets == True:
        large_feature_data = pd.read_parquet(fdata_dir + "/large_tickets_data/{}.parquet".format(code))
        large_feature_data.drop(columns=["vol"], inplace=True)
        data = pd.merge(data, large_feature_data, left_index=True, right_index=True, how="left")

    data["datetime"] = data["datetime"].map(str)
    data,fea = add_seasonal_rolling_features(data, seasonal_periods=[48], rolls=[20], column="amount" )
    data,fea = add_seasonal_rolling_features(data, seasonal_periods=[48], rolls=[5], column="amount" )
    data,fea = add_seasonal_rolling_features(data, seasonal_periods=[48], rolls=[60], column="amount" )
    
    if tickets:
        data,fea = add_seasonal_rolling_features(data, seasonal_periods=[48], rolls=[20], column="turnover" )
        data,fea = add_seasonal_rolling_features(data, seasonal_periods=[48], rolls=[5], column="turnover" )
        data,fea = add_seasonal_rolling_features(data, seasonal_periods=[48], rolls=[60], column="turnover" )


    data["amount_normalize5"] = np.log(data["amount"]/data["amount_48_seasonal_rolling_5_mean"])
    data["amount_normalize20"] = np.log(data["amount"]/data["amount_48_seasonal_rolling_20_mean"])
    data["amount_normalize60"] = np.log(data["amount"]/data["amount_48_seasonal_rolling_60_mean"])

    if tickets:
        data["turnover_normalize5"] = np.log(data["turnover"]/data["turnover_48_seasonal_rolling_5_mean"])
        data["turnover_normalize20"] = np.log(data["turnover"]/data["turnover_48_seasonal_rolling_20_mean"])
        data["turnover_normalize60"] = np.log(data["turnover"]/data["turnover_48_seasonal_rolling_60_mean"])

        data["buy_turnover_normalize5"] = np.log(data["buy_turnover"]/data["turnover_48_seasonal_rolling_5_mean"])
        data["buy_turnover_normalize20"] = np.log(data["buy_turnover"]/data["turnover_48_seasonal_rolling_20_mean"])
        data["buy_turnover_normalize60"] = np.log(data["buy_turnover"]/data["turnover_48_seasonal_rolling_60_mean"])

        data["sell_turnover_normalize5"] = np.log(data["sell_turnover"]/data["turnover_48_seasonal_rolling_5_mean"])
        data["sell_turnover_normalize20"] = np.log(data["sell_turnover"]/data["turnover_48_seasonal_rolling_20_mean"])
        data["sell_turnover_normalize60"] = np.log(data["sell_turnover"]/data["turnover_48_seasonal_rolling_60_mean"])

        data["turnover_imbalance_rate"] = data["turnover_imbalance"] / data["turnover"]

    # data["amount_diff"] = data["amount_normalize"].diff()
    data, features = add_rolling_features(data, rolls=[6, 24, 96, 480, 2880], column="close", agg_funcs=["mean", "std", "std_mean", "exp_mean"])
    data, features = add_rolling_features(data, rolls=[24, 96, 480], column="amount_normalize5", agg_funcs=["mean", "std", "std_mean", "exp_mean"])
    data, features = add_rolling_features(data, rolls=[24, 96, 480], column="amount_normalize20", agg_funcs=["mean", "std", "std_mean", "exp_mean"])
    data, features = add_rolling_features(data, rolls=[24, 96, 480], column="amount_normalize60", agg_funcs=["mean", "std", "std_mean", "exp_mean"])
    # data, features2 = add_rolling_features(data, rolls=[24, 96, 480], column="amount_diff", agg_funcs=["mean", "std", "std_mean"])
    if tickets:
        for normal_amount in [
                            "turnover_normalize5", "turnover_normalize20", "turnover_normalize60",
                            "buy_turnover_normalize5", "buy_turnover_normalize20", "buy_turnover_normalize60",                          
                            "sell_turnover_normalize5", "sell_turnover_normalize20", "sell_turnover_normalize60",
                            "turnover_imbalance_rate"
                            ]:
            data, features = add_rolling_features(data, rolls=[24, 96, 480], column="{}".format(normal_amount), agg_funcs=["mean", "std", "std_mean", "exp_mean"])

    data["close6_close24"] = data["close_rolling_6_mean"] - data["close_rolling_24_mean"]
    data["close6_close96"] = data["close_rolling_6_mean"] - data["close_rolling_96_mean"]
    data["close6_close480"] = data["close_rolling_6_mean"] - data["close_rolling_480_mean"]
    data["close24_close480"] = data["close_rolling_24_mean"] - data["close_rolling_480_mean"]
    data["close24_close2880"] = data["close_rolling_24_mean"] - data["close_rolling_2880_mean"]
    data["close480_close2880"] = data["close_rolling_480_mean"] - data["close_rolling_2880_mean"]

    close_corr2 = ["amount_normalize5", "amount_normalize20", "amount_normalize60"]
    if tickets:
        # close_corr2 = []
        # data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close", column2="amount_normalize")
        close_corr2 +=  ["turnover_normalize5", "turnover_normalize20", "turnover_normalize60",
                        "buy_turnover_normalize5", "buy_turnover_normalize20", "buy_turnover_normalize60",
                        "sell_turnover_normalize5", "sell_turnover_normalize20", "sell_turnover_normalize60",
                        "turnover_imbalance_rate"]
        for normal_amount in close_corr2:
            data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close", column2="{}".format(normal_amount))    
            data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close_rolling_24_mean", column2="{}_rolling_24_mean".format(normal_amount))    
            data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close_rolling_96_mean", column2="{}_rolling_96_mean".format(normal_amount))    
            data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close_rolling_480_mean", column2="{}_rolling_480_mean".format(normal_amount))    


    data = calculate_kdj(data, n=9*2, k_period=3*2, d_period=3*2,  abr="18")
    data = calculate_kdj(data, n=9*4, k_period=3*4, d_period=3*4,  abr="36")
    data = calculate_kdj(data, n=9*8, k_period=3*8, d_period=3*8,  abr="72")
    data = calculate_kdj(data, n=9*16, k_period=3*16, d_period=3*16,  abr="144")


    data["target_close1"] = (data["close"].shift(-48) - data["close"])/data["close"]
    data["target_close2"] = (data["close"].shift(-96) - data["close"])/data["close"]
    data["target_close5"] = (data["close"].shift(-240) - data["close"])/data["close"]
    data["target_close20"] = (data["close"].shift(-960) - data["close"])/data["close"]

    data = add_kdj_type(data, "K18")
    data = add_kdj_type(data, "K36")
    data = add_kdj_type(data, "K72")

    for level in [1, 3, 6, 12, 24, 48, 96]:
        data = calculate_macd(data, level=level)
        data = calculate_bolling(data, level=level)
        data = calculate_es(data, level=level)


    


    # data_choose = data[['open', 'close', 'high', 'low', 'vol', 'amount', 'datetime', 'code','date', 'amount_normalize', 'K', 'D', 'J', "close_rolling_480_std", "amount_normalize_rolling_6_mean", "amount_diff_rolling_24_std"]]
    data_choose = data
    data_choose.to_parquet(fdata_dir + "/{}.qfq.merge.kdj.parquet".format(code))


    

    # 择时策略
    # data["k_last"] = data["K"].shift(1)
    # data["k_last3"] = data["K"].shift(3)
    # data["K_choose"] = "none"
    # data["K_choose"][(data["k_last"] < 20) & (data["K"] >= 20) & (data["k_last3"] < 19)] = "type1"
    # data["K_choose"][(data["k_last"] > 80) & (data["K"] < 80)] = "typen"
    # data["K_choose"][(data["k_last"] < 50) & (data["K"] >= 50) & (data["k_last3"] < 45)]= "type2"

    # data_choose = data[(data["K_choose"] !="none")]
    # data_choose["K_choose_last"] = data_choose["K_choose"].shift()
    # data_choose["K_choose"][(data_choose["K_choose"] == "type2") & (data_choose["K_choose_last"] == "type2")] = "type3"

    # data_choose_K = data[(data["K_choose"] == "type1")]
    # data_choose_K3 = data_choose[(data_choose["K_choose"] == "type3")]
    # data_choose_Kall = data_choose[(data_choose["K_choose"] == "type1") |  (data_choose["K_choose"] == "type3")]

    # caculate_pearson_corr(data_choose_Kall, code)

if __name__ == "__main__":
    code = sys.argv[1]
    run(code)



