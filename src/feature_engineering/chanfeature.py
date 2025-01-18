
# from more_itertools import last
import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
import sys
import os


"""
特征说明
fpoint_.*_end: 段结束时间
frange_.*_range: 段范围
frange_.*_range_mean: 段范围均值
frange_.*_range_diff: 段范围差值
frange_.*_range_diff_rate: 段范围差值变化率
fcmp_.*_range_rate12_cmp: 段和倒数第二段比较
fcmp_.*_range_rate13_cmp: 段和倒数第三段比较
feachan_.*_zs_rate1: 段和最后一个中枢比较
feachan_.*_zs_rate2: 段和倒数第二个中枢比较
feachan_.*_zs_peak_recall_rate: 段和最后一个中枢高点和低点比较
"""

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


def no_zs_time_rate(bi_ranges):
    '''
    range_rate12 倒数第一笔和倒数第三笔的时间比
    range_rate13 倒数第一笔和倒数第五笔的时间比
    range_rate12_cmp 倒数第一笔和倒数第三笔的时间段
    range_rate13_cmp 倒数第一笔和倒数第五笔的时间段
    '''
    if len(bi_ranges) >= 5:
        bi_ranges = bi_ranges
        last_bi_time = bi_ranges[-1][1] - bi_ranges[-1][0]
        last_2_bi_time = bi_ranges[-3][1] - bi_ranges[-3][0]
        last_3_bi_time = bi_ranges[-5][1] - bi_ranges[-5][0]
        range_rate12 = float(last_bi_time) / last_2_bi_time
        range_rate13 = float(last_bi_time) / last_3_bi_time
        range_rate12_cmp = [bi_ranges[-1], bi_ranges[-3]]
        range_rate13_cmp = [bi_ranges[-1], bi_ranges[-5]]
    elif len(bi_ranges) >= 3:
        bi_ranges = bi_ranges
        last_bi_time = bi_ranges[-1][1] - bi_ranges[-1][0]
        last_2_bi_time = bi_ranges[-3][1] - bi_ranges[-3][0]
        range_rate12 = float(last_bi_time) / last_2_bi_time
        range_rate13 = None
        range_rate12_cmp = [bi_ranges[-1], bi_ranges[-3]]
        range_rate13_cmp = None
    else:
        range_rate12 = None
        range_rate13 = None
        range_rate12_cmp = None
        range_rate13_cmp = None

    return range_rate12, range_rate13, range_rate12_cmp, range_rate13_cmp


