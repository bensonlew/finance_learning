# from QUANTAXIS.QAData.data_fq import QA_data_etf_to_fq, QA_data_stock_to_fq
import pymongo
from QUANTAXIS.QAFetch.QAQuery import (QA_fetch_etf_min,
                                       QA_fetch_index_transaction,
                                       QA_fetch_etf_transaction,
                                       QA_fetch_stock_min,
                                       QA_fetch_stock_transaction)

uri = 'mongodb://localhost:27017'
import pandas as pd

client = pymongo.MongoClient(uri)


data_dir = "/liubinxu/liubinxu/finance/learning/data/"




def get_tdx_index_trac(code):
    df = QA_fetch_index_transaction(code, "2010-01-01", "2030-01-01", format="pd")
    df.to_parquet(data_dir + "{}.transaction.parquet".format(code))

def get_tdx_etf_trac(code):
    df = QA_fetch_etf_transaction(code, "2010-01-01", "2030-01-01", format="pd")
    df.to_parquet(data_dir + "{}.transaction.parquet".format(code))


if __name__ == "__main__":
    # records = find2mongo2df()




    # code_list = [
    #     "510050",
    #     "510300",
    #     "510330",
    #     "510500",
    #     "510880",
    #     "510900",
    #     "511380",
    #     "512000",
    #     "512010",
    #     "512070",
    #     "512100",
    #     "512100",
    #     "512170",
    #     "512200",
    #     "512290",
    #     "512400",
    #     "512480",
    #     "512500",
    #     "512660",
    #     "512690",
    #     "512760",
    #     "512800",
    #     "512880",
    #     "513010",
    #     "513060",
    #     "513100",
    #     "513130",
    #     "513180",
    #     "513500",
    #     "515030",
    #     "515050",
    #     "515210",
    #     "515220",
    #     "515700",
    #     "515790",
    #     "516010",
    #     "516160",
    #     "516780",
    #     "516950",
    #     "516970",
    #     "560050",
    #     "561300",
    #     "561550",
    #     "561990",
    #     "563000",
    #     "588000",
    #     "588050",
    #     "588080",
    #     "159605",
    #     "159611",
    #     "159745",
    #     "159766",
    #     "159825",
    #     "159845",
    #     "159865",
    #     "159867",
    #     "159905",
    #     "159915",
    #     "159920",
    #     "159928",
    #     "159949",
    #     "159967",
    #     "159995",
    #     "159996"
    # ]
    code_list = ["510050", "512100", "510880", "512690", "159915", "000016", "000852", "399006"]
    for code in code_list[:4]:
        get_tdx_etf_trac(code)



