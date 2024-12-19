# 删除parquet文件的第一天 48行数据
import pandas as pd
import os
import sys

def delete_first_day(file_path):
    df = pd.read_parquet(file_path)
    df = df.iloc[48:]
    df.to_parquet(file_path)


if __name__ == "__main__":
    code_parquet = sys.argv[1]
    delete_first_day(code_parquet)
