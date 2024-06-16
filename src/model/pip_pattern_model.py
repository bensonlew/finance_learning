# coding:utf-8
#  给etf数据添加feature

import glob
import json
import os
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from src.utils.pip_pattern_miner import PIPPatternMiner
# from pyswarm import pso


class PipPatternModel:
    def __init__(self):
        # Initialize any necessary variables or objects here
        self.fdata_dir = os.environ.get('FDATA', '/liubinxu/liubinxu/finance/learning/data/')
        self.model_params = {
            "train": {
                "amount": "amount_normalize20_rolling_96_exp_mean",
                "reg": "close480_close2880",
                "reg_type": "down",
                "k_type": "K72",
                "n_pips": 7,
                "lookback": 240,
                "hold_period": 3,
                "k_range": 300,
                "amount_type": "no",
                "amount_pct": 0.1,
                "close_std_type": "no",
                "close_std_pct": 1.0,
            },
            "test": {
                # 减少计算每个模型里保存不同的k
                "k_parent": None,
            },
            "evaluate": {
                "target_close": "target_close1"
            }
        }
        self.version = "1"
        self.pip_miner = None
        self.file_path_abr = "test"
        self.is_test = False

    def load_params_from_file(self, file_path):
        '''
        文件中获取模型
        '''
        self.model_params = json.load(open(file_path, "r"))
        self.file_path_abr = self.get_file_path_abr()
        self.file_path_test_abr = self.get_file_path_test_abr()
        # self.pip_miner = self.load_model()

    def load_data(self, data_path):
        # Load data from the specified path
        pass

    def get_train_data(self, data_type="train"):
        '''
        获取pippartern训练数据
        '''
        amount = self.model_params["train"]["amount"]
        reg = self.model_params["train"]["reg"]
        reg_type = self.model_params["train"]["reg_type"]
        k_type = self.model_params["train"]["k_type"]
        
        print("amount {}".format(amount))
        print("close std")
        data_list = list()
        arrs = list()
        amounts = list()
        signal_chooses = list()
        closestds = list()

        test_data_list = list()
        test_arrs = list()
        test_amounts = list()
        test_signal_chooses = list()
        test_closestds = list()

        if data_type == "train":
            data_files = self.train_data_files
        else:
            data_files = self.test_data_files
        for data_file in data_files:
            data = pd.read_parquet(data_file)

            # data["K_pre"] = data["K"].shift()
            data["signal"] = False
            data["signal"][data["K_choose" + "_" + k_type].isin(["type1", "type3"])] = True
            if reg_type == "up":
                data["signal"][data[reg]<0] = False
            elif reg_type == "down":
                data["signal"][data[reg]>0] = False
            data["close_rolling_2880_std_mean"].fillna(0.0, inplace=True)
            
            train_data = data[data.index<"2023"]
            test_data = data[data.index>="2023"]

            arr = train_data['close'].to_numpy()
            amount_data = train_data[amount]
            closestd = train_data["close_rolling_2880_std_mean"]
            # closestd.fillna(0.0, inplace=True)
            signal_choose = train_data["signal"].to_numpy()        
            data_list.append(train_data)
            arrs.append(arr)
            amounts.append(amount_data)
            signal_chooses.append(signal_choose)
            closestds.append(closestd)

            test_arr = test_data['close'].to_numpy()
            test_amount_data = test_data[amount]
            test_closestd = test_data["close_rolling_2880_std_mean"]
            # test_closestds.fillna(0.0, inplace=True)
            test_signal_choose = test_data["signal"].to_numpy()        
            test_data_list.append(test_data)
            test_arrs.append(test_arr)
            test_amounts.append(test_amount_data)
            test_signal_chooses.append(test_signal_choose)
            test_closestds.append(test_closestd)
        # if data_type == "train":
        #     self.train_data_list = data_list
        # elif data_type == "test":
        #     self.test_data_list = data_list    
        return  arrs,  amounts, closestds,  signal_chooses, data_list, test_arrs, test_amounts, test_closestds, test_signal_chooses, test_data_list
    
    def get_file_path_abr(self):
        amount = self.model_params["train"]["amount"]
        reg = self.model_params["train"]["reg"]
        reg_type = self.model_params["train"]["reg_type"]
        k_type = self.model_params["train"]["k_type"]
        n_pips = self.model_params["train"]["n_pips"]
        lookback = self.model_params["train"]["lookback"]
        hold_period = self.model_params["train"]["hold_period"]
        k_range = self.model_params["train"]["k_range"]
        amount_type = self.model_params["train"]["amount_type"]
        close_std_type = self.model_params["train"]["close_std_type"]
        amount_pct = self.model_params["train"]["amount_pct"]
        close_std_pct = self.model_params["train"]["close_std_pct"] 
        version = self.version        
        file_path = os.path.join(self.fdata_dir, "train", "_".join([amount, reg, reg_type, k_type, str(n_pips), str(lookback), str(hold_period), str(k_range), str(amount_type), str(close_std_type), str(amount_pct), str(close_std_pct),str(version)]))
        return file_path
    
    def get_file_path_test_abr(self):
        if self.model_params["test"]["k_parent"]:
            k_parent = self.model_params["test"]["k_parent"]
            return "_kparent" + str(k_parent)
        else:
            return ""       


    def preprocess_data(self):
        # Preprocess the loaded data
        pass

    def train_model(self):
        # Train the model using the preprocessed data

        n_pips = self.model_params["train"]["n_pips"]
        lookback = self.model_params["train"]["lookback"]
        hold_period = self.model_params["train"]["hold_period"]
        # arrs, amounts, signal_chooses, data_list = self.get_train_data()
        
        pip_miner = PIPPatternMiner(n_pips=n_pips, lookback=lookback, hold_period=hold_period, signal_choose=self.train_signal_chooses)
        pip_miner.k_range = self.model_params["train"]["k_range"]
        pip_miner.amount_type = self.model_params["train"]["amount_type"]
        pip_miner.close_std_type = self.model_params["train"]["close_std_type"]
        pip_miner.amount_pct = self.model_params["train"]["amount_pct"]
        pip_miner.close_std_pct = self.model_params["train"]["close_std_pct"]
        if self.model_params["train"]["k_parent_retain"]:            
            retain_ks = [str(k) for k in range(1, pip_miner.k_range) if k % 5 == 0]
        else:
            retain_ks = []
        pip_miner.train_multi(self.train_arrs, vol=self.train_amounts, n_reps=-1, retain_ks=retain_ks, closestds=self.train_closestd)
        
        return pip_miner
    
    def set_train_test_data(self,):
        self.train_code_list = ['159905', '159003', '159601', '159606', '159610', '159612', '159619', '159628', '159632', '159636', '159677', '159741', '159814', '159881', '159647', '159650', '159667', '159679', '159681', '159688', '159708', '159718', '159736', '159742', '159747', '159755', '159776', '159781', '159790', '159796', '159805', '159813', '159820', '159828', '159831', '159839', '159841', '159843', '159850', '159852', '159864', '159866', '159869', '159875', '159887', '159892', '159902', '159907', '159915', '159920', '159925', '159930', '159937', '159939', '159941', '159949', '159968', '159972', '159980', '159982', '159992', '159994', '159997', '510050', '510150', '510230', '510310', '510350', '510500', '510580', '510710', '510800', '510900', '511020', '511060', '511220', '511270', '511380', '511620', '511690', '511810', '511880', '511990', '512010', '512070', '512120', '512290', '512400', '512500', '512660', '512680', '512700', '512720', '512810', '512880', '512900', '512950', '513000', '513020', '513060', '513080', '513100', '513120', '513160', '513200', '513280', '513300', '513330', '513380', '513520', '513550', '513600', '513690', '513770', '513860', '513900', '515000', '515050', '515070', '515100', '159952', '510210', '512560', '513030', '513890', '515650', '516640', '515130', '515180', '515220', '515250', '515330', '515390', '515450', '515710', '515790', '515810', '515880', '515980', '516020', '516110', '516160', '516300', '516510', '516780', '516880', '516950', '517090', '518680', '518850']
        self.test_code_list = ['159001', '159005', '159605', '159607', '159611', '159615', '159625', '159629', '159633', '159637', '159719', '159768', '159859', '159638', '159649', '159655', '159671', '159680', '159682', '159707', '159713', '159732', '159740', '159745', '159750', '159766', '159780', '159783', '159792', '159801', '159806', '159819', '159825', '159830', '159837', '159840', '159842', '159845', '159851', '159857', '159865', '159867', '159870', '159883', '159888', '159901', '159903', '159908', '159919', '159922', '159928', '159934', '159938', '159940', '159943', '159967', '159971', '159977', '159981', '159985', '159993', '159995', '159998', '510100', '510180', '510300', '510330', '510360', '510510', '510680', '510760', '510880', '511010', '511030', '511180', '511260', '511360', '511520', '511660', '511700', '511850', '511900', '512000', '512040', '512100', '512170', '512330', '512480', '512510', '512670', '512690', '512710', '512760', '512820', '512890', '512930', '512980', '513010', '513050', '513070', '513090', '513110', '513130', '513180', '513260', '513290', '513310', '513360', '513500', '513530', '513580', '513660', '513700', '513800', '513880', '513980', '515030', '515060', '515080', '159929', '159996', '512200', '512800', '513220', '515310', '515900', '515120', '515170', '515210', '515230', '515290', '515380', '515400', '515700', '515770', '515800', '515850', '515950', '516010', '516090', '516150', '516220', '516310', '516770', '516820', '516910', '516970', '517180', '518800', '518880']
        
        if self.version == "0":
            self.train_code_list = self.train_code_list[:2]
            self.test_code_list = self.test_code_list[:2]
        # 按日期拆分
        self.all_code_list = self.train_code_list + self.test_code_list

        self.train_data_files = [self.fdata_dir + "/{}.qfq.kdj.parquet".format(code) for code in self.all_code_list] 
        self.test_data_files = [self.fdata_dir + "/{}.qfq.kdj.parquet".format(code) for code in self.all_code_list]
        self.train_arrs,  self.train_amounts, self.train_closestd,  self.train_signal_chooses, self.train_data_list, self.test_arrs,  self.test_amounts, self.test_closestd,  self.test_signal_chooses, self.test_data_list= self.get_train_data()
        # self.test_arrs,  self.test_amounts,  self.test_signal_chooses, self.test_data_list = self.get_train_data(data_type="test")
        # Save the variables to a file
        # variables = {
        #     "train_arrs": self.train_arrs,
        #     "train_amounts": self.train_amounts,
        #     "train_signal_chooses": self.train_signal_chooses,
        #     "train_data_list": self.train_data_list,
        #     "test_arrs": self.test_arrs,
        #     "test_amounts": self.test_amounts,
        #     "test_signal_chooses": self.test_signal_chooses,
        #     "test_data_list": self.test_data_list
        # }
        # with open("variables.pkl", "wb") as f:
        #     pickle.dump(variables, f)

    def train_run(self):
        # data, add_feature = add_corr_feature(data, rolls=[24, 96, 480], column="close", column2="amount_normalize")     
        print("get data")
        
        print("train")
        self.pip_miner = self.train_model()
        print("save stat")        
        # self.file_path_abr = self.get_file_path_abr()        
        
        # pip_miner._unique_pip_patterns = []
        # pip_miner._unique_pip_indices = []
        # pip_miner._unique_pip_datasource=[]
        # pip_miner._cluster_signals = []        
        train_stat_df = self.pip_miner_stat(self.train_data_files, self.train_data_list)
        # 不需要保存
        self._cluster_signals_dict = []
        self.save_model()

        return train_stat_df    

    def test_run(self):
        # arrs,  amounts,  signal_chooses, data_list = self.get_train_data(data_type="test")
        # pip_miner = train(n_pips=n_pips, lookback=lookback, hold_period=hold_period, arrs=arrs, amounts=amounts, signal_chooses=signal_chooses)
        # self.pip_miner = self.load_model()
        self.pip_miner.signal_choose = self.test_signal_chooses
        # print(len(pip_miner.signal_chooses[0]))
        self.pip_miner.test_multi(arr=self.test_arrs, vol=self.test_amounts, closestds=self.test_closestd)
        test_stat_df = self.pip_miner_stat(self.test_data_files, self.test_data_list, test=True)
        return test_stat_df
    
    def train_and_test_run(self):
        if self.load_model():
            pass
        else:
            train_stat_df = self.train_run()
        if self.model_params["test"]["k_parent"]:
            self.pip_miner.train_multi_parent_cluster(self.model_params["test"]["k_parent"])
            train_stat_df = self.pip_miner_stat(self.train_data_files, self.train_data_list)
        else:
            train_stat_df = self.load_train_stat_df()
        
        test_stat_df = self.test_run()
        sum_over_present = self.evaluate_model(train_stat_df, test_stat_df)
        return sum_over_present


    def pip_miner_stat(self, data_files, data_list, test=False):
        target_close=self.model_params["evaluate"]["target_close"]
        stat_file=self.file_path_abr  + self.file_path_test_abr + "_" + target_close        
        if test:
            stat_file += ".test"
        hold_period= self.model_params["train"]["hold_period"]
        cluster_martins = []
        nums = []
        martinss = []                                                                                                        
        for clust_i in range(len(self.pip_miner._pip_clusters)): # Loop through each cluster
            # print(len(self.pip_miner._cluster_signals_dict[clust_i]))
            rec = dict()
            rec2 = dict()
            martins = []
            for n, data in enumerate(data_list):
                index_code = os.path.basename(data_files[n]).split(".")[0]

                sig = self.pip_miner._cluster_signals_dict[clust_i][n]
                # print(n)
                # print(len(sig))
                # print(len(data_list[n]))
                martin = data_list[n][sig == 1][target_close]
                martin = martin[~np.isnan(martin)]
                rec[index_code] = len(martin)
                rec2[index_code] = martin.mean()
                martins += list(martin)[0::hold_period]
            cluster_martins.append(rec2)
            nums.append(rec)
            martinss.append(martins)

        matrinss_all = []
        for mal in martinss:
            matrinss_all += mal
        mannwhitneyu_p = []
        for m in martinss:
            if len(m) > 0:
                statistic, p_value = mannwhitneyu(matrinss_all, m)
                mannwhitneyu_p.append(p_value)
            else:
                mannwhitneyu_p.append(1.0)

        df1 = pd.DataFrame(cluster_martins)
        df2 = pd.DataFrame(nums)
        df_stat = pd.DataFrame(df1.apply(np.mean, axis=1))
        df_stat.columns = ["target_mean"]
        df_stat.fillna(0.0, inplace=True)
        df_stat["target_num"] = df2.apply(sum, axis=1)
        df_stat["target_sum"]  = df_stat["target_mean"] * df_stat["target_num"] /hold_period
        df_stat["mannwhitneyu_p"] = mannwhitneyu_p
        df_stat["clusters"] = df_stat.index
        df_stat = df_stat.sort_values(by=["target_mean"], ascending=False)
        df_stat["num_sum"] = df_stat["target_num"].cumsum()/hold_period
        df_stat["target_sum_sum"] = df_stat["target_sum"].cumsum()
        df_stat.to_csv(stat_file + ".stat.tsv", sep="\t", index=False)
        return df_stat
    
    def load_train_stat_df(self):
        target_close=self.model_params["evaluate"]["target_close"]
        stat_file=self.file_path_abr  + self.file_path_test_abr + "_" + target_close
        if os.path.exists(stat_file):
            return pd.read_csv(stat_file + ".stat.tsv", sep="\t")
        else:
            train_stat_df = self.pip_miner_stat(self.train_data_files, self.train_data_list)
            return train_stat_df
        
    def detail_model(self, cluster_list=[]):
        if self.load_model():
            pass
        else:
            train_stat_df = self.train_run()
        if self.model_params["test"]["k_parent"]:
            self.pip_miner.train_multi_parent_cluster(self.model_params["test"]["k_parent"])
            # train_stat_df = self.pip_miner_stat(self.train_data_files, self.train_data_list)
        else:
            pass
            # train_stat_df = self.load_train_stat_df()

        for cluster in cluster_list:
            self.pip_miner.detail_cluster(int(cluster), self.train_data_list, file=self.file_path_abr + self.file_path_test_abr + str(cluster))


    def evaluate_model(self, train_stat_df, test_stat_df):
        # Evaluate the trained model

        def get_fun(data):
            return (1+data["target_mean"]) ** (data["target_num"]/3)
        def get_test_fun(data):
            return (1+data["test_target_mean"]) ** (data["test_target_num"]/3)

        data = train_stat_df
        test_data = test_stat_df
        
        test_data_choose = test_data[["target_mean", "target_num", "clusters"]]
        test_data_choose.rename(columns={"target_mean":"test_target_mean", "target_num":"test_target_num"}, inplace=True)
        data = data.merge(test_data_choose, left_on="clusters", right_on="clusters")
        data = data[data["target_num"]> 60]
        data = data[data["mannwhitneyu_p"] < 0.1]
        # if len(data) == 0:
        #     return 0.0
        data.fillna(0, inplace=True)
        hold_period = 3 
        data["test_target_num2"]  = data["test_target_num"] /hold_period
        data["test_target_sum"]  = data["test_target_mean"] * data["test_target_num"] /hold_period
        data["test_target_num_sum"] = data["test_target_num2"].cumsum()
        data["test_target_sum_sum"] = data["test_target_sum"].cumsum()


        record = {
            "model": self.file_path_abr + self.file_path_test_abr,
        }

        for choose_pct in [2, 5 ,10, 20, 30, 50, 70, 90, 100]:
            choose = data[data["test_target_num_sum"]< list(data["test_target_num_sum"])[-1]/100 * choose_pct]
            if len(choose) == 0:
                record.update({
                    "day" + str(choose_pct): 0,
                    "all_get" + str(choose_pct): 0,
                    "day_get" + str(choose_pct): 1.0,
                    "test_day" + str(choose_pct): 0,
                    "test_all_get" + str(choose_pct): 0,
                    "test_day_get" + str(choose_pct): 1.0 
                })
                continue
            day = choose["target_num"].sum()/3
            choose["get_fun"] = choose.apply(get_fun, axis=1) 
            all_get = choose["get_fun"].prod()
            day_get = all_get ** (1/(day))

            test_day = choose["test_target_num"].sum()/3
            choose["test_get_fun"] = choose.apply(get_test_fun, axis=1) 
            test_all_get = choose["test_get_fun"].prod()
            test_day_get = test_all_get ** (1/(test_day))
            record.update({
                "day" + str(choose_pct): day,
                "all_get" + str(choose_pct): all_get,
                "day_get" + str(choose_pct): day_get,
                "test_day" + str(choose_pct): test_day,
                "test_all_get" + str(choose_pct): test_all_get,
                "test_day_get" + str(choose_pct): test_day_get 
            })

        

        sum_over_present = (float(record["test_day_get5"]) - float(record["test_day_get100"])) * 0.5 + \
                            (float(record["test_day_get10"]) - float(record["test_day_get100"])) + \
                            (float(record["test_day_get20"]) - float(record["test_day_get100"])) + \
                            (float(record["test_day_get30"]) - float(record["test_day_get100"]))
        
        record["sum_over_present"] = sum_over_present # type: ignore
        
        stat_file=self.file_path_abr  + self.file_path_test_abr + "_" + self.model_params["evaluate"]["target_close"]
        with open(stat_file + ".json", "w") as f:
            f.write(json.dumps(record, ensure_ascii=False, indent=4))

        data.to_csv(stat_file + "merge.tsv", sep="\t", index=False)


        return sum_over_present
    

    def save_model(self):
        # Save the trained model to the specified path
        filehandler = open(self.file_path_abr + ".pickle", 'wb') 
        pickle.dump(self.pip_miner, filehandler)
        

    def load_model(self):
        # Load a trained model from the specified path
        if os.path.exists(self.file_path_abr + ".pickle"):
            print("loading trained model {}".format(self.file_path_abr))
            filehandler = open(self.file_path_abr + ".pickle", 'rb')        
            self.pip_miner = pickle.load(filehandler)
            return self.pip_miner
        else:
            return False
        
    def predict(self, input_data):
        # Use the trained model to make predictions on new data
        pass


