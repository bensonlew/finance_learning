#获取指定ETF分时数据
import pandas as pd
import matplotlib.pyplot as plt
import akshare as ak
import datetime
import os
import sys
 

now = datetime.datetime.now().strftime("%y%m%d")

# index_stock_info_df = ak.index_stock_info()

# index_stock_info_df.to_csv("index_stock_info.csv", sep="\t")
index_list = [
    "sh510050",
    "sh512100",
    "sh563000",
    "sh560050",
    "sh510300",
    "sh510330",
    "sh561300",
    "sh561990",
	"sh510500",
	"sh561550",
	"sh512500",
	"sz159845",
	"sz159949",
	"sz159915",
	"sz159967",
	"sh588000",
	"sh588080",
	"sh588050",
    "sh515790",
    "sh512480",
    "sh512760",
    "sz159995",
    "sh512660",
    "sh516160",
    "sh515030",
    "sh515700",
    "sz159611",
    "sh516010",
    "sh515050",
    "sh512880",
    "sh512000",
    "sh512070",
    "sh512800",
    "sh512200",
    "sh510880",
    "sz159905",
    "sh516950",
    "sz159745",
    "sz159825",
    "sz159867", 
    "sh515790",
    "sh512480",
    "sh512760",
    "sz159995",
    "sh512660",
    "sh516160",
    "sh515030",
    "sh515700",
    "sz159611",
    "sh516010",
    "sh515050",
    "sh512880",
    "sh512000",
    "sh512070",
    "sh512800",
    "sh512200",
    "sh510880",
    "sz159905",
    "sh516950",
    "sz159745",
    "sz159825",
    "sz159867"
]

index_dict = {
    "sh510050": "上证50ETF",
    "sh563000": "中国A50ETF",
    "sh560050": "MSCI中国A50ETF",
    "sh510300": "沪深300ETF",
    "sh510330": "300ETF基金",
    "sh561300": "300增强ETF",
    "sh561990": "沪深300增强ETF",
    "sh510500": "中证500ETF",
    "sh561550": "500增强ETF",
    "sh512500": "500ETF基金",
    "sz159845": "中证1000ETF",
    "sh512100": "中证1000ETF",
    "sz159949": "创业板50ETF",
    "sz159915": "创业板ETF",
    "sz159967": "创成长ETF",
    "sh588000": "科创50ETF",
    "sh588080": "科创板50ETF",
    "sh588050": "科创ETF",
    "sh515790": "光伏ETF",
    "sh512480": "半导体ETF",
    "sh512760": "芯片ETF",
    "sz159995": "芯片ETF",
    "sh512660": "军工ETF",
    "sh516160": "新能源ETF",
    "sh515030": "新能源车ETF",
    "sh515700": "新能车ETF",
    "sz159611": "电力ETF",
    "sh516010": "游戏ETF",
    "sh515050": "5GETF",
    "sh512880": "证券ETF",
    "sh512000": "券商ETF",
    "sh512070": "证券保险ETF",
    "sh512800": "银行ETF",
    "sh512200": "房地产ETF",
    "sh510880": "红利ETF",
    "sz159905": "深红利ETF",
    "sh516970": "基建50ETF",
    "sh516950": "基建ETF",
    "sz159745": "建材ETF",
    "sz159825": "农业ETF",
    "sz159865": "养殖ETF",
    "sz159867": "畜牧ETF",
    "sz159605": "中概互联ETF",
    "sh513180": "恒生科技指数ETF",
    "sh513130": "恒生科技ETF",
    "sh513010": "恒生科技30ETF",
    "sz159920": "恒生ETF",
    "sh510900": "H股ETF",
    "sh513060": "恒生医疗ETF",
    "sh512010": "医药ETF",
    "sh512170": "医疗ETF",
    "sh512290": "生物医药ETF",
    "sh512690": "酒ETF",
    "sz159928": "消费ETF",
    "sz159996": "家电ETF",
    "sz159766": "旅游ETF",
    "sh515220": "煤炭ETF",
    "sh515210": "钢铁ETF",
    "sh516780": "稀土ETF",
    "sh512400": "有色金属ETF",
    "sh511380": "可转债ETF",
    "sh513500": "标普500ETF",
    "sh513100": "纳指ETF",
}

def get_min_data(start_date):
    for index in index_dict.keys():
        try:
            stock_zh_index_5_min_df = ak.stock_zh_a_minute(symbol=index, period='5', adjust="qfq")
            stock_zh_index_5_min_df = stock_zh_index_5_min_df[stock_zh_index_5_min_df["day"]>start_date]
            stock_zh_index_5_min_df.to_csv("sh_etf_data" + "/" + index + "_" + now + ".5.tsv", sep="\t")

        except Exception as e:
            print(e)

def get_day_data():
    for index in index_dict.keys():
        try:
            # if os.path.exists("sh_etf_data" + "/" + index + "_" + "daily" + ".tsv"):
            #     pass
            # else:
                stock_zh_index_daily_df = ak.stock_zh_index_daily(symbol=index)
                stock_zh_index_daily_df.to_csv("sh_etf_data" + "/" + index + "_" + "daily" + ".tsv", sep="\t")
                print("get {}".format(index))

        except Exception as e:
            print(index)
            print(e)

if __name__ == '__main__':
    # get_day_data()
    if len(sys.argv) >= 2:
        start_date = sys.argv[1]
        if len(start_date) == 8:
            start_date = start_date[:4] + "-" + start_date[4:6] + "-" + start_date[6:]
        get_min_data(start_date)
    else:
        get_day_data()