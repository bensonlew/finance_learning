# coding:utf-8
# 初始化通达信下载的历史数据


from http import client
from re import S
from QUANTAXIS.QAUtil.QASetting import QA_Setting
import glob
import pymongo
import pandas as pd
from QUANTAXIS.QAUtil.QADate import QA_util_time_stamp, QA_util_date_stamp
from QUANTAXIS.QAUtil import QA_util_to_json_from_pandas
import os

QASETTING = QA_Setting()
DATABASE = QASETTING.client.quantaxis
client = DATABASE
coll = client.stock_min
coll.create_index(
    [
        ('code',
            pymongo.ASCENDING),
        ('time_stamp',
            pymongo.ASCENDING),
        ('date_stamp',
            pymongo.ASCENDING)
    ]
)

def df_insert2mongo(file1):
    data =pd.read_table(file1,index_col=0)
    code = os.path.basename(file1).split("_")[0]
    data = data \
                .assign(datetime=pd.to_datetime(data['datetime'], utc=False),
                        code=code) \
                .drop(['year', 'month', 'day', 'hour', 'minute'], axis=1,
                    inplace=False) \
                .assign(code=code,
                        date=data['datetime'].apply(lambda x: str(x)[0:10]),
                        date_stamp=data['datetime'].apply(
                            lambda x: QA_util_date_stamp(x)),
                        time_stamp=data['datetime'].apply(
                            lambda x: QA_util_time_stamp(x)),
                        type='5min').set_index('datetime', drop=False,
                                            inplace=False)

    if len(data) > 1:
        coll.insert_many(
            QA_util_to_json_from_pandas(data[1::])
        )

if __name__ == '__main__':
    import sys
    file1 = sys.argv[1]
    df_insert2mongo(file1)




