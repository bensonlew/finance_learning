from turtle import distance
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import mplfinance as mpf
from pyclustering.cluster.silhouette import silhouette_ksearch_type, silhouette_ksearch
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from .perceptually_important import find_pips
from .kmeans import bi_kMeans
import os

class PIPPatternMiner:

    def __init__(self, n_pips: int, lookback: int, hold_period: int, signal_choose: list):
        self._n_pips = n_pips
        self._lookback = lookback
        self._hold_period = hold_period
        self._close_std = []
        
        self._unique_pip_patterns = []
        self._unique_pip_indices = []
        self._unique_pip_datasource=[]
        self._cluster_centers = []

        self._pip_clusters = []

        self._cluster_signals = []
        self._cluster_objs = []

        self._long_signal = None
        self._short_signal = None

        self._selected_long = []
        self._selected_short = []

        self._fit_martin = None
        self._perm_martins = []
        
        self._data = None # Array of log closing prices to mine patterns
        self._returns = None # Array of next log returns, concurrent with _data
        self.data_list = list()
        self.signal_choose = signal_choose
        self.amount_type = "all"
        self.amount_pct = 1.0
        self.close_std_type = "all"
        self.close_std_pct = 1.0
        self.k_range = 300
        self.cluster_method = "bi-kmeans"
        self.start_range_pct = 0.0

    def get_fit_martin(self):
        return self._fit_martin

    def get_permutation_martins(self):
        return self._perm_martins
    
    def detail_cluster(self, cluster=0, data_list=[], file="test"):
        '''
        提取分类的详细信息
        '''
        indices = self._pip_clusters[int(cluster)]
        choose_mat = np.mat(self._unique_pip_patterns)[indices, ]

        # 使用matplotlib 对choose_mat 做折线图 并保存 到file
        fig, axs = plt.subplots(1, 1)
        for i in range(choose_mat.shape[0]):
            choose_line = np.array(choose_mat[i])[0]
            axs.plot(range(len(choose_line)), choose_line)
        axs.set_title("{}".format(cluster))

        plt.savefig(file + ".png")


        merge_df = pd.DataFrame()
        for n, data in enumerate(data_list):
            # index_code = os.path.basename(data_list[n])
            sig = self._cluster_signals_dict[int(cluster)][n]
            cluster_df = data[sig == 1]
            merge_df = pd.concat([merge_df, cluster_df])
        merge_df.to_csv(file + ".tsv", sep="\t")
        corr_df = merge_df.corr()
        corr_choose = corr_df[["target_close1"]]
        corr_choose.to_csv(file + "_corr.tsv", sep="\t")

    

    def plot_cluster_examples(self, candle_data: pd.DataFrame, cluster_i: int, grid_size: int = 5):
        plt.style.use('dark_background')
        fig, axs = plt.subplots(grid_size, grid_size)
        flat_axs = axs.flatten()
        for i in range(len(flat_axs)):
            if i >= len(self._pip_clusters[cluster_i]):
                break
            
            pat_i = self._unique_pip_indices[self._pip_clusters[cluster_i][i]]
            data_slice = candle_data.iloc[pat_i - self._lookback + 1: pat_i + 1]
            idx = data_slice.index
            plot_pip_x, plot_pip_y = find_pips(data_slice['close'].to_numpy(), self._n_pips, 3)
            
            pip_lines = []
            colors = []
            for line_i in range(self._n_pips - 1):
                l0 = [(idx[plot_pip_x[line_i]], plot_pip_y[line_i]), (idx[plot_pip_x[line_i + 1]], plot_pip_y[line_i + 1])]
                pip_lines.append(l0)
                colors.append('w')

            mpf.plot(data_slice, type='candle',alines=dict(alines=pip_lines, colors=colors), ax=flat_axs[i], style='charles', update_width_config=dict(candle_linewidth=1.75) )
            flat_axs[i].set_yticklabels([])
            flat_axs[i].set_xticklabels([])
            flat_axs[i].set_xticks([])
            flat_axs[i].set_yticks([])
            flat_axs[i].set_ylabel("")

        fig.suptitle(f"Cluster {cluster_i}", fontsize=32)
        plt.show()


    def predict(self, pips_y: list):
        norm_y = (np.array(pips_y) - np.mean(pips_y)) / np.std(pips_y)

        # Find cluster
        best_dist = 1.e30
        best_clust = -1
        for clust_i in range(len(self._cluster_centers)):
            center = np.array(self._cluster_centers[clust_i])
            dist = np.linalg.norm(norm_y-center)
            if dist < best_dist:
                best_dist = dist
                best_clust = clust_i

        if best_clust in self._selected_long:
            return 1.0
        elif best_clust in self._selected_short:
            return -1.0
        else:
            return 0.0
    
    
    def train(self, arr: np.array, vol:np.array, n_reps=-1, returns=None):
        self._data = arr
        self._amount = vol
        if isinstance(returns, pd.Series):
            self._returns = returns
        else:
            self._returns = pd.Series(arr).diff(48).shift(-48)
        self._find_unique_patterns()
        

        search_instance = silhouette_ksearch(
                self._unique_pip_patterns, 5, 40, algorithm=silhouette_ksearch_type.KMEANS).process()
        
        amount = search_instance.get_amount()
        self._kmeans_cluster_patterns(amount)

        self._get_cluster_signals()
        self._assign_clusters()
        self._fit_martin = self._get_total_performance()
        
        print(self._fit_martin)

        if n_reps <= 1:
            return

        # Start monte carlo permutation test
        data_copy = self._data.copy()
        returns_copy = self._returns.copy()
        
        for rep in range(1, n_reps):
            x = np.diff(data_copy).copy()
            np.random.shuffle(x)
            x = np.concatenate([np.array([data_copy[0]]), x])
            self._data = np.cumsum(x)
            self._returns = pd.Series(self._data).diff().shift(-1)
            print("rep", rep) 
            self._find_unique_patterns()
            search_instance = silhouette_ksearch(
                    self._unique_pip_patterns, 4, 50, algorithm=silhouette_ksearch_type.KMEANS).process()
            amount = search_instance.get_amount()
            print(amount)
            self._kmeans_cluster_patterns(amount)
            self._get_cluster_signals()
            self._assign_clusters()
            perm_martin = self._get_total_performance()
            self._perm_martins.append(perm_martin)

    
    def test_multi(self, arr: list, vol:list, closestds: list):
        self.data_list = []
        self._unique_pip_patterns = []
        self._unique_pip_indices = []
        self._unique_pip_datasource=[]
        n = 0
        for arr, vol, closestd in zip(arr, vol, closestds):
            self._data = arr
            self.data_list.append(arr)
            self._amount = vol
            self._close_std = closestd

            self._test_unique_patterns(n=n)
            n += 1
        self._get_test_cluster_signals_multi()
        
        

    def train_multi(self, arr: list, vol:list, n_reps=-1, returns=None, retain_ks=[], closestds=[]):
        # 多组数据训练
        self.data_list = []
        n = 0
        for arr, vol, closestd in zip(arr, vol, closestds):
            self._data = arr
            self.data_list.append(arr)
            self._amount = vol
            self._close_std = closestd

            self._find_unique_patterns(n=n)
            n += 1
        
        if self.cluster_method == "kmeans":
            search_instance = silhouette_ksearch(
                        self._unique_pip_patterns, self.k_range - 50, self.k_range, algorithm=silhouette_ksearch_type.KMEANS).process()
            
            amount = search_instance.get_amount()
            self._kmeans_cluster_patterns(amount)
        elif self.cluster_method == "bi-kmeans":
            self._bikmeans_cluster_patterns(self.k_range, retain_ks=retain_ks)

        self._get_cluster_signals_multi()
        # self._assign_clusters()
        # self._fit_martin = self._get_total_performance()

    def train_multi_parent_cluster(self, k=10):
        self._bikmeans_cluster_parent_patterns(k=k)
        self._get_cluster_signals_multi()   


    def _find_unique_patterns(self, n=None):
        # Find unique pip patterns in data
        if n == None:
            self._unique_pip_indices.clear()
            self._unique_pip_patterns.clear()
        
        last_pips_x = [0] * self._n_pips
        for i in range(self._lookback - 1, len(self._data) - self._hold_period):
            if self.signal_choose[n][i] == False:
                # 筛选部分时间点
                continue
            start_i = i - self._lookback + 1

            # choose low closestd position  
            # 效果反而变差
            # start_i_begin = start_i - int(self._lookback * 2 * self.start_range_pct)
            # start_i_end = start_i + int(self._lookback * 1 * self.start_range_pct)
            # if start_i_begin < 0:
            #     start_i_begin = 0
            # start_min = np.array(self._close_std[start_i_begin: start_i_end]).argmin()
            # start_i = start_i_begin + start_min
                       

            window = self._data[start_i: i + 1]
            pips_x, pips_y = find_pips(window, self._n_pips, 3)
            pips_x = [j + start_i for j in pips_x]
            
            amount_y = [self._amount[x] for x in pips_x]
            close_std_y = [self._close_std[x] for x in pips_x]
            if np.isnan(amount_y[0]):
                continue
            # Check internal pips to see if it is the same as last
            same = True
            for j in range(1, self._n_pips - 1):
                if pips_x[j] != last_pips_x[j]:
                    same = False
                    break
            
            if not same:
                # Z-Score normalize pattern
                # pips_y = np.log(pips_y)
                pips_y = list((np.array(pips_y) - np.mean(pips_y)) / np.std(pips_y))
                amount_y = list((np.array(amount_y) - np.mean(amount_y)) / np.std(amount_y))
                # close_std_y = list((np.array(close_std_y) - np.mean(close_std_y)) / np.std(close_std_y)
                # 只选择部分成交量
                if self.amount_type == "all":
                    amount_choose = amount_y
                elif self.amount_type == "half":
                    if len(amount_y) % 2 == 0:
                        amount_choose = amount_y[1::2]
                    else:
                        amount_choose = amount_y[::2]
                elif self.amount_type == "begin_end":
                    amount_choose = [amount_y[0], amount_y[-1]]
                elif self.amount_type == "tree":
                    amount_choose = [amount_y[0], amount_y[int(len(amount_y)/2)], amount_y[-1]]
                elif self.amount_type == "tail":
                    amount_choose = [amount_y[0], amount_y[-2], amount_y[-1]]
                elif self.amount_type == "no":
                    amount_choose = []
                else:
                    amount_choose = []

                if self.close_std_type == "all":
                    close_std_choose = close_std_y
                elif self.close_std_type == "half":
                    if len(close_std_y) % 2 == 0:
                        close_std_choose = close_std_y[1::2]
                    else:
                        close_std_choose = close_std_y[::2]
                elif self.close_std_type == "begin_end":
                    close_std_choose = [close_std_y[0], close_std_y[-1]]
                elif self.close_std_type == "tree":
                    close_std_choose = [close_std_y[0], close_std_y[int(len(close_std_y)/2)], close_std_y[-1]]
                elif self.close_std_type == "tail":
                    close_std_choose = [close_std_y[0], close_std_y[-2], close_std_y[-1]]
                elif self.close_std_type == "no":
                    close_std_choose = []
                else:
                    close_std_choose = []
                amount_choose = [amount * self.amount_pct for amount in amount_choose]
                close_std_choose = [close_std * self.close_std_pct for close_std in close_std_choose]

                self._unique_pip_patterns.append(pips_y + amount_choose + close_std_choose)

                self._unique_pip_indices.append(i)
                self._unique_pip_datasource.append(n)

            last_pips_x = pips_x

    def _test_unique_patterns(self, n=None):
        # Find unique pip patterns in data
        if n == None:
            self._unique_pip_indices.clear()
            self._unique_pip_patterns.clear()
        
        last_pips_x = [0] * self._n_pips
        # print(n, len(self._data), len(self.signal_choose[n]))
        for i in range(self._lookback - 1, len(self._data) - self._hold_period):
            if self.signal_choose[n][i] == False: # type: ignore
                # 筛选部分时间点
                continue
            start_i = i - self._lookback + 1

            # start_i_begin = start_i - int(self._lookback * 2 * self.start_range_pct)
            # start_i_end = start_i + int(self._lookback * 1 * self.start_range_pct)
            # if start_i_begin < 0:
            #     start_i_begin = 0
            # start_min = np.array(self._close_std[start_i_begin: start_i_end]).argmin()
            # start_i = start_i_begin + start_min

            window = self._data[start_i: i + 1]
            pips_x, pips_y = find_pips(window, self._n_pips, 3)
            pips_x = [j + start_i for j in pips_x]
            
            amount_y = [self._amount[x] for x in pips_x]
            close_std_y = [self._close_std[x] for x in pips_x]

            if np.isnan(amount_y[0]):
                continue
            # Check internal pips to see if it is the same as last
            same = True
            for j in range(1, self._n_pips - 1):
                if pips_x[j] != last_pips_x[j]:
                    same = False
                    break
            
            if not same:
                # Z-Score normalize pattern
                # pips_y = np.log(pips_y)
                pips_y = list((np.array(pips_y) - np.mean(pips_y)) / np.std(pips_y))
                amount_y = list((np.array(amount_y) - np.mean(amount_y)) / np.std(amount_y))
                amount_choose = []
                if self.amount_type == "all":
                    amount_choose = amount_y
                elif self.amount_type == "half":
                    if len(amount_y) % 2 == 0:
                        amount_choose = amount_y[1::2]
                    else:
                        amount_choose = amount_y[::2]
                elif self.amount_type == "begin_end":
                    amount_choose = [amount_y[0], amount_y[-1]]
                elif self.amount_type == "tree":
                    amount_choose = [amount_y[0], amount_y[int(len(amount_y)/2)], amount_y[-1]]
                elif self.amount_type == "tail":
                    amount_choose = [amount_y[0], amount_y[-2], amount_y[-1]]
                elif self.amount_type == "no":
                    amount_choose = []

                if self.close_std_type == "all":
                    close_std_choose = close_std_y
                elif self.close_std_type == "half":
                    if len(close_std_y) % 2 == 0:
                        close_std_choose = close_std_y[1::2]
                    else:
                        close_std_choose = close_std_y[::2]
                elif self.close_std_type == "begin_end":
                    close_std_choose = [close_std_y[0], close_std_y[-1]]
                elif self.close_std_type == "tree":
                    close_std_choose = [close_std_y[0], close_std_y[int(len(close_std_y)/2)], close_std_y[-1]]
                elif self.close_std_type == "tail":
                    close_std_choose = [close_std_y[0], close_std_y[-2], close_std_y[-1]]
                elif self.close_std_type == "no":
                    close_std_choose = []
                amount_choose = [amount * self.amount_pct for amount in amount_choose]
                close_std_choose = [close_std * self.close_std_pct for close_std in close_std_choose]




                corr_list = []
                for cluster_center in self._cluster_centers:
                    corr_list.append(
                        np.linalg.norm(np.array(pips_y + amount_choose + close_std_choose) - np.array(cluster_center))
                        # np.corrcoef(pips_y + amount_choose, cluster_center)[0][1]
                    )

                corr_list = np.array(corr_list)
                cluster_num = corr_list.argmin()
                distance = min(corr_list)
                if distance < self._cluster_center_distance[cluster_num][0] + 2 * self._cluster_center_distance[cluster_num][1]:
                    # print(len(self._cluster_centers), cluster_num)
                    self._unique_pip_patterns.append(cluster_num)
                    self._unique_pip_indices.append(i)
                    self._unique_pip_datasource.append(n)

            last_pips_x = pips_x


    def _kmeans_cluster_patterns(self, amount_clusters):
        # Cluster Patterns
        initial_centers = kmeans_plusplus_initializer(self._unique_pip_patterns, amount_clusters).initialize()
        kmeans_instance = kmeans(self._unique_pip_patterns, initial_centers)
        kmeans_instance.process()

        # Extract clustering results: clusters and their centers
        self._pip_clusters = kmeans_instance.get_clusters()
        self._cluster_centers = kmeans_instance.get_centers()

    def _bikmeans_cluster_patterns(self, amount_clusters, retain_ks=[]):
        # Cluster Patterns

        a1, a2, retain_dict = bi_kMeans(np.mat(self._unique_pip_patterns), k=amount_clusters, retain_ks=retain_ks)
        distances = []
        pip_clusters = []
        for n in range(0,len(a1)):
            mean = a1[n]
            indices = np.where([a2[:, 0] == n])[1]
            choose_mat = np.mat(self._unique_pip_patterns)[indices, ]
            dis = [np.linalg.norm(np.array(mean) - np.array(b)) for b in choose_mat]
            distances.append([
                np.mean(dis),
                np.std(dis),
                len(choose_mat)
            ])
            pip_clusters.append(indices)

        print(a1[:2])
        # Extract clustering results: clusters and their centers
        self._pip_clusters = pip_clusters
        self._cluster_centers = a1
        self._cluster_center_distance = distances
        self._retain_dict = retain_dict

    def _bikmeans_cluster_parent_patterns(self, k):
        # Cluster Patterns

        a1, a2 = self._retain_dict[str(k)]
        distances = []
        pip_clusters = []
        for n in range(0,len(a1)):
            mean = a1[n]
            indices = np.where([a2[:, 0] == n])[1]
            choose_mat = np.mat(self._unique_pip_patterns)[indices, ]
            dis = [np.linalg.norm(np.array(mean) - np.array(b)) for b in choose_mat]
            distances.append([
                np.mean(dis),
                np.std(dis),
                len(choose_mat)
            ])
            pip_clusters.append(indices)


        # Extract clustering results: clusters and their centers
        self._pip_clusters = pip_clusters
        self._cluster_centers = a1
        self._cluster_center_distance = distances

    def _get_martin(self, rets: np.array):
        rsum = np.sum(rets)
        short = False
        if rsum < 0.0:
            rets *= -1
            rsum *= -1
            short = True

        csum = np.cumsum(rets)
        eq = pd.Series(np.exp(csum))
        sumsq = np.sum( ((eq / eq.cummax()) - 1) ** 2.0 )
        ulcer_index = (sumsq / len(rets)) ** 0.5
        martin = rsum / ulcer_index
        if short:
            martin = -martin

        return martin

    def _get_cluster_signals(self):
        self._cluster_signals.clear()

        for clust in self._pip_clusters: # Loop through each cluster
            signal = np.zeros(len(self._data)) # type: ignore
            for mem in clust: # Loop through each member in cluster
                arr_i = self._unique_pip_indices[mem]
                data_source = self._unique_pip_datasource[mem]
                # Fill signal with 1s following pattern identification
                # for hold period specified
                signal[arr_i: arr_i + self._hold_period] = 1. 
            
            self._cluster_signals.append(signal)

    def _get_cluster_signals_multi(self):
        self._cluster_signals_dict = dict()

        for n, clust in enumerate(self._pip_clusters): # Loop through each cluster # type: ignore
            self._cluster_signals_dict[n] = []
            for adata in self.data_list:
                signal = np.zeros(len(adata))
                self._cluster_signals_dict[n].append(signal)
            for mem in clust: # Loop through each member in cluster
                arr_i = self._unique_pip_indices[mem]
                data_source = self._unique_pip_datasource[mem]
                # Fill signal with 1s following pattern identification
                # for hold period specified
                signal= self._cluster_signals_dict[n][data_source]
                signal[arr_i: arr_i + self._hold_period] = 1.

    def _get_test_cluster_signals_multi(self):
        self._cluster_signals_dict = dict()

        for n, clust in enumerate(self._pip_clusters): # Loop through each cluster
            self._cluster_signals_dict[n] = []
            for adata in self.data_list:
                signal = np.zeros(len(adata))
                self._cluster_signals_dict[n].append(signal)
        for data_source, cluster_n, arr_i in zip(self._unique_pip_datasource, self._unique_pip_patterns, self._unique_pip_indices):
            # print(data_source, cluster_n, arr_i)
            signal= self._cluster_signals_dict[cluster_n][data_source]
            signal[arr_i: arr_i + self._hold_period] = 1. 
            


    def _assign_clusters(self):
        self._selected_long.clear()
        self._selected_short.clear()
        
        # Assign clusters to long/short/neutral
        cluster_martins = []
        for clust_i in range(len(self._pip_clusters)): # Loop through each cluster
            sig = self._cluster_signals[clust_i]
            sig_ret = self._returns * sig
            martin = self._get_martin(sig_ret)
            cluster_martins.append(martin)

        best_long = np.argmax(cluster_martins)
        best_short = np.argmin(cluster_martins)
        self._selected_long.append(best_long)
        self._selected_short.append(best_short)

    def _get_total_performance(self):

        long_signal = np.zeros(len(self._data))
        short_signal = np.zeros(len(self._data))

        for clust_i in range(len(self._pip_clusters)):
            if clust_i in self._selected_long:
                long_signal += self._cluster_signals[clust_i]
            elif clust_i in self._selected_short:
                short_signal += self._cluster_signals[clust_i]
        
        long_signal /= len(self._selected_long)
        short_signal /= len(self._selected_short)
        short_signal *= -1

        self._long_signal = long_signal
        self._short_signal = short_signal
        rets = (long_signal + short_signal) * self._returns

        martin = self._get_martin(rets)
        return martin

if __name__ == '__main__':
    data = pd.read_csv('BTCUSDT3600.csv')
    data['date'] = data['date'].astype('datetime64[s]')
    data = data.set_index('date')
    data = np.log(data)

    plt.style.use('dark_background')

    data = data[data.index < '01-01-2020']
    arr = data['close'].to_numpy()
    pip_miner = PIPPatternMiner(n_pips=5, lookback=24, hold_period=6)
    pip_miner.train(arr, n_reps=-1)

    '''
    # Monte Carlo test, takes about an hour..
    pip_miner.train(arr, n_reps=100)
    
    plt.style.use('dark_background')
    actual_martin = pip_miner.get_fit_martin()
    perm_martins = pip_miner.get_permutation_martins()
    ax = pd.Series(perm_martins).hist()
    ax.set_ylabel("# Of Permutations")
    ax.set_xlabel("Martin Ratio")
    ax.set_title("Permutation's Martin Ratio BTC-USDT 1H 2018-2020")
    ax.axvline(actual_martin, color='red')
    '''






    