def chan_feature_type(a_chan_feature):
    '''
    1、上一段中枢数量、 出中枢后终结有几段
    2、最后一段中枢时间占总数的比例
    3、多段中枢高低点是否有重叠
    4、当前是当前段的第几笔，三笔以上， 三笔的高点是否超过第一笔
    5、fpoint 计算时间点的特征, frange 计算时间段的特征, fcmp 计算比较时间段
    '''
    for seg_fea in CHAN_FEATURE:
        # 循环计算每一个段， 和父级别段
        if seg_fea not in a_chan_feature:
            continue
        feas = ["support_trend_line_slope", "bi_num", "is_sure"]
        for fea in feas:
            a_chan_feature["feachan__" + seg_fea + "__" + fea] = a_chan_feature[seg_fea][fea]
        
        # 添加每个段的结束时间
        # 添加每个段的时间范围
        a_chan_feature["fpoint__" + seg_fea + "__end"] = a_chan_feature[seg_fea]["end"]
        a_chan_feature["frange__" + seg_fea + "__range"] = [a_chan_feature[seg_fea]["begin"], a_chan_feature[seg_fea]["end"]]
        
    for seg_fea,zs_fea in zip(CHAN_FEATURE, CHAN_ZS_FEATURE):
        if seg_fea not in a_chan_feature:
            continue
        feas = []
        zs_num = len(a_chan_feature[zs_fea])
        a_chan_feature["feachan__" + zs_fea + "__" + "num"] = zs_num
        
        if zs_num == 0: # type: ignore
            # 无中枢
            range_rate12, range_rate13, range_rate12_cmp, range_rate13_cmp = no_zs_time_rate(a_chan_feature[seg_fea]["bi_ranges"])

        elif zs_num >= 1: # type: ignore
            # 有中枢 添加中枢结束后的笔的情况
            zs_end = a_chan_feature[zs_fea][-1]["end"]
            bi_ranges = a_chan_feature[seg_fea]["bi_ranges"]
            zs_after_bi_range = []
            for bi_range in bi_ranges:
                if bi_range[1] >= zs_end + 3:
                    zs_after_bi_range.append(bi_range)

            range_rate12, range_rate13, range_rate12_cmp, range_rate13_cmp = no_zs_time_rate(zs_after_bi_range)
        

        # 中枢结束后需要比较的背驰区间
        a_chan_feature["feachan__" + seg_fea + "__" + "range_rate12"] = range_rate12
        a_chan_feature["feachan__" + seg_fea + "__" + "range_rate13"] = range_rate13

        a_chan_feature["fcmp__" + seg_fea + "__" + "range_rate12_cmp"] = range_rate12_cmp
        a_chan_feature["fcmp__" + seg_fea + "__" + "range_rate13_cmp"] = range_rate13_cmp


        zs_rate1, zs_rate2, zs_peak_recall_rate = None, None, None
        if zs_num >= 1: # type: ignore
            # 有中枢
            zs_last = a_chan_feature[zs_fea][-1]
            zs_begin = zs_last["begin"]
            zs_end = zs_last["end"]
            seg_begin = a_chan_feature[seg_fea]["begin"]
            seg_end = a_chan_feature[seg_fea]["end"]
            
            # 最后一个 中枢时间/段时间
            # 最后一个 中枢时间/中枢到该段结束时间
            zs_rate1 = float(zs_end - zs_begin) / (seg_end - seg_begin)
            zs_rate2 = float(zs_end - zs_begin) / (seg_end - zs_begin)

            zs_peak_recall_rate = None
            a_chan_feature["frange__" + seg_fea + "__" + "zs1"] = [zs_begin, zs_end]
            a_chan_feature["frange__" + seg_fea + "__" + "zs1after"] = [zs_end, seg_end]
            a_chan_feature["frange__" + seg_fea + "__" + "zs1before"] = [seg_begin, zs_begin]

            # 中枢前后比较
            a_chan_feature["fcmp__" + seg_fea + "__" + "range_ratezs1ab_cmp"] = [
                [zs_end, seg_end], 
                [seg_begin, zs_begin]
            ]
            # 中枢后和中枢内比较
            a_chan_feature["fcmp__" + seg_fea + "__" + "range_ratezs1az_cmp"] = [
                [zs_end, seg_end], 
                [zs_begin, zs_end]
            ]


        if zs_num >= 2: # type: ignore
            # 有中枢
            zs_last = a_chan_feature[zs_fea][-1]
            zs_last2 = a_chan_feature[zs_fea][-2]
            zs_last_peak_high = zs_last["peak_high"]
            zs_last_peak_low = zs_last["peak_low"]
            zs_last2_peak_high = zs_last2["peak_high"]
            zs_last2_peak_low = zs_last2["peak_low"]
            
            # 中枢高点和低点之间有没有价格重叠（正值有重叠， 负值没有重叠， 上升趋势则反过来）
            if a_chan_feature[seg_fea]["support_trend_line_slope"] < 0:                    
                zs_peak_recall_rate = float(zs_last_peak_high - zs_last2_peak_low) /(zs_last2_peak_high - zs_last_peak_low)
            else:
                zs_peak_recall_rate = - float(zs_last_peak_low - zs_last2_peak_high) /(zs_last_peak_high - zs_last2_peak_low)
            
            # 倒数第二个中枢时间 到倒数第一个中枢时间
            a_chan_feature["frange__" + seg_fea + "__" + "zs1before"] = [zs_last2["end"], zs_begin]

            # 倒数第一个中枢出入比较
            a_chan_feature["fcmp__" + seg_fea + "__" + "range_ratezs2ab_cmp"] = [[zs_end, zs_last["end"]], [zs_last2["begin"], zs_begin]]           
            


        a_chan_feature["feachan__" + seg_fea + "__" + "zs_rate1"] = zs_rate1
        a_chan_feature["feachan__" + seg_fea + "__" + "zs_rate2"] = zs_rate2

        a_chan_feature["feachan__" + seg_fea + "__" + "zs_peak_recall_rate"] = zs_peak_recall_rate



def add_chan_feature(a_chan_feature, fearure_origin):
    '''
    1、是否背驰
    2、最后一个中枢对应的级别
    3、最后一个中枢两端是否有背驰
    4、最两个中枢两端是否有背驰
    5、不是以中枢加一笔结束的情况下 最后一笔和倒数第三笔， 最后一笔和倒数第五笔是否有背驰
    '''
    pass

