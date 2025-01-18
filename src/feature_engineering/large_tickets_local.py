# coding:utf-8
# 统计大单成交明细
# 
from concurrent.futures import thread
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.feature_engineering.autoregressive_features import *
# from window_ops.rolling import seasonal_rolling_mean
from scipy.stats import pearsonr
from scipy.stats import kurtosis
import sys
import os


uri = 'mongodb://localhost:27017'


def large_stat_time(record, transaction_df=None, day_stat_df=None):
    # 获取datetime属性和上一条记录的datetime属性
    #     print(record)
    curr_datetime = str(record.name)

    prev_datetime = str(record["pre_datetime"])
    #     print(curr_datetime)
    #     print(prev_datetime)

    # 获取transaction_df 该段时间之间的记录
    transaction_df_choose = transaction_df[(transaction_df["datetime"] >= prev_datetime) & (transaction_df["datetime"] < curr_datetime)]
    # print(len(transaction_df_choose))
    #获取改天的成交量均值和标准差
    if len(day_stat_df[day_stat_df.index == record["date"]]) == 0:
        print("no data for this day %s" % record["date"])
        return pd.Series({
            "buy_1_ratio": 0,
            "buy_1_amount_ratio": 0,
            "sell_1_ratio": 0,
            "sell_1_amount_ratio": 0,
            "buy_1_diff2_sum": 0,
            "sell_1_diff2_sum": 0,

            "buy_2_ratio": 0,
            "buy_2_amount_ratio": 0,
            "sell_2_ratio": 0,
            "sell_2_amount_ratio": 0,
            "buy_2_diff2_sum": 0,
            "sell_2_diff2_sum": 0,

            "buy_3_ratio": 0,
            "buy_3_amount_ratio": 0,
            "sell_3_ratio": 0,
            "sell_3_amount_ratio": 0,
            "buy_3_diff2_sum": 0,
            "sell_3_diff2_sum": 0
        })
    
    day_stat_dict = day_stat_df[day_stat_df.index == record["date"]].to_dict("records")[0]

    thereshold_1 = day_stat_dict["mean_5"] + day_stat_dict["std_5"]
    thereshold_2 = day_stat_dict["mean_5"] + 2 * day_stat_dict["std_5"]
    thereshold_3 = day_stat_dict["mean_5"] + 3 * day_stat_dict["std_5"]

    thereshold_1_exp = np.exp(thereshold_1)
    thereshold_2_exp = np.exp(thereshold_2)
    thereshold_3_exp = np.exp(thereshold_3)

    
    buy_df = transaction_df_choose[transaction_df_choose["buyorsell"] == 0]
    sell_df = transaction_df_choose[transaction_df_choose["buyorsell"] == 1]
    

    if len(buy_df) ==0:
        buy = pd.Series([0])
    else:
        buy = buy_df["vol"]
    if len(sell_df) == 0:
        sell = pd.Series([0])
    else:
        sell = sell_df["vol"]

    buy_1_index = (buy > thereshold_1_exp) & (buy < thereshold_2_exp)
    buy_2_index = (buy > thereshold_2_exp) & (buy < thereshold_3_exp)
    buy_3_index = buy > thereshold_3_exp

    sell_1_index = (sell > thereshold_1_exp) & (sell < thereshold_2_exp)
    sell_2_index = (sell > thereshold_2_exp) & (sell < thereshold_3_exp)
    sell_3_index = sell > thereshold_3_exp

    buy_1 = buy[buy_1_index]
    # print(buy_df)
    if len(buy_1) == 0:
        buy_1_diff2_sum = 0
    else:
        buy_1_diff2_sum = buy_df[buy_1_index]["diff_2_mean"].sum()

    sell_1 = sell[sell_1_index]
    if len(sell_1) == 0:
        sell_1_diff2_sum = 0
    else:
        sell_1_diff2_sum = sell_df[sell_1_index]["diff_2_mean"].sum()

    buy_2 = buy[buy_2_index]
    # print(buy_df)
    if len(buy_2) == 0:
        buy_2_diff2_sum = 0
    else:
        buy_2_diff2_sum = buy_df[buy_2_index]["diff_2_mean"].sum()

    sell_2 = sell[sell_2_index]
    if len(sell_2) == 0:
        sell_2_diff2_sum = 0
    else:
        sell_2_diff2_sum = sell_df[sell_2_index]["diff_2_mean"].sum()

    
    buy_3 = buy[buy_3_index]
    if len(buy_3) == 0:
        buy_3_diff2_sum = 0
    else:
        buy_3_diff2_sum = buy_df[buy_3_index]["diff_2_mean"].sum()
    sell_3 = sell[sell_3_index]
    if len(sell_3) == 0:
        sell_3_diff2_sum = 0
    else:
        sell_3_diff2_sum = sell_df[sell_3_index]["diff_2_mean"].sum()

    # 计算buy_1大单交易比例和成交总量比例
    buy_1_ratio = buy_1.shape[0] / buy.shape[0]
    buy_1_amount_ratio = buy_1.sum() / buy.sum()
    # 计算sell_1大单交易比例和成交总量比例
    sell_1_ratio = sell_1.shape[0] / sell.shape[0]
    sell_1_amount_ratio = sell_1.sum() / sell.sum()
    
    # 计算buy_2大单交易比例和成交总量比例
    buy_2_ratio = buy_2.shape[0] / buy.shape[0]
    buy_2_amount_ratio = buy_2.sum() / buy.sum()
    # 计算sell_2大单交易比例和成交总量比例
    sell_2_ratio = sell_2.shape[0] / sell.shape[0]
    sell_2_amount_ratio = sell_2.sum() / sell.sum()
    # 计算buy_3大单交易比例和成交总量比例
    buy_3_ratio = buy_3.shape[0] / buy.shape[0]
    buy_3_amount_ratio = buy_3.sum() / buy.sum()
    # 计算sell_3大单交易比例和成交总量比例
    sell_3_ratio = sell_3.shape[0] / sell.shape[0]
    sell_3_amount_ratio = sell_3.sum() / sell.sum()


    # 判断大单buy2是否改变了原有的趋势


    return pd.Series({
        "buy_1_ratio": buy_1_ratio,
        "buy_1_amount_ratio": buy_1_amount_ratio,
        "sell_1_ratio": sell_1_ratio,
        "sell_1_amount_ratio": sell_1_amount_ratio,
        "buy_1_diff2_sum": buy_1_diff2_sum,
        "sell_1_diff2_sum": sell_1_diff2_sum,

        "buy_2_ratio": buy_2_ratio,
        "buy_2_amount_ratio": buy_2_amount_ratio,
        "sell_2_ratio": sell_2_ratio,
        "sell_2_amount_ratio": sell_2_amount_ratio,
        "buy_2_diff2_sum": buy_2_diff2_sum,
        "sell_2_diff2_sum": sell_2_diff2_sum,

        "buy_3_ratio": buy_3_ratio,
        "buy_3_amount_ratio": buy_3_amount_ratio,
        "sell_3_ratio": sell_3_ratio,
        "sell_3_amount_ratio": sell_3_amount_ratio,
        "buy_3_diff2_sum": buy_3_diff2_sum,
        "sell_3_diff2_sum": sell_3_diff2_sum   

    })


