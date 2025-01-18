from operator import index
import os
import zipfile
import pandas as pd
import akshare as ak
from sklearn.linear_model import LinearRegression
import numpy as np


furure_dict = {
    "000300": "IF",
    "000016": "IH",
    "000905": "IC",
    "000852": "IM"

}

def process_zip_files(directory):
    # 用于存储所有CSV数据
    all_data = []
    
    # 遍历目录中的所有zip文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                
                # 打开并解压zip文件
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    # 获取zip中的所有csv文件
                    for csv_file in zip_ref.namelist():
                        print(csv_file)
                        if csv_file.endswith('.csv'):
                            # 读取csv文件为DataFrame
                            with zip_ref.open(csv_file) as f:
                                df = pd.read_csv(f, encoding='GBK')
                                # 添加一个新列，用于记录表格名称（csv文件名）
                                df['table_name'] = csv_file.split(".")[0]
                                # 将数据追加到列表中
                                all_data.append(df)

    # 合并所有DataFrame为一张表
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df




def get_index_future_data(future_type, combined_data):
    ifs = [c.startswith(future_type) for c in combined_data["合约代码"]]
    if_data = combined_data[ifs]

    if_data['duplicate_order'] = if_data.groupby('table_name').cumcount() + 1
    # if_data

    if_order1_data =  if_data[if_data["duplicate_order"] == 1]
    if_order1_data.sort_values(by=["table_name"], inplace=True)
    if_order1_data.reset_index(inplace=True)

    if_order2_data =  if_data[if_data["duplicate_order"] == 2]
    if_order2_data.sort_values(by=["table_name"], inplace=True)
    if_order2_data.reset_index(inplace=True)

    if_order3_data =  if_data[if_data["duplicate_order"] == 3]
    if_order3_data.sort_values(by=["table_name"], inplace=True)
    if_order3_data.reset_index(inplace=True)

    if_order4_data =  if_data[if_data["duplicate_order"] == 4]
    if_order4_data.sort_values(by=["table_name"], inplace=True)
    if_order4_data.reset_index(inplace=True)

    for df in [if_order1_data, if_order2_data, if_order3_data, if_order4_data]:
        print(len(df))

    if_data_df = pd.DataFrame(
        {
            future_type +  '_1': if_order1_data["今收盘"], 
            future_type +  '_2': if_order2_data["今收盘"],
            future_type +  '_3': if_order3_data["今收盘"], 
            future_type +  '_4': if_order4_data["今收盘"],
        })
    # print(if_data_df)
    if_data_df["table_name"] = if_order1_data["table_name"]

    if_data_df["date"] = if_data_df["table_name"].map(lambda x: x.split("_")[0])
    if_data_df['date'] = pd.to_datetime(if_data_df['date'], format='%Y%m%d')
    if_data_df.set_index("date", inplace=True)

    return if_data_df


def get_index_day_data(index_code, future_type=""):


    # 获取沪深300指数的历史数据
    # df000001 = ak.index_zh_a_hist(symbol="000001", period="daily", start_date="20200101", end_date="20241231")
    print(index_code)
    print(future_type)
    index_df = ak.index_zh_a_hist(symbol=index_code, period="daily", start_date="20140101", end_date="20241231")
    df_choose = index_df[["日期", "收盘"]]
    df_choose.columns  = ["date", future_type + "_now"]
    df_choose['date'] = pd.to_datetime(df_choose['date'], format='%Y-%m-%d')
    df_choose.set_index("date",inplace=True)
    return df_choose

def get_index_future_feature(index_code, future_type, combined_data):
    index_df = get_index_day_data(index_code, future_type)
    print(index_df)
    if_data_df = get_index_future_data(future_type, combined_data)
    print(if_data_df)

    df_merge = pd.merge(index_df, if_data_df, how="left", left_index=True, right_index=True)

    print(df_merge)
    for time_dis in [1 ,2 ,3, 4]:  
        df_merge[future_type + '_basis_{}'.format(time_dis)] = (df_merge[future_type +  '_{}'.format(time_dis)] - df_merge[future_type +  '_now']) / df_merge[future_type +  '_now']

    time_to_maturity = np.array([1, 2, 3, 4]).reshape(-1, 1)

    # 计算斜率因子
    def calculate_slope(row):
        prices = np.array([row[future_type +  '_1'], row[future_type +  '_2'], row[future_type +  '_3'], row[future_type +  '_4']]).reshape(-1, 1)
        try:
            model = LinearRegression().fit(time_to_maturity, prices)
            return model.coef_[0][0]
        except: 
            return np.nan

    df_merge[future_type + '_slope'] = df_merge.apply(calculate_slope, axis=1)

    # 计算曲率因子
    df_merge[future_type + '_curvature13'] = df_merge[future_type +  '_1'] - 2 * df_merge[future_type +  '_2'] + df_merge[future_type +  '_3']
    df_merge[future_type + '_curvature24'] = df_merge[future_type +  '_2'] - 2 * df_merge[future_type +  '_3'] + df_merge[future_type +  '_4']
    df_merge[future_type + '_curvature14'] = df_merge[future_type +  '_1'] -  df_merge[future_type +  '_2']-  df_merge[future_type +  '_3'] + df_merge[future_type +  '_4']


    for time_dis in [1 ,2 ,3, 4]:  
        df_merge[future_type + '_basis_change_{}'.format(time_dis)] = df_merge[future_type + '_basis_{}'.format(time_dis)] - df_merge[future_type + '_basis_{}'.format(time_dis)].shift()
    
    return df_merge

if __name__ == '__main__':
    if not os.path.exists('combined_data.csv'):
        # 指定目录路径
        directory_path = '/liubinxu/liubinxu/future'
        combined_data = process_zip_files(directory_path)
        combined_data.to_csv('combined_data.csv', index=False)
        print("合并完成，保存到 combined_data.csv")
    else:
        combined_data = pd.read_csv('combined_data.csv')

    for index_code, future_type in furure_dict.items():
        future_data = get_index_future_feature(index_code, future_type, combined_data)
        future_data.to_csv('future_data_{}.csv'.format(index_code))