def add_fvg_feature(a_chan_feature, fearure_origin):
    '''
    获取段中的fvg
    '''
    updown = "down"
    for seg_fea in CHAN_FEATURE:
        seg = a_chan_feature[seg_fea]
        if seg["support_trend_line_slope"] > 0:
            updown = "up"
        bi_ranges = seg["bi_ranges"]
        bi_values = seg["bi_values"]
        fvg_list, fvg_range = identify_fvg(bi_ranges, bi_values, updown)
        a_chan_feature["feachan__" + seg_fea + "__" + "fvg_list"] = fvg_list
        a_chan_feature["feachan__" + seg_fea + "__" + "fvg_range"] = fvg_range

def identify_fvg(bi_ranges, bi_values, updown = "up"):
    """
    识别 FVG 区域，基于已知的笔区域和价格。
    条件：FVG 必须出现在第三笔的低点，并位于第二笔的低点和第四笔的高点之间。
    """
    fvg_list = []
    fvg_range = []
    
    if updown == "up":
        # 检查是否满足条件：第三笔在第二笔之上，且在第四笔之下
        for i in range(2, len(bi_values)-1):
            if i % 2 == 0:
                last_high = bi_values[i - 1][0]
                next_low = bi_values[i + 1][1]
                if next_low > last_high:
                    fvg_list.append([last_high, next_low])
                    fvg_range.append(bi_ranges[i])
            else:
                # print(i)
                now_low = bi_values[i][1]
                fvg_rev= fvg_list[::-1]

                for fvg in fvg_rev:
                   print(now_low)
                   if now_low <= fvg[0]:

                       fvg_range.pop()
                   else:
                       fvg_list[-1][1] = now_low  
                # print(fvg_list)
    else:
        for i in range(2, len(bi_values)-1):
            if i % 2 == 0:
                last_low = bi_values[i - 1][0]
                next_high = bi_values[i + 1][1]
                if next_high < last_low:
                    fvg_list.append([last_low, next_high])
                    fvg_range.append(bi_ranges[i])
            else:
                # print(i)
                now_high = bi_values[i][1]
                fvg_rev= fvg_list[::-1]

                for fvg in fvg_rev:
                    if now_high >= fvg[0]:
                       fvg_range.pop()
                    else:
                       fvg_list[-1][1] = now_high  
                # print(fvg_list)

    return fvg_list , fvg_range

def identify_turtle_soup(a_chan_feature, fearure_origin):
    '''
    识别海龟汤形态
    '''
    for seg_fea in CHAN_FEATURE:
        if seg_fea not in a_chan_feature:
            continue
            
        seg = a_chan_feature[seg_fea]
        bi_ranges = seg["bi_ranges"]
        bi_values = seg["bi_values"]
        
        # 判断是否形成突破
        is_breakout = check_breakout(bi_ranges, bi_values, fearure_origin)
        
        # 判断成交量特征
        volume_confirm = check_volume_pattern(bi_ranges, fearure_origin)
        
        # 判断波动率
        volatility_expand = check_volatility(bi_ranges, fearure_origin)
        
        # 综合判断
        if is_breakout and volume_confirm and volatility_expand:
            a_chan_feature[f"feachan__{seg_fea}__turtle_soup"] = True
            a_chan_feature[f"feachan__{seg_fea}__turtle_type"] = "bullish/bearish"

def check_breakout(bi_ranges, bi_values, fearure_origin):
    '''
    检查是否突破20/55日高低点
    '''
    last_bi = bi_values[-1]
    price_series = fearure_origin["close"]
    
    # 计算20/55日高低点
    high_20d = price_series.rolling(20).max()
    low_20d = price_series.rolling(20).min()
    high_55d = price_series.rolling(55).max()
    low_55d = price_series.rolling(55).min()
    
    # 判断突破
    return check_price_breakout(last_bi, high_20d, low_20d, high_55d, low_55d)



