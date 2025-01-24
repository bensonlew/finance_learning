# 计算pandas dataframe 每一列的均值，方差 ，丰度， 偏度， 是否符合正态分布， 对每一列取log后再计算一次

import pandas as pd
import numpy as np
import scipy.stats as stats
import os
import sys

def calculate_feature_des(df):
    result_list= []
    for column in df.columns:
        # 跳过非数值列
        if not np.issubdtype(df[column].dtype, np.number):
            continue
        print(column)
        # 计算非na 值的比例
        non_na_ratio = df[column].notna().sum() / len(df[column])
        
        non_na = df[column].notna()
        # 计算非na 值的均值
        non_na_mean = df[column][non_na].mean()
        # 计算非na 值的方差
        non_na_var = df[column][non_na].var()
        non_na_min = df[column][non_na].min()
        # 计算非na 值的偏度
        non_na_skew = df[column][non_na].skew()
        # 计算非na 值的峰度
        non_na_kurt = df[column][non_na].kurt()
        # 计算非na 值的正态性
        stat, non_na_normality = stats.normaltest(df[column][non_na])

        

        # 对数转换后的统计量计算
        # 添加错误处理，避免负数和零值
        positive_values = df[column] > 0

        positive_ratio = df[column][positive_values].notna().sum() / len(df)
    
        log_mean = np.log(df[column][positive_values]).mean()
        log_var = np.log(df[column][positive_values]).var()
        log_skew = np.log(df[column][positive_values]).skew()
        log_kurt = np.log(df[column][positive_values]).kurt()
        _stat,log_normality = stats.normaltest(np.log(df[column][positive_values]))


        feature_dict = {
            "feature_name": column,
            "non_na_ratio": non_na_ratio,
            "non_na_mean": non_na_mean,
            "non_na_min": non_na_min,
            "non_na_var": non_na_var, 
            "non_na_skew": non_na_skew,
            "non_na_kurt": non_na_kurt,
            "non_na_normality": non_na_normality,
            "positive_ratio": positive_ratio,
            "log_mean": log_mean,
            "log_var": log_var,
            "log_skew": log_skew,
            "log_kurt": log_kurt,
            "log_normality": log_normality
        }    
        result_list.append(feature_dict)
    return result_list


if __name__ == "__main__":
    df = pd.read_parquet(sys.argv[1])
    result_list = calculate_feature_des(df)
    result_df = pd.DataFrame.from_records(result_list)
    result_df.to_csv('feature_des.csv', index=False)