# 计算A股成交明细中的大单交易比例

def large_ticket_ratio(df, threshold=1000000):
    """
    计算大单交易比例
    :param df: DataFrame
    :param threshold: int
    :return: float
    """
    large_ticket = df[df['amount'] > threshold]
    return large_ticket.shape[0] / df.shape[0]

# 计算大单交易的价格分布
def large_ticket_price_distribution(df, threshold=1000000, bins=10):
    """
    计算大单交易的价格分布
    :param df: DataFrame
    :param threshold: int
    :param bins: int
    :return: Series
    """
    # 筛选出大单交易
    large_ticket = df[df['amount'] > threshold]
    
    # 计算每笔交易的价格
    large_ticket['price'] = large_ticket['amount'] / large_ticket['volume']
    
    # 划分价格区间
    price_bins = pd.cut(large_ticket['price'], bins=bins)
    
    # 计算每个价格区间的大单交易数量
    price_distribution = large_ticket.groupby(price_bins).size()
    
    return price_distribution


def tick_feature(transaction_df):
    """

    """
    transaction_df["turnover"] = transaction_df["price"] * transaction_df["volume"]
    # 1. 成交量（Volume）

    # 分时段成交量 (例如按5分钟)
    vol = transaction_df.resample('5T', on='datetime')['vol'].sum()
    
    # 2. 成交金额（Turnover）
    # 总成交金额


    # 分时段成交金额 (5分钟)
    turnover = transaction_df.resample('5T', on='datetime')['turnover'].sum()

    # 3. 加权平均成交价（VWAP, Volume Weighted Average Price）
    # VWAP = 总成交金额 / 总成交量
    # 分时段的 VWAP (5分钟)
    vwap = transaction_df.resample('5T', on='datetime')['turnover'].sum() / transaction_df.resample('5T', on='datetime')['vol'].sum()


    # 4. 逐笔买卖方向（Trade Direction）
    # 按买卖方向统计成交量 (5分钟)
    buy_df = transaction_df[transaction_df['buyorsell'] == 0]
    sell_df = transaction_df[transaction_df['buyorsell'] == 1]

    # 按买卖方向统计成交笔数


    # 按买卖方向统计成交金额
    buy_turnover = buy_df.resample('5T', on='datetime')['turnover'].sum()
    sell_turnover = sell_df.resample('5T', on='datetime')['turnover'].sum()

    buy_volume = buy_df.resample('5T', on='datetime')['volume'].sum()
    sell_volume = buy_df.resample('5T', on='datetime')['volume'].sum()



    # 5. 成交密度（Trade Frequency / Trade Intensity）
    # 每分5钟的成交笔数
    trade_frequency = transaction_df.resample('5T', on='datetime')['order'].count()

    
    # 6. 成交量加权价格变化率（Volume Weighted Price Change Rate）
    # 计算价格变化率并加权成交量 (5分钟)



    transaction_df['price_change'] = transaction_df['price'].diff()
    transaction_df['weighted_price_change'] = transaction_df['price_change'] * transaction_df['vol']
    

    # 累加得到加权价格变化率
    # weighted_price_change_rate = transaction_df['weighted_price_change'].sum() / transaction_df['vol'].sum()

    # 7. 交易量不对称性（Volume Imbalance）
    # 计算主动买入和主动卖出的成交量差异
    volume_imbalance = buy_volume - sell_volume
    turnover_imbalance = buy_turnover - sell_turnover
    
    # 8. 价格波动率（Price Volatility）
    # 价格波动率的计算可以通过标准差来度量
    # price_volatility = transaction_df['price'].std()

    # 5分钟计算价格波动率
    price_volatility_per_5min = transaction_df.resample('5T', on='datetime')['price'].std()

    # 9. 资金流向（Capital Flow）  turnover_imbalance
    # 主动买入时的资金流入(5分钟)

    # 主动买入时的资金流入

    # capital_inflow = transaction_df[transaction_df['buyorsell'] == 0]['turnover'].sum()

    # 主动卖出时的资金流出
    # capital_outflow = transaction_df[transaction_df['buyorsell'] == 1]['turnover'].sum()

    # 净资金流入 = 资金流入 - 资金流出
    # net_capital_flow = capital_inflow - capital_outflow

    # 10. 平均每笔交易量（Average Trade Size）
    # 平均每笔交易量(5分钟)

    average_trade_size = transaction_df.resample('5T', on='datetime')['vol'].mean()
    
    # 11. 换手率（Turnover Rate）
    # 换手率 = 总成交量 / 流通股本
    # 假设流通股本 circulating_shares 已知：
    # turnover_rate = total_volume / circulating_shares

    # 12. 逐笔滑点（Slippage per Trade）
    # 计算每笔滑点（假设与前一笔成交价相比）
    transaction_df['slippage'] = transaction_df['price'] - transaction_df['price'].shift(1)

    # 平均滑点
    average_slippage = transaction_df.resample('5T', on='datetime')['slippage'].mean()

    # 13. 大单识别（Large Trade Identification）
    # 识别大单
    # large_trades = transaction_df[transaction_df['vol'] > 1000]

    # # 大单的数量和总量
    # large_trade_count = large_trades.shape[0]
    # large_trade_volume = large_trades['vol'].sum()
    
    #14. 买卖力量对比（Buy vs Sell Volume Ratio）
    # 买卖力量对比 = 买盘成交量 / 卖盘成交量
    # buy_sell_volume_ratio = buy_volume / sell_volume

    # 15. 盘中跳跃（Price Jump Detection）
    # 定义价格跳跃的阈值（例如 1% 的价格变动）
    threshold = 0.01
    transaction_df['price_jump'] = transaction_df['price'].pct_change().abs() > threshold

    # 计算跳跃次数
    price_jump_count = transaction_df.resample('5T', on='datetime')['price_jump'].sum()

    # 16. 时间加权平均价格（TWAP, Time Weighted Average Price）
    # 按时间段内计算 TWAP
    twap_per_minute = transaction_df.resample('5T', on='datetime').apply(lambda x: x['price'].mean())
    
    
    #峰度
    kurtosis_per_minute = transaction_df.resample('5T', on='datetime').apply(lambda x: kurtosis(x['price']))


    features_per_5min = pd.DataFrame({
        'vol': vol,
        'turnover': turnover,
        'buy_volume': buy_volume,
        'sell_volume': sell_volume,
        'buy_turnover': buy_turnover,
        'vwap': vwap,
        'trade_frequency': trade_frequency,   
        'sell_turnover': sell_turnover,
        'volume_imbalance': volume_imbalance,
        'turnover_imbalance': turnover_imbalance,
        'price_volatility_per_5min': price_volatility_per_5min,
        'average_trade_size': average_trade_size,
        'average_slippage': average_slippage,
        'price_jump_count': price_jump_count,
        'twap_per_minute': twap_per_minute,
        'kurtosis_per_minute': kurtosis_per_minute
    })
    features_per_5min["datet"] = features_per_5min.index + pd.Timedelta(minutes=5)
    features_per_5min["datetime"] = features_per_5min["datet"]
    features_per_5min.index = features_per_5min["datetime"]
    features_per_5min = features_per_5min.drop(columns=["datetime"])

    features_per_5min["datemin"] =  features_per_5min["datet"].dt.strftime("%H:%M")
    features_per_5min_choose = features_per_5min[(features_per_5min["datemin"] >= "09:30") & (features_per_5min["datemin"] <= "11:30") | (features_per_5min["datemin"] > "13:00") ]
    # features_per_5min_choose["datetime"] = features_per_5min["datet"]
    return features_per_5min_choose









if __name__ == "__main__":
    pass
    # code = sys.argv[1]
    # run(code)



