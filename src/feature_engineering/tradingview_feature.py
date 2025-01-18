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
from scipy import stats

def calculate_obv(close, volume):
    obv = [0]
    for i in range(1, len(close)):
        if close[i] > close[i-1]:
            obv.append(obv[-1] + volume[i])
        elif close[i] < close[i-1]:
            obv.append(obv[-1] - volume[i])
        else:
            obv.append(obv[-1])
    return obv

def calculate_macd(close, fast=12, slow=26, signal=9):
    # 计算快线和慢线的EMA
    exp1 = close.ewm(span=fast, adjust=False).mean()
    exp2 = close.ewm(span=slow, adjust=False).mean()
    
    # 计算MACD线
    macd = exp1 - exp2
    # 计算信号线
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    
    return macd, signal_line

def obv_macd_indicator(df):
    """
    计算OBV MACD指标
    
    参数:
    df: DataFrame，需要包含'close'和'volume'列
    
    返回:
    tt1: 最终的指标线
    """
    # 1. 计算OBV
    obv = calculate_obv(df['close'], df['volume'])
    
    # 2. 将OBV转换为pandas Series
    obv_series = pd.Series(obv)
    
    # 3. 计算OBV的MACD
    macd_line, signal_line = calculate_macd(obv_series)
    
    # 4. 计算最终指标线tt1
    tt1 = macd_line - signal_line
    
    return tt1

# 使用示例
def generate_signals(df):
    """
    生成交易信号
    """
    tt1 = obv_macd_indicator(df)
    
    signals = pd.Series(index=df.index, data=np.nan)
    signals[tt1 > 0] = 1    # 买入信号
    signals[tt1 < 0] = -1   # 卖出信号
    
    return signals


import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from typing import Tuple

class MLRSI:
    def __init__(self, period: int = 14, smooth_period: int = 3, clusters: int = 3):
        """
        初始化 ML-RSI 指标
        
        参数:
            period (int): RSI 计算周期
            smooth_period (int): 平滑周期
            clusters (int): 聚类数量
        """
        self.period = period
        self.smooth_period = smooth_period
        self.clusters = clusters
        
    def calculate_rsi(self, data: pd.Series) -> pd.Series:
        """计算传统 RSI"""
        delta = data.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def smooth_rsi(self, rsi: pd.Series) -> pd.Series:
        """使用简单移动平均进行平滑处理"""
        return rsi.rolling(window=self.smooth_period).mean()
    
    def calculate_dynamic_thresholds(self, rsi: pd.Series) -> Tuple[float, float]:
        """使用 K-means 计算动态阈值"""
        # 将 RSI 值重塑为二维数组
        X = rsi.dropna().values.reshape(-1, 1)
        
        # 应用 K-means 聚类
        kmeans = KMeans(n_clusters=self.clusters, random_state=42)
        kmeans.fit(X)
        
        # 获取聚类中心并排序
        centers = sorted(kmeans.cluster_centers_.flatten())
        
        # 返回超卖和超买阈值
        return centers[0], centers[-1]
    
    def generate_signals(self, data: pd.Series) -> pd.DataFrame:
        """生成交易信号"""
        # 计算 RSI
        rsi = self.calculate_rsi(data)
        
        # 平滑处理
        smooth_rsi = self.smooth_rsi(rsi)
        
        # 计算动态阈值
        oversold, overbought = self.calculate_dynamic_thresholds(smooth_rsi)
        
        # 生成信号
        signals = pd.DataFrame(index=data.index)
        signals['RSI'] = smooth_rsi
        signals['Overbought'] = overbought
        signals['Oversold'] = oversold
        signals['Buy_Signal'] = (smooth_rsi < oversold).astype(int)
        signals['Sell_Signal'] = (smooth_rsi > overbought).astype(int)
        
        return signals

# 使用示例
if __name__ == "__main__":
    # 创建示例数据
    import yfinance as yf
    
    # 下载比特币数据作为示例
    btc = yf.download('BTC-USD', start='2023-01-01', end='2024-01-01')
    
    # 初始化 ML-RSI
    ml_rsi = MLRSI(period=14, smooth_period=3, clusters=3)
    
    # 计算信号
    signals = ml_rsi.generate_signals(btc['Close'])
    
    # 打印结果
    print("\n最后 5 条记录:")
    print(signals.tail())
    
    # 计算胜率
    total_signals = signals['Buy_Signal'].sum() + signals['Sell_Signal'].sum()
    print(f"\n总信号数: {total_signals}")


class LinearRegressionOscillator:
    def __init__(self, period=14, overbought=80, oversold=20):
        """
        初始化线性回归振荡器
        
        参数:
            period (int): 计算周期
            overbought (float): 超买水平
            oversold (float): 超卖水平
        """
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        
    def calculate(self, prices):
        """
        计算线性回归振荡器值
        
        参数:
            prices (np.array): 价格序列
        返回:
            dict: 包含振荡器值和信号的字典
        """
        results = {
            'oscillator': [],
            'signals': [],
            'upper_band': [],
            'lower_band': []
        }
        
        # 确保有足够的数据
        if len(prices) < self.period:
            return results
            
        for i in range(self.period, len(prices)):
            # 获取当前周期的价格
            window = prices[i-self.period:i]
            
            # 计算线性回归
            x = np.arange(len(window))
            slope, intercept, r_value, _, _ = stats.linregress(x, window)
            
            # 计算回归线
            reg_line = x * slope + intercept
            
            # 计算当前价格与回归线的偏离程度
            current_deviation = (window[-1] - reg_line[-1]) / window[-1] * 100
            
            # 计算标准差通道
            std_dev = np.std(window - reg_line)
            upper = reg_line[-1] + (2 * std_dev)
            lower = reg_line[-1] - (2 * std_dev)
            
            # 生成信号
            signal = 0  # 0表示无信号
            if current_deviation > self.overbought:
                signal = -1  # 卖出信号
            elif current_deviation < self.oversold:
                signal = 1   # 买入信号
                
            # 存储结果
            results['oscillator'].append(current_deviation)
            results['signals'].append(signal)
            results['upper_band'].append(upper)
            results['lower_band'].append(lower)
            
        return results

    def generate_trading_signals(self, prices):
        """
        生成交易信号
        
        参数:
            prices (np.array): 价格序列
        返回:
            pd.DataFrame: 包含交易信号的数据框
        """
        results = self.calculate(prices)
        
        df = pd.DataFrame({
            'price': prices[self.period:],
            'oscillator': results['oscillator'],
            'signal': results['signals'],
            'upper_band': results['upper_band'],
            'lower_band': results['lower_band']
        })
        
        return df