def add_range_feature(a_chan_feature, fearure_origin):
    '''
    1、最后一段的range
    2、最后一个中枢的range
    '''
    point_feas = [f for f in a_chan_feature.keys() if f.startswith("fpoint")]
    range_feas = [f for f in a_chan_feature.keys() if f.startswith("frange")]
    cmp_feas = [f for f in a_chan_feature.keys() if f.startswith("fcmp")]
    for chan_fea in point_feas:
        point = a_chan_feature[chan_fea]
        for org_fea in ORIGIN_FEATURE:
            if org_fea in fearure_origin.columns:
                fea_name = "feachan__" + chan_fea + "__" + org_fea + "__point"
                a_chan_feature[fea_name] = fearure_origin.iloc[point][org_fea]

    for chan_fea in range_feas:
        range = a_chan_feature[chan_fea]
        for org_fea in ORIGIN_FEATURE:
            if org_fea in fearure_origin.columns:
                fea_name = "feachan__" + chan_fea + "__" + org_fea + "__range"
                a_chan_feature[fea_name + "_mean"] = fearure_origin[range[0]: range[1]][org_fea].mean()
                a_chan_feature[fea_name + "_diff"] = fearure_origin.iloc[range[1]][org_fea] - fearure_origin.iloc[range[0]][org_fea]
                a_chan_feature[fea_name + "_diff_rate"] = a_chan_feature[fea_name + "_diff"] / (range[1] - range[0])

    for chan_fea in cmp_feas:
        cmp = a_chan_feature[chan_fea]
        if not cmp:
            continue
        for org_fea in ORIGIN_FEATURE:
            if org_fea in fearure_origin.columns:
                fea_name = "feachan__" + chan_fea + "__" + org_fea + "__cmp"
                range1 = cmp[0]
                range2 = cmp[1]
                a_chan_feature[fea_name + "_1mean"] = fearure_origin[range1[0]: range[0]][org_fea].mean()
                a_chan_feature[fea_name + "_1sum"] = fearure_origin[range1[0]: range[0]][org_fea].sum()

                a_chan_feature[fea_name + "_2mean"] = fearure_origin[range2[1]: range[1]][org_fea].mean()
                a_chan_feature[fea_name + "_2sum"] = fearure_origin[range2[1]: range[1]][org_fea].sum()

                a_chan_feature[fea_name + "_sumdiff"] = a_chan_feature[fea_name + "_1sum"] / a_chan_feature[fea_name + "_2sum"]
                a_chan_feature[fea_name + "_meandiff"] = a_chan_feature[fea_name + "_1mean"] / a_chan_feature[fea_name + "_2mean"]
                


def add_largetick_feature(a_chan_feature, fearure_origin):
    '''
    1、最后一段大单比例
    2、最后一个中枢大单比例
    '''
    point_feas = [f for f in a_chan_feature.keys() if f.startswith("fpoint")]
    range_feas = [f for f in a_chan_feature.keys() if f.startswith("frange")]
    cmp_feas = [f for f in a_chan_feature.keys() if f.startswith("fcmp")]

    for chan_fea in range_feas:
        range = a_chan_feature[chan_fea]
        for org_fea in LARGETICK_FEATURE:
            fea_name = "feachan__" + chan_fea + "__" + org_fea + "__range"
            a_chan_feature[fea_name + "_mean"] = fearure_origin[range[0]: range[1]][org_fea].mean()

    for chan_fea in cmp_feas:
        cmp = a_chan_feature[chan_fea]
        if not cmp:
            continue
        for org_fea in LARGETICK_FEATURE:
            fea_name = "feachan__" + chan_fea + "__" + org_fea + "__cmp"
            range1 = cmp[0]
            range2 = cmp[1]
            a_chan_feature[fea_name + "_1mean"] = fearure_origin[range1[0]: range[0]][org_fea].mean()
            # a_chan_feature[fea_name + "_1sum"] = fearure_origin[range1[0]: range[0]][org_fea].sum()

            a_chan_feature[fea_name + "_2mean"] = fearure_origin[range2[1]: range[1]][org_fea].mean()
            # a_chan_feature[fea_name + "_2sum"] = fearure_origin[range2[1]: range[1]][org_fea].sum()

            # a_chan_feature[fea_name + "_sumdiff"] = a_chan_feature[fea_name + "_1sum"] / a_chan_feature[fea_name + "_2sum"]
            a_chan_feature[fea_name + "_meandiff"] = a_chan_feature[fea_name + "_1mean"] / a_chan_feature[fea_name + "_2mean"]




