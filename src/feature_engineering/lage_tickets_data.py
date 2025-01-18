import pandas as pd
from src.feature_engineering.large_tickets import *
import sys
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list


def run(code, type="etf"):
    # code = "601360"
    fdata_dir = os.environ.get('FDATA', '/data/finance/')
    # if os.path.exists(fdata_dir + "/large_tickets_data/{}.parquet".format(code)):``
    #     print("code {} exists")
    #     return True
    fd = "2010-01-01"
    td = "2030-01-01"
    df1 = get_5minutes_data(code, type=type, from_date=fd, to_date=td)
    # df1.to_csv(fdata_dir + "/large_tickets_data/{}.csv".format(code))
    transaction_df, df_grouped = get_transaction_data(code, type=type, from_date=fd, to_date=td)
    transaction_df.to_parquet(fdata_dir + "/large_tickets_data/{}_transaction.parquet".format(code))
    df_grouped.to_parquet(fdata_dir + "/large_tickets_data/{}_grouped.parquet".format(code))



    # large_stat_time_df = df1.apply(large_stat_time, transaction_df=transaction_df, day_stat_df=df_grouped, axis=1)
    # # large_stat_time_df.to_parquet(fdata_dir + "/large_tickets_data/{}.parquet".format(code))
    # # transaction_df.to_parquet(fdata_dir + "/large_tickets_data/{}_transaction.parquet".format(code))
    # tick_features = tick_feature(transaction_df)
    # # tick_features.to_parquet(fdata_dir + "/large_tickets_data/{}_tick_feature.parquet".format(code))
    # large_stat_time_df = large_stat_time_df.merge(tick_features, on="datetime", how="left")
    # large_stat_time_df.to_parquet(fdata_dir + "/large_tickets_data/{}.parquet".format(code))

def get_etf_code_list():
    delele_code = [
        "159670",
        "159690",
        "159696",
        "159698",
        "159697",
        "159695",
        "159692",
        "159699",
        "159966",
        "159965",
        "159969",
        "159967",
        "159968",
        "159970",
        "159971",
        "159972",
        "159975",
        "159974",
        "159973",
        "159977",
        "159980",
        "159976",
        "159983",
        "159982",
        "159985",
        "159981",
        "159987",
        "159991",
        "159990",
        "159992",
        "159995",
        "159993",
        "159994",
        "159998",
        "159997",
        "159996",
        "515220",
        "561550",
        "561990",
        "561300",
        "560050",
        "563000",
        "588050",
        "588000",
        "588080",
        "159670",
        "159690",
        "159696",
        "159698",
        "159697",
        "159695",
        "159692",
        "159699",
        "159966",
        "159965",
        "159969",
        "159967",
        "159968",
        "159970",
        "159971",
        "159972",
        "159975",
        "159974",
        "159973",
        "159977",
        "159980",
        "159976",
        "159983",
        "159982",
        "159985",
        "159981",
        "159987",
        "159991",
        "159990",
        "159992",
        "159995",
        "159993",
        "159994",
        "159998",
        "159997",
        "159996",
        "515220",
        "561550",
        "561990",
        "561300",
        "560050",
        "563000",
        "588050",
        "588000",
        "588080"
    ]
    # return delele_code
    a = QA_fetch_get_stock_list("etf")
    return list(a["code"])

if __name__ == "__main__":
    # code = sys.argv[1]
    type = sys.argv[2]
    for code in get_etf_code_list():
        try:
            print("get code %s" % code)
            run(code, type=type)
        except Exception as e:
            print(e)