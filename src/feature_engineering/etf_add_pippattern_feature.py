# coding:utf-8
#  给etf数据添加feature

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.utils.pip_pattern_miner import PIPPatternMiner
import sys
import os
import glob




def get_train_data(train_files, amount="amount_normalize20_rolling_96_mean", reg="close480_close2880", reg_type="all", k_type="K18"):
    print("amount {}".format(amount))
    data_list = list()
    arrs = list()
    amounts = list()
    signal_chooses = list()
    for data_file in train_files:
        data = pd.read_parquet(data_file)

        # data["K_pre"] = data["K"].shift()
        data["signal"] = False
        data["signal"][data["K_choose" + "_" + k_type].isin(["type1", "type3"])] = True
        if reg == "up":
            data["signal"][data[reg]<0] = False
        elif reg == "down":
            data["signal"][data[reg]>0] = False
        arr = data['close'].to_numpy()
        amount_data = data[amount]
        signal_choose = data["signal"].to_numpy()
        data_list.append(data)
        arrs.append(arr)
        amounts.append(amount_data)
        signal_chooses.append(signal_choose)    
    return  arrs,  amounts,  signal_chooses, data_list

def train(n_pips=7, lookback=960, hold_period=12, arrs=[], amounts=[], signal_chooses=[]):
    # print(signal_chooses)
    pip_miner = PIPPatternMiner(n_pips=n_pips, lookback=lookback, hold_period=hold_period, signal_choose=signal_chooses)
    pip_miner.train_multi(arrs, vol=amounts, n_reps=-1)
    return pip_miner

def pip_miner_save(pip_miner, file_path):
    import pickle
    filehandler = open(file_path + ".pickle", 'wb') 
    pickle.dump(pip_miner, filehandler)

def pip_miner_stat(pip_miner, data_files, data_list, target_close="target_close5", stat_file="", hold_period=12):
    cluster_martins = []
    nums = []                                                                                                             
    for clust_i in range(len(pip_miner._pip_clusters)): # Loop through each cluster
        rec = dict()
        rec2 = dict()
        for n, data in enumerate(data_list):
            index_code = os.path.basename(data_files[n]).split(".")[0]
            sig = pip_miner._cluster_signals_dict[clust_i][n]
            martin = data_list[n][sig == 1][target_close]
            rec[index_code] = len(martin)
            rec2[index_code] = martin.mean()
        cluster_martins.append(rec2)
        nums.append(rec)
    df1 = pd.DataFrame(cluster_martins)
    df2 = pd.DataFrame(nums)
    df_stat = pd.DataFrame(df1.apply(np.mean, axis=1))
    df_stat.columns = ["target_mean"]
    df_stat["target_num"] = df2.apply(sum, axis=1)
    df_stat["target_sum"]  = df_stat["target_mean"] * df_stat["target_num"] /hold_period
    df_stat["clusters"] = df_stat.index
    df_stat = df_stat.sort_values(by=["target_mean"], ascending=False)
    df_stat["num_sum"] = df_stat["target_num"].cumsum()/hold_period
    df_stat["target_sum_sum"] = df_stat["target_sum"].cumsum()
    df_stat.to_csv(stat_file + ".stat.tsv", sep="\t", index=False)