if __name__ == "__main__":
    model = PipPatternModel()
    params_file = sys.argv[1]
    fun = sys.argv[2]
    version = sys.argv[3]
    model.version = version
    model.load_params_from_file(params_file)
    model.set_train_test_data()

    if fun == "train":
        model.train_run()
    elif fun == "test":
        model.test_run()
    elif fun == "train_test":
        getting = model.train_and_test_run()
        with open("{}.result".format(params_file), 'w') as f:
            f.write("{}".format(getting))
    elif fun == "detail":
        if sys.argv[4] == "all":
            list = list(range(100))
        else:  
            list = sys.argv[4].split(",")
        model.detail_model(cluster_list=list)

    # def objective_function(x):
    #     # Set the parameters for the model
    #     model.model_params["train"]["n_pips"] = int(x[0])
    #     model.model_params["train"]["lookback"] = int(x[1])
    #     model.model_params["train"]["hold_period"] = int(x[2])
        
    #     # Run the model and get the evaluation metric
    #     train_stat_df = model.train_run()
    #     test_stat_df = model.test_run()
    #     evaluation_metric = model.evaluate_model(train_stat_df, test_stat_df)
        
    #     # Return the negative evaluation metric since PSO minimizes the objective function
    #     return -evaluation_metric

    # # Define the bounds for the parameters
    # lower_bounds = [1, 1, 1]
    # upper_bounds = [10, 10, 10]

    # # Use PSO to find the optimal parameters
    # best_params, best_value = pso(objective_function, lower_bounds, upper_bounds)

    # # Print the best parameters and the corresponding evaluation metric
    # print("Best Parameters:", best_params)
    # print("Best Evaluation Metric:", -best_value)