def add_rank_feature(a_chan_feature, fearure_origin):
    '''
    1、最后一段rank 的变化情况
    2、最后一个中枢 rank的变化情况
    '''
    point_feas = [f for f in a_chan_feature.keys() if f.startswith("fpoint")]
    range_feas = [f for f in a_chan_feature.keys() if f.startswith("frange")]
    cmp_feas = [f for f in a_chan_feature.keys() if f.startswith("fcmp")]

    for chan_fea in range_feas:
        range = a_chan_feature[chan_fea]
        for org_fea in RANK_FEATURE:
            fea_name = "feachan__" + chan_fea + "__" + org_fea + "__range"
            a_chan_feature[fea_name + "_mean"] = fearure_origin[range[0]: range[1]][org_fea].mean()

    for chan_fea in cmp_feas:
        cmp = a_chan_feature[chan_fea]
        if not cmp:
            continue
        for org_fea in RANK_FEATURE:
            fea_name = "feachan__" + chan_fea + "__" + org_fea + "__cmp"
            range1 = cmp[0]
            range2 = cmp[1]
            a_chan_feature[fea_name + "_1mean"] = fearure_origin[range1[0]: range[0]][org_fea].mean()
            # a_chan_feature[fea_name + "_1sum"] = fearure_origin[range1[0]: range[0]][org_fea].sum()

            a_chan_feature[fea_name + "_2mean"] = fearure_origin[range2[1]: range[1]][org_fea].mean()
            # a_chan_feature[fea_name + "_2sum"] = fearure_origin[range2[1]: range[1]][org_fea].sum()

            # a_chan_feature[fea_name + "_sumdiff"] = a_chan_feature[fea_name + "_1sum"] / a_chan_feature[fea_name + "_2sum"]
            a_chan_feature[fea_name + "_meandiff"] = a_chan_feature[fea_name + "_1mean"] / a_chan_feature[fea_name + "_2mean"]



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

def day_rank2min_rank(feature_rank, fearure_origin):
    # fearure_rank = pd.read_parquet("/liubinxu/liubinxu/finance/learning/data/510050.rank.parquet")
    feature_rank["rank_log"] = np.log(feature_rank["rank"].shift())
    feature_rank["rank_log_pct"] = feature_rank["rank"].pct_change()
    fearure_origin_choose = fearure_origin[["date"]]
    return pd.merge(fearure_origin_choose, feature_rank, on="date", how="left")

# def day_future_relation(feature_rank, fearure_origin):


code = sys.argv[1]
suffix = sys.argv[2]
fdata_dir = os.environ.get('FDATA', '/data/finance/')

fearure_origin = pd.read_parquet(fdata_dir + "/{}.{}".format(code, suffix))
# fearure_origin = pd.read_parquet(fdata_dir + "/{}.qfq.merge.kdj.day.parquet".format(code))
# feature_large_tick = pd.read_parquet("../{}.largetick.parquet".format(code))
# feature_rank = pd.read_parquet("../{}.rank.parquet".format(code))
# feature_rank = day_rank2min_rank(feature_rank, fearure_origin)

columns = fearure_origin.columns

ORIGIN_FEATURE = [c for c in fearure_origin.columns if c.startswith("close_") or c.startswith("amount_") or c.startswith("esv_") or c.startswith("ev_") or c.startswith("macdhist_") or c.startswith("bbands_normal_") or c in ["K18", "K36", "K72", "K144"]]
LARGETICK_FEATURE = [c for c in fearure_origin.columns if c.startswith("buy_") or c.startswith("sell_") or c.startswith("turnover_") or c in ["average_slippage", "average_trade_size", "kurtosis_per_minute", "price_jump_count", "turnover", "twap_per_minute", "price_volatility_per_5min", "trade_frequency", "volume_imbalance"]]
RANK_FEATURE = ["rank_log", "rank_log_pct"]
FUTURE_FEATURE = [c for c in fearure_origin.columns if c.split("_")[0] in ["IC", "IF", "IM", "IH"]]

ORIGIN_FEATURE = ORIGIN_FEATURE + LARGETICK_FEATURE + RANK_FEATURE + FUTURE_FEATURE
# with open("feature.tsv", "w") as f:
#     for col in columns:
#         f.write(col + "\n")
chan_feature_file = "{}_all.feature.libsvm.json".format(code)

feature_list = []
with open(chan_feature_file) as f:
    for line in f:
        cols = line.strip().split("\t")
        time = cols[0]
        labels = cols[1:-1]
        feature_list.append([time, labels, json.loads(cols[-1])])

# feature_list = feature_list[-30:]

for feature in feature_list:
    # print("add_feature")
    chan_feature_type(feature[-1])
    add_range_feature(feature[-1], fearure_origin)
    # add_chan_feature(feature, fearure_origin)
    # add_largetick_feature(feature[-1], feature_large_tick)
    # add_rank_feature(feature[-1], feature_rank)
    

with open("{}.feature_chan.all.json".format(code), "w") as f:
    for t, l, a_chan_feature in feature_list:
        # add_seg_feature(a_chan_feature, fearure_origin)
        # add_zs_feature(a_chan_feature, fearure_origin)
        f.write("{}\t{}\t{}\n".format(t, "__".join(l), json.dumps(a_chan_feature)))