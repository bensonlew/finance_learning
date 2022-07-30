# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd
import datetime

sh000001 = ak.stock_zh_index_daily(symbol="sh000001")

sh000001_choose = sh000001[["date", "close"]]
fund_name_em_df = ak.fund_name_em()
with open("fundcorr.tsv", 'w') as f:
    for fund in fund_name_em_df.iterrows():
        try:
            fund_dict = dict(fund[1])
            fund_code = fund_dict["基金代码"]
            print(fund_dict)
            fund = ak.fund_open_fund_info_em(fund=fund_code)
            if len(fund) < 100:
                continue
            fund_choose = fund[["净值日期", "单位净值"]]
            fund_choose.rename(
                columns={"净值日期": "date", "单位净值": "jinzhi"}, inplace=True)

            mergepd = pd.merge(sh000001_choose, fund_choose,
                            on=["date", "date"], how="inner")
            mergepd.corr("pearson")
            all_corr = mergepd.corr()["close"]["jinzhi"]

            a1 = datetime.date(year=2021, month=1, day=1)
            a2 = datetime.date(year=2019, month=1, day=1)
            a3 = datetime.date(year=2015, month=1, day=1)

            mergepd_choose1 = mergepd[mergepd["date"] > a1]
            all_corr1 = mergepd_choose1.corr()["close"]["jinzhi"]
            mergepd_choose2 = mergepd[mergepd["date"] > a2]
            all_corr2 = mergepd_choose2.corr()["close"]["jinzhi"]
            mergepd_choose3 = mergepd[mergepd["date"] > a3]
            all_corr3 = mergepd_choose3.corr()["close"]["jinzhi"]

            date_start = mergepd['date'][0]
            table_row = [fund_dict.get("基金简称", ""), fund_dict["基金代码"], all_corr, all_corr1, all_corr2, all_corr3, date_start]
            print("\t".join(map(str, table_row)))

            f.write("\t".join(map(str, table_row)) + "\n")
        except Exception as e:
            print("error {}".format(e))