def run(amount="amount_normalize20_rolling_96_mean", reg="close480_close2880", reg_type="all", k_type="K18", n_pips=7, lookback=960, hold_period=12, target_close="target_close5"):
    # data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close", column2="amount_normalize")
    fdata_dir = os.environ.get('FDATA', '/liubinxu/liubinxu/finance/learning/data/')
    train_code_list = ['159905', '159003', '159601', '159606', '159610', '159612', '159619', '159628', '159632', '159636', '159677', '159741', '159814', '159881', '159647', '159650', '159667', '159679', '159681', '159688', '159708', '159718', '159736', '159742', '159747', '159755', '159776', '159781', '159790', '159796', '159805', '159813', '159820', '159828', '159831', '159839', '159841', '159843', '159850', '159852', '159864', '159866', '159869', '159875', '159887', '159892', '159902', '159907', '159915', '159920', '159925', '159930', '159937', '159939', '159941', '159949', '159968', '159972', '159980', '159982', '159992', '159994', '159997', '510050', '510150', '510230', '510310', '510350', '510500', '510580', '510710', '510800', '510900', '511020', '511060', '511220', '511270', '511380', '511620', '511690', '511810', '511880', '511990', '512010', '512070', '512120', '512290', '512400', '512500', '512660', '512680', '512700', '512720', '512810', '512880', '512900', '512950', '513000', '513020', '513060', '513080', '513100', '513120', '513160', '513200', '513280', '513300', '513330', '513380', '513520', '513550', '513600', '513690', '513770', '513860', '513900', '515000', '515050', '515070', '515100', '159952', '510210', '512560', '513030', '513890', '515650', '516640', '515130', '515180', '515220', '515250', '515330', '515390', '515450', '515710', '515790', '515810', '515880', '515980', '516020', '516110', '516160', '516300', '516510', '516780', '516880', '516950', '517090', '518680', '518850']
    test_code_list = ['159001', '159005', '159605', '159607', '159611', '159615', '159625', '159629', '159633', '159637', '159719', '159768', '159859', '159638', '159649', '159655', '159671', '159680', '159682', '159707', '159713', '159732', '159740', '159745', '159750', '159766', '159780', '159783', '159792', '159801', '159806', '159819', '159825', '159830', '159837', '159840', '159842', '159845', '159851', '159857', '159865', '159867', '159870', '159883', '159888', '159901', '159903', '159908', '159919', '159922', '159928', '159934', '159938', '159940', '159943', '159967', '159971', '159977', '159981', '159985', '159993', '159995', '159998', '510100', '510180', '510300', '510330', '510360', '510510', '510680', '510760', '510880', '511010', '511030', '511180', '511260', '511360', '511520', '511660', '511700', '511850', '511900', '512000', '512040', '512100', '512170', '512330', '512480', '512510', '512670', '512690', '512710', '512760', '512820', '512890', '512930', '512980', '513010', '513050', '513070', '513090', '513110', '513130', '513180', '513260', '513290', '513310', '513360', '513500', '513530', '513580', '513660', '513700', '513800', '513880', '513980', '515030', '515060', '515080', '159929', '159996', '512200', '512800', '513220', '515310', '515900', '515120', '515170', '515210', '515230', '515290', '515380', '515400', '515700', '515770', '515800', '515850', '515950', '516010', '516090', '516150', '516220', '516310', '516770', '516820', '516910', '516970', '517180', '518800', '518880']
    train_data_files = [fdata_dir + "/{}.qfq.kdj.parquet".format(code) for code in train_code_list]  

    arrs,  amounts,  signal_chooses, data_list = get_train_data(train_data_files, amount=amount, reg=reg, reg_type=reg_type, k_type=k_type)
    pip_miner = train(n_pips=n_pips, lookback=lookback, hold_period=hold_period, arrs=arrs, amounts=amounts, signal_chooses=signal_chooses)
    file_path = os.path.join(fdata_dir, "train", "_".join([amount, reg, reg_type, k_type, str(n_pips), str(lookback), str(hold_period), str(target_close)]))
    pip_miner_save(pip_miner, file_path)
    pip_miner_stat(pip_miner, train_data_files, data_list, target_close="target_close5", stat_file=file_path)

    # data_choose = data[['open', 'close', 'high', 'low', 'vol', 'amount', 'datetime', 'code','date', 'amount_normalize', 'K', 'D', 'J', "close_rolling_480_std", "amount_normalize_rolling_6_mean", "amount_diff_rolling_24_std"]]

if __name__ == "__main__":
    amount = ['amount_normalize20_rolling_24_mean', 'amount_normalize20_rolling_24_exp_mean',
              'amount_normalize20_rolling_96_mean', 'amount_normalize20_rolling_96_exp_mean',
              'amount_normalize20_rolling_480_mean', 'amount_normalize20_rolling_480_exp_mean']
    reg = ["close24_close480", "close480_close2880"]
    reg_type = ["all", "up", "down"]
    k_type = ["K18", "K36", "K72"]
    n_pips = [5, 6, 7, 8, 9]
    look_back = [240, 480, 960, 2880]
    hold_period=[3, 6, 12, 36]
    target_close = ["target_close1", "target_close2", "target_close5", "target_close10"]

    # run(amount="amount_normalize20_rolling_96_mean", reg="close480_close2880", reg_type="all", k_type="K18", n_pips=7, lookback=960, hold_period=12, target_close="target_close5")
    
    run(amount=sys.argv[1], 
        reg=sys.argv[2], 
        reg_type=sys.argv[3], 
        k_type=sys.argv[4], 
        n_pips=int(sys.argv[5]), 
        lookback=int(sys.argv[6]), 
        hold_period=int(sys.argv[7]), 
        target_close=sys.argv[8])




