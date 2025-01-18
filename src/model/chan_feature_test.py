import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
import sys
import xgboost as xgb
import glob
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import os

chan_feature_files = glob.glob(sys.argv[1])
time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

if os.path.exists("chan_feature_df.parquet"):
    chan_feature_df = pd.read_parquet("chan_feature_df.parquet")
else:
    feature_list = []
    for chan_feature_file in chan_feature_files:
        print(chan_feature_file)
        with open(chan_feature_file) as f:
            for line in f:
                cols = line.strip().split("\t")
                if cols[1] not in ["1low", "1high", "2low", "2high", "0"]:
                    continue
                try:
                    fea_dict = json.loads(cols[-1])
                    fea_dict["time"] = cols[0]
                    fea_dict["label"] = cols[1]
                    feature_list.append(fea_dict)
                except Exception as e:
                    print("error {} {}".format(chan_feature_file, line))



    chan_feature_df = pd.DataFrame(feature_list)
    chan_feature_df.to_parquet("chan_feature_df.parquet")
# chan_feature_df = pd.read_parquet("chan_feature_df.parquet")
# frange__now_seg__range: object, fcmp__now_seg__range_rate12_cmp: object, fcmp__now_seg__range_rate13_cmp: object, feachan__last_seg__is_sure: object, frange__last_seg__range: object, fcmp__last_seg__range_rate12_cmp:
#  object, fcmp__last_seg__range_rate13_cmp: object, frange__now_seg__zs1: object, frange__now_seg__zs1after: object, frange__now_seg__zs1before: object, frange__last_seg__zs1: object, frange__last_seg__zs1after: 
# object, frange__last_seg__zs1before: object, feachan__now_segseg__is_sure: object, frange__now_segseg__range: object, feachan__last_segseg__is_sure: object, frange__last_segseg__range: object, fcmp__now_segseg__
# range_rate12_cmp: object, fcmp__now_segseg__range_rate13_cmp: object, fcmp__last_segseg__range_rate12_cmp: object, fcmp__last_segseg__range_rate13_cmp: object, frange__now_segseg__zs1: object, frange__now_segseg
# __zs1after: object, frange__now_segseg__zs1before: object, frange__last_segseg__zs1: object, frange__last_segseg__zs1after: object, frange__last_segseg__zs1before
print("read data finish")


X_drop_list = ["now_seg", "last_seg", "now_segseg", "last_segseg", "now_segzs", "last_segzs", "now_seg_segzs", "last_seg_segzs"]

X_drop_list += ["time", "label"]
X_drop_list += [c for c in chan_feature_df.columns if c.startswith("fcmp__") or c.startswith("frange__") or c.startswith("fpoint__") or c.endswith("__is_sure")]

X_contain = [c for c in chan_feature_df.columns if c not in X_drop_list]
y_train = chan_feature_df["label"]
# X_train = train
y_train[y_train=="1low"] = 3
y_train[y_train=="1high"] = 1
y_train[y_train=="2low"] = 4
y_train[y_train=="2high"] = 2
y_train[y_train=="0"] = 0
for fea in X_contain:
    X_train = chan_feature_df[[fea]]
    try:
        dtrain = xgb.DMatrix(X_train, label=y_train)
        print("{} ok".format(fea))
    except Exception as e:
        print("{} err".format(fea))
        print(e)


