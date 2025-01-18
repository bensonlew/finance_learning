from QUANTAXIS.QAData.data_fq import QA_data_etf_to_fq, QA_data_stock_to_fq
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_etf_min, QA_fetch_stock_min, QA_fetch_stock_transaction
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_list
import pymongo
uri = 'mongodb://localhost:27017'
import pandas as pd

client = pymongo.MongoClient(uri)


data_dir = "/data/finance/"


def get_tdx_qfq_etf_min5data(code):
    
    df = QA_fetch_etf_min(code, "2010-01-01", "2030-01-01", format="pd")
    code_hfq = QA_data_etf_to_fq(df, '01')
    a1t = code_hfq["datetime"][0]
    if a1t.hour == 9 & a1t.hour == 35:
        pass
    else:
        code_hfq = code_hfq[code_hfq["date"]>code_hfq["date"][0]]
    print(len(code_hfq))
    if len(code_hfq) % 48 != 0:
        print("{} lack data".format(code))
    else:
        print("{} ok".format(code))
    code_hfq.to_parquet(data_dir + "{}.qfq.parquet".format(code))


def get_tdx_qfq_stock_min5data(code):
    df = QA_fetch_stock_min(code, "2010-01-01", "2030-01-01", format="pd", frequence="5min")
    code_hfq = QA_data_stock_to_fq(df, '01', '5min')
    a1t = code_hfq["datetime"][0]
    if a1t.hour == 9 & a1t.hour == 35:
        pass
    else:
        code_hfq = code_hfq[code_hfq["date"]>code_hfq["date"][0]]
    code_hfq.to_parquet(data_dir + "{}.qfq.parquet".format(code))

def get_tdx_stock_trac(code):
    df = QA_fetch_stock_transaction(code, "2010-01-01", "2030-01-01", format="pd")
    df.to_parquet(data_dir + "{}.transaction.parquet".format(code))




def find2mongo2df():
    coll = client.quantaxis.stock_min
    records = coll.find({"time_stamp" : 1632274500.0, "amount": {"$gt": 2000000.0}})
    return records

def find2mongo2df_etfranked():
    coll = client.quantaxis.etf_rank
    records = coll.find({"date":"2023-12-04"})
    return records

def get_etf_code_list():
    __index_list = QA_fetch_get_stock_list('etf')
    return list(__index_list["code"])


if __name__ == "__main__":
    # records = find2mongo2df()
    # records = find2mongo2df_etfranked()
    # code_list = [record["code"][2:] for record in records]
    code_list = get_etf_code_list()
    # for record in records:
    #     code = record["code"]
    #     print(code)
    #     get_tdx_qfq_stock_min5data(code)

    # for record in records:
    #     code = record["code"]
    #     print(code)
    #     get_tdx_stock_trac(code)



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
    # code_list = ["510050", "512100", "510880", "512690", "159915", "000016", "000852", "399006"]
    for code in code_list:
        print("code {}".format(code))
        try:
            get_tdx_qfq_etf_min5data(code)
        except:
            print("error {}".format(code))


