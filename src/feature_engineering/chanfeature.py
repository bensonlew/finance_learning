
import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
import sys

CHAN_FEATURE = [
    "now_seg",
    "last_seg",
    "now_segseg",
    "last_segseg",
]

CHAN_ZS_FEATURE = [
    "now_segzs",
    "last_segzs",
    "now_seg_segzs",
    "now_seg_segzs",
]

ORIGIN_FEATURE = []

def add_seg_feature(a_chan_feature, fearure_origin):
    for chan_fea in CHAN_FEATURE:
        if chan_fea in a_chan_feature:
            for org_fea in ORIGIN_FEATURE:
                fea_name = chan_fea + "__" + org_fea + "__mean"
                a_chan_feature[fea_name] = fearure_origin[a_chan_feature[chan_fea]['begin']:a_chan_feature[chan_fea]['end']][org_fea].mean()

def add_zs_feature(a_chan_feature, fearure_origin):
    for chan_fea in CHAN_ZS_FEATURE:
        if chan_fea in a_chan_feature and chan_fea[:-2] in a_chan_feature:
            for org_fea in ORIGIN_FEATURE:
                fea_name_before = chan_fea + "__" + org_fea + "__beforezs_mean"
                fea_name_zs = chan_fea + "__" + org_fea + "__zs_mean"
                fea_name_after = chan_fea + "__" + org_fea + "__afterzs_mean"
                
                if chan_fea == "last_segzs":
                    zs_list = a_chan_feature["last_segzs"]
                    seg = a_chan_feature["last_seg"]
                elif chan_fea == "now_segzs":
                    zs_list = a_chan_feature["now_segzs"]
                    seg = a_chan_feature["now_seg"]
                elif chan_fea == "now_seg_segzs":
                    zs_list = a_chan_feature["now_seg_segzs"]
                    seg = a_chan_feature["now_segseg"]
                elif chan_fea == "last_seg_segzs":
                    zs_list = a_chan_feature["last_seg_segzs"]
                    seg = a_chan_feature["last_segseg"]
                
                
                if len(zs_list) > 0:
                    a_chan_feature[fea_name_zs] = fearure_origin[zs_list[-1]['begin']:zs_list[-1]['end']][org_fea].mean()
                    a_chan_feature[fea_name_after] = fearure_origin[zs_list[-1]['end']:seg['end']][org_fea].mean()
                    if len(zs_list) > 1:
                        a_chan_feature[fea_name_before] = fearure_origin[zs_list[-2]['end']:zs_list[-1]['begin']][org_fea].mean()
                    else:
                        a_chan_feature[fea_name_before] = fearure_origin[seg['begin']:zs_list[-1]['begin']][org_fea].mean()


code = sys.argv[1]
fearure_origin = pd.read_parquet("../{}.qfq.kdj.parquet".format(code))
columns = fearure_origin.columns
ORIGIN_FEATURE = [c for c in fearure_origin.columns if c.startswith("close_") or c.startswith("amount_")]

# with open("feature.tsv", "w") as f:
#     for col in columns:
#         f.write(col + "\n")
chan_feature_file = "{}.feature.libsvm.json".format(code)

feature_list = []
with open(chan_feature_file) as f:
    for line in f:
        cols = line.strip().split("\t")
        feature_list.append([cols[0], cols[1], json.loads(cols[-1])])

with open("{}.feature_chan.all.json".format(code), "w") as f:
    for t, l, a_chan_feature in feature_list:
        add_seg_feature(a_chan_feature, fearure_origin)
        add_zs_feature(a_chan_feature, fearure_origin)
        f.write("{}\t{}\t{}\n".format(t, l, json.dumps(a_chan_feature)))