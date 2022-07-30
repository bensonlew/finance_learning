 1/1: import CommonMark
 1/2: from markdown_to_json import CMarkASTNester
 2/1: from markdown_to_json.vendor import CommonMark
 2/2: f= open('document.md', 'r')
 2/3: a= CommonMark.DocParser().parser(f.read())
 2/4: a= CommonMark.DocParser().parse(f.read())
 2/5: a
 2/6: afrom markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
 2/7: from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
 2/8: nester = CMarkASTNester()
 2/9: renderer = Renderer()
2/10: nested = nester.nest(ast)
2/11: nested = nester.nest(a)
2/12: nested
2/13: rendered = renderer.stringify_dict(nested)
2/14: rendered
2/15: rendered
2/16: rendered['faq']
2/17: rendered['faq'].items()
 3/1: import update_mongo_functions as funcs
 4/1: import update_mongo_functions as funcs
 4/2: import bson.objectid
 4/3: import update_mongo_functions as funcs
 4/4: funcs getattr(funcs, "change_tran2gene_id")
 4/5: funcs =  getattr(funcs, "change_tran2gene_id")
 4/6: funcs
 4/7: funcs({"gene": "_", "target": "123"})
 5/1: import pandas as pd
 5/2: a=pd.read_table("express_correlation_info.tsv")
 5/3: a
 5/4: all_node_list = a["gene_id_1"] + a["gene_id_2"]
 5/5: all_node_list
 5/6: all_node_list = list(a["gene_id_1"]) + list(a["gene_id_2"])
 5/7: all_node_list
 5/8: all_node_list.count('ENSMUSG00000073407')
 5/9: a=pd.read_table("./deseq2_gene.tsv", sep="\t", header=0)
5/10: a
5/11: a["degree"] = a["gene_id"].map(lambda x: all_node_list.count(x))
5/12: a
5/13: ls -rlt
5/14: a.to_csv(sep="\t")
5/15: a.to_csv("test.tsv", sep="\t")
5/16: a.to_csv("test.tsv", sep="\t", index_label=False)
5/17: a.to_csv
5/18: a.to_csv("test.tsv", sep="\t", index=False)
5/19: %history
 6/1: a= "{\"cv\":\"0.1\",\"exp_id\":\"5ff48b0317b2bf287eb27064\",\"exp_level\":\"T\",\"geneset_id\":\"All\",\"group_dict\":{\"A1\":[\"A1_1\",\"A1_2\",\"A1_3\"],\"A2\":[\"A2_1\",\"A2_2\",\"A2_3\"],\"B1\":[\"B1_1\",\"B1_2\",\"B1_3\"],\"B2\":[\"B2_1\",\"B2_2\",\"B2_3\"],\"C1\":[\"C1_1\",\"C1_2\",\"C1_3\"],\"C2\":[\"C2_1\",\"C2_2\",\"C2_3\"]},\"group_id\":\"5ff48aae17b2bf287eab68b6\",\"me\":\"1\",\"submit_location\":\"wgcnaprepare\",\"task_id\":\"sanger_312625\",\"task_type\":2}"
 6/2: import json
 6/3: json.loads(a)
 6/4: json.loads(a)["group_dict"]
 7/1: a=None
 7/2: None >="123"
 8/1:
def aaa():
    a=1
 8/2: type(aaa)
 8/3: type(aaa) == function
 8/4: type(aaa) == "function"
 8/5: type(aaa)
 8/6: from types import FunctionType
 8/7: isinstance(a, FunctionType)
 8/8: isinstance(aaa, FunctionType)
 8/9: aaa
8/10: isinstance(aaa, FunctionType)
8/11: type(aaa)
8/12:
class Transcript(object):
    def add_abs(self):
        a= 123
8/13: a= Transcript()
8/14: a.add_abs()
8/15: types(a.add_abs)
8/16: type(a.add_abs)
8/17: import types
8/18: types.BuiltinMethodType
8/19: isinstance(a.add_abs)
8/20: isinstance(a.add_abs, types.FunctionType)
8/21: isinstance(a.add_abs, types.MethodType)
 9/1:
import numpy as np
import pandas as pd
import quandl as q
 9/2: q.ApiConfig.api_key = "../nasdag.api.key"
 9/3: msft_data = q.get("EOD/MSFT", start_date="2010-01-01", end_date="2019-01-01")
 9/4: q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
 9/5: msft_data = q.get("EOD/MSFT", start_date="2010-01-01", end_date="2019-01-01")
 9/6: q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
 9/7: msft_data = q.get("EOD/MSFT", start_date="2010-01-01", end_date="2019-01-01")
 9/8: msft_data = q.get("EOD/MSFT", start_date="2020-01-01", end_date="2021-01-01")
 9/9: msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")
9/10: msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")
9/11: msft_data.head()
10/1: msft_data.head()
10/2: msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")
10/3:
import numpy as np
import pandas as pd
import quandl as q
10/4: q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
10/5: msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")
10/6: msft_data.head()
10/7: msft_data.head()
10/8: msft_data.info
10/9: msft_data.describe()
10/10: msft_data.resample("M").mean()
10/11: msft_data.resample("Y").mean()
10/12: msft_data.resample("W").mean()
10/13: help(msft_data.resample)
10/14: msft_data.resample("W")
10/15: msft_data.resample("W").head()
10/16: msft_data.resample("W").apply(mean)
10/17: msft_data.resample("W").apply(lambda x:x[-1])
10/18: msft_data.resample("W").apply(lambda x:x[-1])
10/19: msft_data.resample("W").apply(lambda x:x)
10/20: msft_data.resample("W").apply(lambda x:mean(x))
10/21: msft_data.resample("W").apply(lambda x:mean(x))
10/22: msft_data.resample("W")[0]
10/23: msft_data.resample("W")[0,]
10/24: msft_data.resample("W")[0,:]
12/1:
import numpy as np
import pandas as pd
import quandl as q

q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")

msft_data.resample("W").mean()
12/2: msft_data.des
12/3: msft_data.describe()
12/4: msft_data["Close"]
12/5: msft_data[["Close"]]
12/6: close = msft_data[["Close"]]
12/7: close.pct_change()
12/8: 0.24 / 12.03
12/9: 0.48 / 12.03
12/10: msft_data.resample
12/11: msft_data.resample("W")
12/12: msft_data.resample("W").apply(lambda x: x[-1])
12/13: msft_data.resample("M").apply(lambda x: x[-1])
12/14: msft_data.resample("M").apply(lambda x: x[-1]).pct_change()
12/15: msft_data.resample("M").apply(lambda x: len(x)?x[-1]: 0)
12/16: msft_data.resample("M").apply(lambda x: length(x)?x[-1]: 0)
12/17: msft_data.resample("M").apply(lambda x: length(x)?x[-1]:0)
12/18: msft_data.resample("M").apply(lambda x: length(x)>0?x[-1]:0)
12/19: len([12,3])
12/20: msft_data.resample("M").apply(lambda x: len(x)>0?x[-1]:0)
12/21: len
12/22: a = len([])?1:3
12/23: msft_data.resample("M").apply(lambda x: x[-1] if len(x) else 0)
12/24: msft_data.resample("W").apply(lambda x: x[-1] if len(x) else 0)
12/25: msft_data.resample("W").apply(lambda x: x[-1] if len(x) else np.nan)
12/26: msft_data.resample("W").apply(lambda x: x[-1] if len(x) else np.nan).pct_change(0)
12/27: msft_data.resample("W").apply(lambda x: x[-1] if len(x) else np.nan).pct_change()
12/28: 16.50 - 16.18
12/29: 0.32 / 16.18
12/30: adj_price = msft_data['Close']
12/31: adj_price
12/32: mav = adj_price.rolling(window=50).mean()
12/33: mav
12/34: print(mav[-10:])
12/35: mav = adj_price.rolling(window=5).mean()
12/36: mav
12/37: print(mav[-10:])
12/38: import matplotlib.pyplot as plt
13/1: help(msft_data.resample)
13/2:
import numpy as np
import pandas as pd
import quandl as q
13/3: q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
13/4: msft_data = q.get("BSE/BOM506166", start_date="2010-01-01", end_date="2019-01-01")
13/5: msft_data.head()
13/6: msft_data.info
13/7: msft_data.describe()
13/8: msft_data.resample("M").mean()
13/9: msft_data.resample("Y").mean()
13/10: msft_data.resample("W").mean()
13/11: help(msft_data.resample)
13/12: msft_data.resample("W").apply(lambda x: x[-1] if len(x) else np.nan).pct_change()
13/13: adj_price = msft_data['Close']
13/14: mav = adj_price.rolling(window=5).mean()
13/15: print(mav[-10:])
13/16: import matplotlib.pyplot as plt
13/17: adj_price.plot()
13/18: mav.plot()
13/19: msft_data = q.get("SPY", start_date="2010-01-01", end_date="2019-01-01")
13/20: msft_data = q.get(ETFG, start_date="2010-01-01", end_date="2019-01-01")
13/21: msft_data = q.get("MRT/F1", start_date="2010-01-01", end_date="2019-01-01")
13/22: msft_data = q.get("MER/F1", start_date="2010-01-01", end_date="2019-01-01")
13/23: msft_data = q.get("MWCS", start_date="2010-01-01", end_date="2019-01-01")
13/24: msft_data = q.get("WIKI", start_date="2010-01-01", end_date="2019-01-01")
13/25: msft_data = q.get("WIKI/PRICES", start_date="2010-01-01", end_date="2019-01-01")
13/26: msft_data = q.get("WIKI/ZUMZ", start_date="2010-01-01", end_date="2019-01-01")
13/27: msft_data.header()
13/28: msft_data.head()
13/29:
short_lb = 50
long_lb = 120
13/30:
signal_df = pd.DataFrame(index=msft_data.index)
signal_df['signal'] = 0.0
13/31: signal_df['short_mav'] = msft_data['Adj_Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
13/32: signal_df['short_mav'] = msft_data['Adj.Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
13/33: signal_df['short_mav'] = msft_data['Adj. Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
13/34: signal_df['long_mav'] = msft_data['Adj. Close'].rolling(window=long_lb, min_periods=1, center=False).mean()
13/35: signal_df.head()
13/36: signal_df['signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)
13/37:
signal_df['positions'] = signal_df['signal'].diff()
signal_df[signal_df['positions'] == -1.0]
13/38: fig = plt.figure()
13/39: plt1 = fig.add_subplot(111,  ylabel='Price in $')
13/40: msft_data['Adj. Close'].plot(ax=plt1, color='r', lw=2.)
13/41: signal_df[['short_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
13/42:
plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, 
         signal_df.short_mav[signal_df.positions == -1.0],
         'v', markersize=10, color='k')
13/43:
plt1.plot(signal_df.loc[signal_df.positions == 1.0].index, 
         signal_df.short_mav[signal_df.positions == 1.0],
         '^', markersize=10, color='m')
13/44: plt.show()
13/45: plt.show()
13/46: .short_mav long_mav
13/47: plt1.show()
13/48: plt.show()
13/49: fig = plt.figure()
13/50:
fig = plt.figure()
fig.show()
13/51: fig = plt.figure()
13/52: plt.show()
13/53: plt1 = fig.add_subplot(111,  ylabel='Price in $')
13/54:
import numpy as np
import pandas as pd
import quandl as q
13/55: q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
13/56: msft_data = q.get("WIKI/ZUMZ", start_date="2010-01-01", end_date="2019-01-01")
13/57:
short_lb = 50
long_lb = 120
13/58:
signal_df = pd.DataFrame(index=msft_data.index)
signal_df['signal'] = 0.0
13/59: signal_df['short_mav'] = msft_data['Adj. Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
13/60: signal_df['long_mav'] = msft_data['Adj. Close'].rolling(window=long_lb, min_periods=1, center=False).mean()
13/61: signal_df['signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)
13/62:
signal_df['positions'] = signal_df['signal'].diff()
signal_df[signal_df['positions'] == -1.0]
13/63: fig = plt.figure()
13/64: plt.show()
13/65: plt1 = fig.add_subplot(111,  ylabel='Price in $')
13/66: msft_data['Adj. Close'].plot(ax=plt1, color='r', lw=2.)
13/67: signal_df[['short_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
13/68:
plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, 
         signal_df.short_mav[signal_df.positions == -1.0],
         'v', markersize=10, color='k')
13/69:
plt1.plot(signal_df.loc[signal_df.positions == 1.0].index, 
         signal_df.short_mav[signal_df.positions == 1.0],
         '^', markersize=10, color='m')
13/70: import matplotlib.pyplot as plt
13/71: fig = plt.figure()
13/72: plt.show()
13/73: plt.imshow(fig)
13/74: plt.imshow()
13/75: %matplotlib inline
13/76: fig = plt.figure()
13/77: plt.show()
13/78: plt1 = fig.add_subplot(111,  ylabel='Price in $')
13/79: plt.show()
13/80: .short_mav long_mav
13/81: plt.show()
14/1:
import numpy as np
import pandas as pd
import quandl as q
14/2: q.ApiConfig.api_key = "cCjtuWZMf4LCen7ePr8n"
14/3: msft_data = q.get("WIKI/ZUMZ", start_date="2010-01-01", end_date="2019-01-01")
14/4: msft_data.head()
14/5:
short_lb = 50
long_lb = 120
14/6:
signal_df = pd.DataFrame(index=msft_data.index)
signal_df['signal'] = 0.0
14/7: signal_df['short_mav'] = msft_data['Adj. Close'].rolling(window=short_lb, min_periods=1, center=False).mean()
14/8: signal_df['long_mav'] = msft_data['Adj. Close'].rolling(window=long_lb, min_periods=1, center=False).mean()
14/9: signal_df.head()
14/10: signal_df['signal'][short_lb:] = np.where(signal_df['short_mav'][short_lb:] > signal_df['long_mav'][short_lb:], 1.0, 0.0)
14/11:
signal_df['positions'] = signal_df['signal'].diff()
signal_df[signal_df['positions'] == -1.0]
14/12: %matplotlib inline
14/13: fig = plt.figure()
14/14: import matplotlib.pyplot as plt
14/15: %matplotlib inline
14/16: fig = plt.figure()
14/17: plt.show()
14/18: plt1 = fig.add_subplot(111,  ylabel='Price in $')
14/19: msft_data['Adj. Close'].plot(ax=plt1, color='r', lw=2.)
14/20: signal_df[['short_mav', 'long_mav']].plot(ax=plt1, lw=2., figsize=(12,8))
14/21:
plt1.plot(signal_df.loc[signal_df.positions == -1.0].index, 
         signal_df.short_mav[signal_df.positions == -1.0],
         'v', markersize=10, color='k')
14/22:
plt1.plot(signal_df.loc[signal_df.positions == 1.0].index, 
         signal_df.short_mav[signal_df.positions == 1.0],
         '^', markersize=10, color='m')
14/23: plt.show()
14/24: plt.show();
14/25: .short_mav long_mav
14/26: plt.show();
14/27: plt.show();
14/28:
slices_hours = [4, 8]
activities = ['Sleep', 'Work']
colors = ['r', 'g']
plt.pie(slices_hours, labels=activities, colors=colors, startangle=90, autopct='%.1f%%')
plt.show()
14/29: plt.show();
14/30: plt
14/31: plt.show();
14/32:
fig = plt.figure()
plt.show();
14/33:
fig = plt.figure()
plt1 = fig.add_subplot(111,  ylabel='Price in $')
plt.show();
19/1:
# -*- coding: utf-8 -*-
# __author__ = 'liubinxu'
# last_modify:2018.11.30

from biocluster.module import Module
import os
import shutil
import re
from biocluster.core.exceptions import OptionError
from biocluster.config import Config
import unittest
import glob

class TargetPredictModule(Module):
    '''
    预测靶基因并合并结果
    novol: 预测的新small_rna fasta格式
    known: 已知small_rna fasta格式
    ref: 靶基因序列， 动物3’utr, 植物cds
    method:靶基因预测方法， 以";" 隔开
    min_support: 至少有几个软件支持
    type: animal/plant
    outtable: 输出的合并结果
    anno_detail: 注释详情表
    '''
    def __init__(self, work_id):
        super(TargetPredictModule, self).__init__(work_id)
        self._fasta_type = {'Protein': 'prot', 'DNA': 'nucl'}
        options = [
            {"name": "known", "type": "infile", "format": "small_rna.fasta"},  # 输入文件
            {"name": "ref", "type": "infile", "format": "small_rna.fasta"},  # 输入文件
            {"name": "method", "type": "string", "default": "miranda"},
            {"name": "type", "type": "string", "default": "animal"},
            {"name": "min_support", "type": "int", "default": 1},
            {"name": "outtable", "type": "outfile", "format": "small_rna.common"},
        ]
        self.add_option(options)
        self.known_predict_tools = []

        self.predict_known = dict()
        self.predict_novol = dict()

    def set_step(self, event):
        if 'start' in event['data'].keys():
            event['data']['start'].start()
        if 'end' in event['data'].keys():
            event['data']['end'].finish()
        self.step.update()

    def check_options(self):
        if not self.option("known").is_set:
            raise OptionError("必须设置参数已知small_rnaknown")
        if len(self.option("method").split(",")) < self.option("min_support"):
            raise OptionError('选择的软件数量应该>= 支持的软件数量')
        return True

    def merge_known(self):
        options = {
            'min_support': self.option('min_support'),
        }

        methods = self.option("method").split(",")
        for n,method in enumerate(methods):
            options.update({
                method.lower(): self.predict_known[method].output_dir + '/' + method.lower() + '_merge_out'
            })
        self.known_merge_tool.set_options(options)
        self.known_merge_tool.run()


    def run_target(self):
        methods = self.option("method").split(",")
        for method in methods:
            predict_tool = self.add_tool('small_rna.mirna_target')
            options = {
                'target': self.option('ref').prop['path'],
                'query': self.option('known').prop['path'],
                "spiece" : self.option('type'),
                "method": method.lower()
            }
            if method.lower() == "targetscan":
                options.update({
                    "target_species": self.option("species")
                })

            else:
                pass

            predict_tool.set_options(options)
            self.predict_known[method] = predict_tool
            self.known_predict_tools.append(predict_tool)


        self.known_merge_tool.on('end', self.set_output)
        for tool in self.known_predict_tools:
            tool.run()

    def import_target(self, target, target_new=None):
        '''
        导入 靶基因信息
        '''
        target_smallrna = dict()
        with open(target, 'rb') as target_f:
            target_f.readline()
            for line in target_f:
                if line.startswith("#"):
                    pass
                else:
                    mirna, target = line.strip().split("\t")[:2]
                    if target in target_smallrna:
                        target_smallrna[target].append(mirna)
                    else:
                        target_smallrna[target] = [mirna]
        if target_new:
            with open(target_new, 'rb') as target_f:
                target_f.readline()
                for line in target_f:
                    if line.startswith("#"):
                        pass
                    else:
                        mirna, target = line.strip().split("\t")[:2]
                        if target in target_smallrna:
                            target_smallrna[target].append(mirna)
                        else:
                            target_smallrna[target] = [mirna]
        return target_smallrna

    def merge_annot_smallrna(self):
        target_smallrna = self.import_target(self.known_merge_tool.output_dir + '/all_merged.xls', None)
        with open(self.option("anno_detail"), 'r') as annot_in, open(self.output_dir + "/All_annot_target.xls", 'w') as annot_out:
            header = annot_in.readline()
            cols = header.split("\t")

            annot_type = "ref"
            if header.startswith("transcript"):
                annot_type = "denovo"
            annot_out.write("target_transcript\tsmall_rnas\tgene\t" + "\t".join(cols[3:]))
            for line in annot_in:
                cols = line.split("\t")
                if annot_type == "denovo":
                    if cols[0] in target_smallrna:
                        small_rnas = ";".join(target_smallrna[cols[0]])
                    else:
                        small_rnas = ""
                else:
                    if cols[1] in target_smallrna:
                        small_rnas = ";".join(target_smallrna[cols[1]])
                    else:
                        small_rnas = ""
                annot_out.write(cols[1] + "\t" + small_rnas + "\t" + cols[0] + "\t" + "\t".join(cols[3:]))

    def set_output(self):
        self.merge_annot_smallrna()
        if os.path.exists(self.output_dir + '/known_target.xls'):
            os.remove(self.output_dir + '/known_target.xls')
        if os.path.exists(self.output_dir + '/novol_target.xls'):
            os.remove(self.output_dir + '/novol_target.xls')
        if os.path.exists(self.output_dir + '/target.fa'):
            os.remove(self.output_dir + '/target.fa')
        os.link(self.option("ref").prop['path'], self.output_dir + '/target.fa')
        for tool in self.known_predict_tools:
            detail_file = glob.glob(tool.output_dir + "/*detail.txt.gz")
            if detail_file:
                detail_out = self.output_dir + '/known_' + os.path.basename(detail_file[0])
                if os.path.exists(detail_out):
                    os.remove(detail_out)
                os.link(detail_file[0], detail_out)

        os.link(self.known_merge_tool.output_dir + '/all_merged.xls', self.output_dir + '/known_target.xls')

        self.end()

    def run(self):
        super(TargetPredictModule, self).run()
        self.known_merge_tool = self.add_tool('small_rna.merge_target_result')
        self.run_target()

    def end(self):
        repaths = [
        ]
        sdir = self.add_upload_dir(self.output_dir)
        sdir.add_relpath_rules(repaths)
        super(TargetPredictModule, self).end()

class TestFunction(unittest.TestCase):
    """
    This is test for the module Just run this script to do test.
    """
    def test(self):
        import random
        from mbio.workflows.single import SingleWorkflow
        from biocluster.wsheet import Sheet
        import datetime
        test_dir='/mnt/ilustre/users/sanger-dev/sg-users/liubinxu/test_small_RNA/'
        data = {
            "id": "target_module" + datetime.datetime.now().strftime('%H-%M-%S'),
            "type": "module",
            "name": "small_rna.target_predict",
            "instant": False,
            "options": dict(
                novol = test_dir + 'mature_rno_novol.dna.fa',
                known = test_dir + 'mature_rno.dna.fa',
                ref = test_dir + 'animal.exon.dna.fa',
                method = 'miranda;targetscan;rnahybrid',
                anno_detail='/mnt/ilustre/users/sanger-dev/app/database/Genome_DB_finish/vertebrates/Rattus_norvegicus/Ensemble_release_89/Annotation_v2/annot_class/anno_stat/all_anno_detail.xls',
                type = 'animal',
                species = 'Rattus_norvegicus'
            )
           }
        wsheet = Sheet(data=data)
        wf = SingleWorkflow(wsheet)
        wf.run()


if __name__ == '__main__':
    unittest.main()
20/1:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/2:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/3:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/4:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/5:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/6:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/7:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/8:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/9:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/10:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
20/11:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
21/1:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
21/2:
# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy
21/3:
# 使用沙盒数据，目的是和书中一样的数据环境
abupy.env.enable_example_env_ipython()
21/4:
from abupy import ABuSymbolPd
ABuSymbolPd.make_kl_df('usJD') is None
21/5:
abupy.env.disable_example_env_ipython()
us_jd = ABuSymbolPd.make_kl_df('usJD')
# 再次开启沙盒环境，本节的示例都是在沙盒数据环境下运行
abupy.env.enable_example_env_ipython()
tail = None
if us_jd is not None:
    tail = us_jd.tail()
tail
22/1:
from __future__ import print_function
# 使用本地的abu
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))

import abupy
from abupy import six, xrange, range, reduce, map, filter, partial
# 使用沙盒数据，目的是和书中一样的数据环境
abupy.env.enable_example_env_ipython()
23/1: complex(1,2)
23/2: complex(1,2)^2
23/3: a= {1,2,3}
23/4: a
23/5: b = set([1.2.3])
23/6: b = set([1.2.3])
23/7: b = set([1,2,3])
23/8: b
23/9: aa = ["ds", "ss", "ds","22"]
23/10: aa.remove("ds")
23/11: aa
23/12: aa
23/13: aa.insert(123, 2)
23/14: aa
23/15: aa.insert(2, 2)
23/16: a
23/17: aa
23/18: aa.reverse()
23/19: aa
23/20: aa.index(2)
23/21: aa.index(2, 2)
23/22: aa.index(2, 1)
23/23: import numpy as np
23/24: range(10)
23/25: array1 == np.array(range(10))
23/26: array1 = np.array(range(10))
23/27: array1
23/28: array1.shape
23/29: array1.reshape(2,3)
23/30: array1.reshape(2,5)
23/31: array2 = array1.reshape(2,5)
23/32: array1.shape
23/33: array2.shape
23/34: array1.shape = 2,3
23/35: array1.shape = 5,2
23/36: array1
23/37: array1 * array2
23/38: import pandas as pd
23/39: ser1 = pd.Series(array1)
23/40: ser1 = pd.Series(array1[0])
23/41: set1
23/42: ser1
23/43: ser1.head()
23/44: ser1.head(1)
23/45: ser1.tail(1)
23/46: ser1.index.to_datetime
23/47: ser1.index.to_datetime()
23/48: pd.to_datetime(ser1.index)
23/49: np.random(3, 1, 2)
23/50: np.random.binomial(3, 1, 2)
23/51: np.random.binomial(5, 1, 2)
23/52: np.random.binomial(5, 0.5)
23/53: np.random.binomial(5, 0.5, 10)
23/54: np.random.binomial(1, 0.5, 10)
23/55: np.random.binomial(10, 0.5, 10)
23/56: np.random.binomial(10, 0.5, 20)
23/57: np.random.binomial(10, 0.1, 20)
23/58: np.random.binomial(10, 0.51, 20)
23/59: a = np.random.binomial(10, 0.51, 20)
23/60: a = sum(np.random.binomial(10, 0.51, 20))/20
23/61: a
23/62: a = sum(np.random.binomial(10, 0.51, 2))/2
23/63: a = sum(np.random.binomial(10, 0.51, 2))/2
23/64: a = sum(np.random.binomial(10, 0.51, 3))/3
23/65: sum(np.random.binomial(10, 0.51, 3))/3
23/66: sum(np.random.binomial(10, 0.51, 3))/3
23/67: sum(np.random.binomial(10, 0.51, 3))/3
23/68: sum(np.random.binomial(10, 0.51, 3))/3
23/69: sum(np.random.binomial(10, 0.51, 3))/3
23/70: sum(np.random.binomial(10, 0.51, 3))/3
23/71: sum(np.random.binomial(10, 0.51, 30))/30
23/72: sum(np.random.binomial(10, 0.51, 30))/30
23/73: sum(np.random.binomial(10, 0.51, 30))/30
23/74: sum(np.random.binomial(10, 0.51, 30))/30
23/75: sum(np.random.binomial(10, 0.51, 30))/30
23/76: sum(np.random.binomial(10, 0.51, 30))/30
23/77: sum(np.random.binomial(10, 0.51, 300))/300
23/78: sum(np.random.binomial(10, 0.51, 300))/300
23/79: sum(np.random.binomial(10, 0.51, 300))/300
23/80: sum(np.random.binomial(10, 0.51, 300))/300
23/81: sum(np.random.binomial(10, 0.51, 3000))/3000
23/82: sum(np.random.binomial(10, 0.51, 3000))/3000
23/83: sum(np.random.binomial(10, 0.51, 3000))/3000
23/84: sum(np.random.binomial(10, 0.51, 3000))/3000
23/85: sum(np.random.binomial(10, 0.51, 3000))/3000
23/86: sum(np.random.binomial(10, 0.51, 3000))/3000
23/87: sum(np.random.binomial(10, 0.51, 3000))/3000
23/88: sum(np.random.binomial(10, 0.51, 30000))/30000
23/89: sum(np.random.binomial(10, 0.51, 30000))/30000
23/90: sum(np.random.binomial(10, 0.51, 30000))/30000
23/91: sum(np.random.binomial(10, 0.51, 30000))/30000
23/92: sum(np.random.binomial(10, 0.51, 30000))/30000
25/1:
        with open("Rockhopper_Results/", "r") as fi:
    

    def set_output(self):
        all_files = os.listdir(self.work_dir + '/Rockhopper_Results')
        all_files = [self.work_dir + '/Rockhopper_Results/' + each for each in all_files ]
        for each in all_files:
            if each.endswith('.fa') or each.endswith('.txt') or each.endswith('.bed') or each.endswith('.xls') or each.endswith('.faa'):
                fname = os.path.basename(each)
                link = os.path.join(self.output_dir, fname)
                if os.path.exists(link):
                    os.remove(link)
                os.link(each, link)

        if os.path.exists(self.output_dir + '/genome.predicted_RNA.fa'):
            self.option("predict_fa").set_path(self.output_dir + '/genome.predicted_RNA.fa')
        if os.path.exists(self.output_dir + '/genome.gene.bed'):
            self.option("genome_bed").set_path(self.output_dir + '/genome.gene.bed')
        if os.path.exists(self.output_dir + '/genome.gene.fa'):
            self.option("genome_fa").set_path(self.output_dir + '/genome.gene.fa')
        if os.path.exists(self.output_dir + '/genome.feature.fa'):
            self.option("feature_fa").set_path(self.output_dir + '/genome.feature.fa')

    def run(self):
        super(RockhopperTool, self).run()
        self.rockhopper()
        self.set_output()
        self.end()

class TestFunction(unittest.TestCase):
    """
    This is test for the tool. Just run this script to do test.
    """
    def test(self):
        from mbio.workflows.single import SingleWorkflow
        from biocluster.wsheet import Sheet
        import datetime
        test_dir='/mnt/ilustre/users/sanger-dev/sg-users/fengyitong/prok_rna/pipline/ref'
        data = {
            "id": "Rockhopper_gff" + datetime.datetime.now().strftime('%H-%M-%S'),
            "type": "tool",
            "name": "prok_rna.rockhopper",
            "instant": False,
            "options": dict(
                fna = "/mnt/lustre/users/sanger/workspace/20181127/Prokrna_sanger_142069/remote_input/genome_db/P_87_scaf.fna",
                input_file = "/mnt/lustre/users/sanger/workspace/20181127/Prokrna_sanger_142069/remote_input/gff_or_gtf_file/ref_genome.gtf",
                type = "gtf",
                group_list = "/mnt/lustre/users/sanger/workspace/20181127/Prokrna_sanger_142069/remote_input/group_table/group.txt",
                trimPairFq = "/mnt/lustre/users/sanger/workspace/20181127/Prokrna_sanger_142069/HiseqQc/output/sickle_dir/fq_list.txt",
                special = 'true'
            )
           }
        wsheet = Sheet(data=data)
        wf = SingleWorkflow(wsheet)
        wf.run()


if __name__ == '__main__':
    unittest.main()
26/1:
import numpy as np
import pandas as pd
26/2:
life_df = pd.read_excel('2-1.xlsx')
life_df.head()
26/3:
life_df = pd.read_excel('2-1.xlsx')
life_df.head()
26/4: life_df.describe()
26/5: life_df.shape
26/6: life_df
26/7: life_df.mean()
26/8: life_df.min()
26/9:
# 利用pandas的cut方法进行分组

# 这个bins区间，是根据这组数的范围选择的，看情况。
# right=False 表明上限不在内
bins = range(800,1701,100) 
life_bin_df = pd.cut(life_df['Hours'],bins,right=False)
life_bin_df
life_bin_df = life_bin_df.value_counts().to_frame(name='value_counts').sort_index()
life_bin_df
26/10:
bins = range(800,1701,100) 
life_bin_dfa = pd.cut(life_df['Hours'],bins,right=False)
life_bin_dfa
26/11:
bins = range(800,1701,100) 
bins
26/12: score_df['Score'].count()
26/13:
score_df = pd.read_excel('2-7.xlsx')
score_df
26/14: score_df['Score'].count()
26/15: score_df['Score'].count("83")
26/16: score_df['Score'].value_count()
26/17: score_df['Score'].values_count()
26/18: score_df['Score'].value_counts()
26/19:
# 峰度
score_df['Score'].kurt()
27/1: from scipy import stats
27/2:
stats.binom.cdf(2, n,p
               )
27/3:
n = 6
p = 0.3
27/4:
stats.binom.cdf(2, n,p
               )
27/5:
stats.binom.cdf(1, n,p
               )
27/6:
stats.binom.cdf(0, n,p
               )
27/7:
stats.binom.cdf(6, n,p
               )
27/8:
stats.binom.cdf(5, n,p
               )
27/9:
stats.binom.pmf(5, n,p
               )
27/10:
stats.binom.pmf(2, n,p
               )
27/11:
stats.binom.pmf(0, 10, 0.1
               )
27/12:
stats.binom.pmf(1, 10, 0.1
               )
27/13:
stats.binom.pmf(2, 10, 0.1
               )
27/14:
stats.binom.pmf(2, 10, 0.01
               )
27/15:
stats.binom.pmf(1, 10, 0.01
               )
27/16:
stats.binom.pmf(0, 10, 0.01
               )
27/17:
stats.binom.pmf(0, 100, 0.01
               )
27/18:
stats.binom.pmf(1, 100, 0.01
               )
27/19:
stats.binom.pmf(2, 100, 0.01
               )
27/20:
stats.binom.pmf(0, 100, 0.01
               )
27/21:
stats.binom.pmf(1, 100, 0.01
               )
28/1: import math
28/2: 64*63/2
28/3: 1/365/365
28/4: 1/365/365*365
28/5: 1/365/365*365*2016
28/6: from scipy import special
28/7: special(5, 2)
28/8: special.comb(5, 2)
28/9: special.comb(5, 2)/2^^5
28/10: special.comb(5, 2)/2**5
28/11: math.factorial(3)
28/12: math.factorial(2)
28/13: ls -rlt
29/1:
import numpy as np
from scipy import stats
28/14: from scipy import stats
28/15: stats.norm.interval(0.95, 0, 1)
28/16: stats.norm.interval(0.955, 0, 1)
28/17: stats.norm.interval(0.9545, 0, 1)
28/18: stats.norm.interval(0.9545, 0, 1)
28/19: stats.norm.interval(0.9543, 0, 1)
28/20: stats.norm.interval(0.95435, 0, 1)
28/21: stats.norm.interval(0.95, 0, 1)
29/2:
import numpy as np
import pandas as pd
29/3:
# 传入数据这一步我简化了
speed_sample = pd.read_excel('4-2.xlsx')
speed_sample
28/22: help(stats.norm.interval)
28/23: help(stats.t.interval)
30/1: import os
30/2: a= os.environ()
30/3: a= os.environ
30/4: a
30/5: "GENEMAP_MONGODB"  in os.environ
31/1: from config import Config
32/1: from config import Config
33/1: from config import Config
34/1:
import pandas as pd
import math
a = 5
math.factorial(a)
35/1:
# !/mnt/ilustre/users/sanger-dev/app/program/Python/bin/python
# -*- coding: utf-8 -*-
# __author__ = "yitong.feng"
# 20180721


import os
import sys
# from mako.template import Template
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

fna = sys.argv[1]
script_path = sys.argv[2]
blast_path = sys.argv[3]
operons = list()
transcripts = list()
rock_results = os.listdir('Rockhopper_Results')
seqs_op = set()
seqs_tr = set()

for file in rock_results:
    if u'transcripts' in file:
        transcripts.append(file)
    if u'operons' in file:
        operons.append(file)

for file in operons:
    seqs_op.add(file.split('_operons.txt')[0])
for file in transcripts:
    seqs_tr.add(file.split('_transcripts.txt')[0])
seqs_tmp = seqs_op & seqs_tr
seqs = set()
for i in os.listdir('rock_index'):
    if '.' in i:
        for j in seqs_tmp:
            if j in i:
                seqs.add(i)
    else:
        for j in seqs_tmp:
            if j == i:
                seqs.add(i)

blast_result = dict()
if os.path.exists(blast_path):
    with open(blast_path, 'r') as f:
        for line in f:
            seq_id = line.split('\t')[0]
            target_id = line.split('\t')[2]
            des = " ".join(line.split("\t")[5].split()[2:])
            blast_result[seq_id] = [target_id, des]


def get_gene_range(predict_rna):
    """
    获取基因cds在坐标信息
    """
    gene_range = dict()
    with open(predict_rna, 'r') as trans_r:
        for line in trans_r.readlines()[1:]:
            cols = line.strip("\n").split("\t")
            if len(cols) >= 3 and cols[1] and cols[2]:
                gene_range[cols[6]] = (min(int(cols[1]), int(cols[2])),
                                       max(int(cols[1]), int(cols[2])),
                                       cols[5],
                                       cols[7])
    return gene_range


def choose_anti_info(anti_info, anti):
    if len(anti_info) == 1:
        choosed_aanti_info = anti_info[0]

    else:
        choosed_aanti_info = None
        for aanti_info in anti_info:
            if aanti_info[1] > anti["end"] or aanti_info[2] < anti["start"]:
                continue
            else:
                choosed_aanti_info = aanti_info
    return choosed_aanti_info

def get_seq_anti(antisense, unanti, antisense_f):
    '''
    写入反义转录本信息
    '''
    gene1_info = []
    gene2_info = []
    # for anti in antisense:
    #     if anti["strand"] == "+":
    #         gene1_info = [anti["id"], anti["start"],
    #                       anti["end"], anti["description"]]
    #     else:
    #         gene2_info = [anti["id"], anti["start"],
    #                       anti["end"], anti["description"]]

    #     if anti["antisense_id"] in unanti:
    #         anti_info = unanti[anti["antisense_id"]]
    #         choosed_aanti_info = choosed_aanti_info(anti_info, anti)           

    #         if choosed_aanti_info:
    #             if choosed_aanti_info[-2] == anti["strand"]:
    #                 print("error : strand is same")
    #             elif anti["strand"] == "+":
    #                 gene2_info = [choosed_aanti_info[0], choosed_aanti_info[1],
    #                                   choosed_aanti_info[2], choosed_aanti_info[-1]]
    #             else:
    #                 gene1_info = [choosed_aanti_info[0], choosed_aanti_info[1],
    #                                   choosed_aanti_info[2], choosed_aanti_info[-1]]

    #         over_laps = [int(gene1_info[1]), int(gene1_info[2]),
    #                      int(gene2_info[1]), int(gene2_info[2])]
    #         over_laps.sort()
    #         if int(gene1_info[1]) <= int(gene2_info[1]) and int(gene1_info[2]) >= int(gene2_info[2]):
    #             anti_type = "enclosed"
    #         elif int(gene1_info[1]) >= int(gene2_info[1]) and int(gene1_info[2]) <= int(gene2_info[2]):
    #             anti_type = "enclosed"
    #         elif int(gene1_info[1]) < int(gene2_info[1]) and int(gene1_info[2]) < int(gene2_info[2]):
    #             anti_type = "enclosed"
    #         else:
    #             anti_type = "divergent"

    #         antisense_f.write("\t".join(gene1_info + gene2_info + [
    #             str(over_laps[1]),
    #             str(over_laps[2]),
    #             str(over_laps[2] - over_laps[1] + 1),
    #             anti_type
    #         ]
    #         ))
    return True


with open('Rockhopper_Results/genome.gene.bed', 'w') as genome_bed, \
    open('Rockhopper_Results/genome.knownnc.bed', 'w') as genome_kbed, \
    open('Rockhopper_Results/fasta.gene.bed', 'w') as fasta_bed, \
    open('Rockhopper_Results/fasta.knownnc.bed', 'w') as fasta_kbed, \
    open('Rockhopper_Results/genome.predicted_RNA.bed', 'w') as genome_prebed, \
    open('Rockhopper_Results/genome.predicted_RNA.bed.tmp', 'w') as genome_prexls, \
    open('Rockhopper_Results/fasta.predicted_RNA.bed', 'w') as fasta_prebed, \
    open('Rockhopper_Results/genome.predicted_cds.bed', 'w') as genome_cds_prebed, \
    open('Rockhopper_Results/genome.predicted_cds.bed.tmp', 'w') as genome_cds_prexls, \
    open('Rockhopper_Results/fasta.predicted_cds.bed', 'w') as fasta_cds_prebed, \
    open('Rockhopper_Results/antisense.xls', 'w') as antisense_f, \
    open('Rockhopper_Results/operon.xls', 'w') as ope_w, \
    open('Rockhopper_Results/TSS_and_TTS.xls', 'w') as tss_tts, \
    open('Rockhopper_Results/UTR.xls', 'w') as utr, \
    open('Rockhopper_Results/UTR5.bed', 'w') as utr5, \
    open('Rockhopper_Results/UTR3.bed', 'w') as utr3:
    ope_w.write(
        "Chr_name\tStart\tStop\tStrand\tNumber_of_genes\tGenes\tGenes_detail\n")
    tss_tts.write('Id\tName\tDescription\tLocation\tStrand\tTranscription start site\tTranslation initiation site\tTranslation stop site\tTranscription terminator site\n')
    utr.write("Chr\tStart\tEnd\tGeneID\tGeneName\tStrand\tType\tGene Desc\n")
    genome_prexls.write(
        'Location\tStart\tEnd\tsRNA ID\tType\tStrand\tAntisense_Genes\tlength\n')
    genome_cds_prexls.write(
        'Location\tStart\tEnd\tpredict ID\tType\tStrand\tAntisense_Genes\tlength\n')
    antisense_f.write("\t".join([
        "Gene ID(+)",
        "Start(+)",
        "End(+)",
        "Description(+)",
        "GeneID(-)",
        "Start(-)",
        "End(-)",
        "Description(-)",
        "Overlap_start",
        "Overlap_end",
        "Overlap_length",
        "Type"
    ]))

    new_num = 0
    new_cds_num = 0
    for seq in seqs:
        gene_range = get_gene_range(
            'Rockhopper_Results/' + seq.split('.')[0] + '_transcripts.txt')
        antisense = list()
        unanti = dict()
        with open('Rockhopper_Results/' + seq.split('.')[0] + '_operons.txt', 'r') as ope_r, \
                open('Rockhopper_Results/' + seq.split('.')[0] + '_transcripts.txt', 'r') as trans_r:
            header_ope = ope_r.readline()
            for line in ope_r.readlines():
                cols = line.strip("\n").split("\t")
                gene_detail = []
                genes = cols[-1].split(", ")
                for gene_id in gene_range:
                    if gene_range[gene_id][0] <= int(cols[1]) and gene_range[gene_id][1] >= int(cols[0]):
                        if gene_id in genes or gene_range[gene_id][2] in genes:
                            gene_detail.append(
                                gene_id + "(" + gene_range[gene_id][2] + "|" + gene_range[gene_id][3] + ")")
                ope_w.write(seq + '\t' + line.strip() + "\t" +
                            ";".join(gene_detail) + "\n")
            header_trans = trans_r.readline()
            for line in trans_r.readlines():
                line = line.strip('\n').split('\t')
                if not len(line) < 6:
                    tran_start = line[0]
                    code_start = line[1]
                    code_end = line[2]
                    tran_end = line[3]
                    strand = line[4]
                    name = line[5]
                    type_ = line[6]
                    des = line[7]
                    des_new = des

                    if u'predicted' in type_:
                        if strand == '-':
                            tran_end, tran_start = tran_start, tran_end
                        length = int(tran_end) - int(tran_start) + 1
                        # id需要固定顺序以确保和blast结果一致
                        type__ = 'sRNA' + str(new_num).zfill(4)
                        predicted_id = type__
                        new_num += 1
                        if type__ in blast_result:
                            new_cds_num += 1
                            type_new = "novel{}".format(
                                str(new_cds_num).zfill(4))
                            genome_cds_prebed.write(
                                seq + '\t' + str(int(tran_start) - 1) + '\t' + tran_end + '\t' + type_new + '\t0' + '\t' + strand + '\t' + str(int(tran_start) - 1) + '\t' + tran_end + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                            des_new = blast_result[type__][1]
                            predicted_id = type_new
                            if strand == '-':
                                genome_cds_prexls.write(
                                    seq + '\t' + tran_end + '\t' + str(int(tran_start)) + '\t' + type_new + '\t' + 'predicted_cds' + '\t' +
                                    strand + '\t' + des_new + '\t' + str(length) + '\n')
                            else:
                                genome_cds_prexls.write(
                                    seq + '\t' + str(int(tran_start)) + '\t' + tran_end + '\t' + type_new + '\t' + 'predicted_cds' + '\t' +
                                    strand + '\t' + des_new + '\t' + str(length) + '\n')
                            fasta_cds_prebed.write(type__ + '\t0' + '\t' + str(length) + '\t' + type__ + '\t0' + '\t' +
                                                   strand + '\t0' + '\t' + str(length) + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                        elif length <= 500 and length >= 30:
                            des = type_
                            genome_prebed.write(
                                seq + '\t' + str(int(tran_start) - 1) + '\t' + tran_end + '\t' + type__ + '\t0' + '\t' + strand + '\t' + str(int(tran_start) - 1) + '\t' + tran_end + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                            if strand == '-':
                                genome_prexls.write(
                                    seq + '\t' + tran_end + '\t' + str(int(tran_start)) + '\t' + type__ + '\t' + 'predicted_RNA' + '\t' +
                                    strand + '\t' + des + '\t' + str(length) + '\n')
                            else:
                                genome_prexls.write(
                                    seq + '\t' + str(int(tran_start)) + '\t' + tran_end + '\t' + type__ + '\t' + 'predicted_RNA' + '\t' +
                                    strand + '\t' + des + '\t' + str(length) + '\n')
                            fasta_prebed.write(type__ + '\t0' + '\t' + str(length) + '\t' + type__ + '\t0' + '\t' +
                                               strand + '\t0' + '\t' + str(length) + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                    elif code_start != '' and code_end != '':
                        tran_start_org = tran_start
                        tran_end_org = tran_end
                        if tran_start == '':
                            tran_start = code_start
                        if tran_end == '':
                            tran_end = code_end
                        tran_start_tmp, tran_end_tmp, code_start_tmp, code_end_tmp = tran_start, tran_end, code_start, code_end
                        if strand == '-':
                            tran_end, tran_start = tran_start, tran_end
                            code_end, code_start = code_start, code_end
                        length = int(tran_end) - int(tran_start) + 1
                        genome_bed.write(seq + '\t' + str(int(tran_start)-1) + '\t' + tran_end + '\t' + type_ + '\t0' + '\t' + strand +
                                         '\t' + str(int(code_start)-1) + '\t' + code_end + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                        fasta_bed.write(type_ + '\t' + '0\t' + str(length) + '\t' + type_ + '\t0' + '\t' + strand + '\t' + str(int(code_start)-int(
                            tran_start)) + '\t' + str(int(code_end)-int(tran_start)+1) + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                        tss_tts.write(type_ + '\t' + name + '\t' + des + '\t' + seq + '\t' + strand + '\t' +
                                      tran_start_org + '\t' + code_start_tmp + '\t' + code_end_tmp + '\t' + tran_end_org + '\n')
                        if line[0] != '' and line[0] != line[1]:
                            utr.write(seq + '\t' + tran_start_tmp + '\t' + code_start_tmp + '\t' +
                                      type_ + '\t' + name + '\t' + strand + '\t' + 'UTR5\t' + des + '\n')
                            if strand == '+':
                                utr5.write(seq + '\t' + str(int(tran_start_tmp)-1) + '\t' +
                                           code_start_tmp + '\t' + type_ + '_UTR5' + '\t0' + '\t' + strand + '\n')
                            else:
                                utr5.write(seq + '\t' + str(int(
                                    code_start_tmp) - 1) + '\t' + tran_start_tmp + '\t' + type_ + '_UTR5' + '\t0' + '\t' + strand + '\n')
                        if line[3] != '' and line[2] != line[3]:
                            utr.write(
                                seq + '\t' + code_end_tmp + '\t' + tran_end_tmp + '\t' + type_ + '\t' + name + '\t' + strand + '\t' + 'UTR3\t' + des + '\n')
                            if strand == '+':
                                utr3.write(seq + '\t' + str(int(code_end_tmp)-1) + '\t' +
                                           tran_end_tmp + '\t' + type_ + '_UTR3' + '\t0' + '\t' + strand + '\n')
                            else:
                                utr3.write(seq + '\t' + str(int(
                                    tran_end_tmp) - 1) + '\t' + code_end_tmp + '\t' + type_ + '_UTR3' + '\t0' + '\t' + strand + '\n')
                    else:
                        if tran_end != '' and tran_start != '':
                            if strand == '-':
                                tran_end, tran_start = tran_start, tran_end
                            # print(tran_end, tran_start)
                            length = int(tran_end) - int(tran_start) + 1
                            genome_kbed.write(seq + '\t' + str(int(tran_start)-1) + '\t' + tran_end + '\t' + type_ + '\t0' + '\t' + strand + '\t' + str(
                                int(tran_start)-1) + '\t' + tran_end + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')
                            fasta_kbed.write(type_ + '\t' + '0\t' + str(length) + '\t' + type_ + '\t0' + '\t' +
                                             strand + '\t0' + '\t' + str(length) + '\t0' + '\t1' + '\t' + str(length) + '\t0' + '\n')

                    if 'antisense: ' in des:
                        antisense.append({
                            "id": predicted_id,
                            "start": tran_start,
                            "end": tran_end,
                            "strand": strand,
                            "antisense_id": des.split("antisense: ")[1],
                            "description": des_new

                        })
                    else:
                        if name in unanti:
                            unanti[name].append(
                                [type_, tran_start, tran_end, strand, des]
                            )
                        else:
                            unanti[name] = [
                                [type_, tran_start, tran_end, strand, des]]
        get_seq_anti(antisense, unanti, antisense_f)


#os.system('cat Rockhopper_Results/genome.gene.bed Rockhopper_Results/genome.knownnc.bed Rockhopper_Results/genome.predicted_RNA.bed >Rockhopper_Results/genome.feature.bed && cat Rockhopper_Results/fasta.gene.bed Rockhopper_Results/fasta.knownnc.bed Rockhopper_Results/fasta.predicted_RNA.bed >Rockhopper_Results/fasta.feature.bed')
# os.system('cat Rockhopper_Results/genome.gene.bed Rockhopper_Results/genome.predicted_RNA.bed >Rockhopper_Results/genome.feature.bed && cat Rockhopper_Results/fasta.gene.bed Rockhopper_Results/fasta.knownnc.bed Rockhopper_Results/fasta.predicted_RNA.bed >Rockhopper_Results/fasta.feature.bed')
os.system('cat Rockhopper_Results/genome.gene.bed Rockhopper_Results/genome.predicted_RNA.bed >Rockhopper_Results/genome.feature.bed && cat Rockhopper_Results/fasta.gene.bed Rockhopper_Results/fasta.predicted_RNA.bed >Rockhopper_Results/fasta.feature.bed')
bedtool_path = script_path + '/bioinfo/seq/bedtools-2.25.0/bin/bedtools'
cmd = '''${bedtool_path} getfasta -fi ${fna} -bed Rockhopper_Results/genome.feature.bed -s -name -fo Rockhopper_Results/genome.feature.fa
${bedtool_path} getfasta -fi ${fna} -bed Rockhopper_Results/genome.gene.bed -s -name -fo Rockhopper_Results/genome.gene.fa
${bedtool_path} getfasta -fi ${fna} -bed Rockhopper_Results/genome.predicted_RNA.bed -s -name -fo Rockhopper_Results/genome.predicted_RNA.fa
${bedtool_path} getfasta -fi ${fna} -bed Rockhopper_Results/UTR5.bed -s -name -fo Rockhopper_Results/UTR5.fa
${bedtool_path} getfasta -fi ${fna} -bed Rockhopper_Results/UTR3.bed -s -name -fo Rockhopper_Results/UTR3.fa
'''

# f = Template(cmd)
# bash_info = f.render(bedtool_path=bedtool_path,
#                      fna=fna,
#                      )
with open('run_rockhopper2bed.bash', 'w') as rock_sh:
    rock_sh.write("{} getfasta -fi {} -bed Rockhopper_Results/genome.feature.bed -s -name -fo Rockhopper_Results/genome.feature.fa".format(bedtool_path, fna)+'\n' +
                  "{} getfasta -fi {} -bed Rockhopper_Results/genome.gene.bed -s -name -fo Rockhopper_Results/genome.gene.fa".format(bedtool_path, fna) + '\n' +
                  "{} getfasta -fi {} -bed Rockhopper_Results/genome.predicted_RNA.bed -s -name -fo Rockhopper_Results/genome.predicted_RNA.fa".format(bedtool_path, fna) + '\n' +
                  "{} getfasta -fi {} -bed Rockhopper_Results/genome.predicted_cds.bed -s -name -fo Rockhopper_Results/genome.predicted_cds.fa".format(bedtool_path, fna) + '\n' +
                  "{} getfasta -fi {} -bed Rockhopper_Results/UTR5.bed -s -name -fo Rockhopper_Results/UTR5.fa".format(bedtool_path, fna) + '\n' +
                  "{} getfasta -fi {} -bed Rockhopper_Results/UTR3.bed -s -name -fo Rockhopper_Results/UTR3.fa".format(
                      bedtool_path, fna)
                  )
    # rock_sh.write(bash_info)

os.system('bash run_rockhopper2bed.bash')

#  ------给genome.predicted_RNA.bed加入seqence那一列-----

with open('Rockhopper_Results/genome.predicted_RNA.bed.tmp', 'r') as pre_tmp, \
        open('Rockhopper_Results/genome.predicted_RNA.fa', 'r') as pre_fa, \
        open('Rockhopper_Results/genome.predicted_RNA.bed.xls', 'w') as pre_xls:
    s2seq = dict()
    for seq in pre_fa.read().split('\n>'):
        seq = seq.strip().split('\n')
        s2seq[seq[0].strip().lstrip('>')] = ''.join(seq[1:])
    pre_xls.write(pre_tmp.readline().strip() + '\tSequence\n')
    for line in pre_tmp.readlines():
        tmp = line.strip().split('\t')
        try:
            pre_xls.write(line.strip() + '\t' + s2seq[tmp[3]] + '\n')
        except:
            pre_xls.write(line.strip() + '\t' + '-' + '\n')

# ---------通过ptt文件生成基因的fasta文件并将其翻译成碱基序列--------

chr_list = os.listdir('rock_index')
for i in chr_list:
    with open('rock_index/' + i + '/' + i + '.ptt', 'r') as ptt_r, \
            open('Rockhopper_Results/' + 'cds.bed', 'a') as bed_w, \
            open('Rockhopper_Results/' + 'ptt.bed', 'a') as ptt_w:
        _ = ptt_r.readline()
        _ = ptt_r.readline()
        _ = ptt_r.readline()
        for line in ptt_r.readlines():
            line = line.strip('\n').split('\t')
            bed_w.write(i + '\t' + str(int(line[0].split('..')[0])-1) + '\t' + line[0].split(
                '..')[1] + '\t' + line[5] + '\t0' + '\t' + line[1] + '\n')
            ptt_w.write(i + '\t' + '\t'.join(line) + '\n')
cmd = "{bedtool_path} getfasta -fi {fna} -bed Rockhopper_Results/cds.bed -s -name -fo Rockhopper_Results/cds.fa".format(
    bedtool_path=bedtool_path, fna=fna)
os.system(cmd)

with open('Rockhopper_Results/cds.fa', 'r') as fa_r, \
        open('Rockhopper_Results/cds.faa', 'w') as faa_w:
    for block in fa_r.read().split('\n>'):
        block = block.lstrip('>').split('\n')
        coding_dna = Seq(''.join(block[1:]), IUPAC.ambiguous_dna)
        protein = coding_dna.translate()
        faa_w.write('>' + block[0].strip() + '\n' + str(protein) + '\n')

# 不添加蛋白序列可能不完整

with open('Rockhopper_Results/genome.predicted_cds.bed.tmp', 'r') as ptt_r, \
        open('Rockhopper_Results/' + 'cds.bed', 'aw') as bed_w, \
        open('Rockhopper_Results/' + 'ptt.bed', 'aw') as ptt_w:
    ptt_r.readline()
    for line in ptt_r.readlines():
        line = line.strip('\n').split('\t')
        bed_w.write(line[0] + '\t' + line[1] + '\t' + line[2] +
                    '\t' + line[3] + '\t0' + '\t' + line[4] + '\n')
        ptt_w.write('\t'.join(line) + '\n')


with open('Rockhopper_Results/genome.predicted_cds.fa', 'r') as fa_r, \
        open('Rockhopper_Results/cds.fa', 'aw') as fa_w:
    for line in fa_r:
        fa_w.write(line)
36/1: import akshare
36/2: akshare.__path__
37/1: import akshare
37/2: akshare.__path__
38/1: from gm.api import *
38/2: ?order_target_percent
39/1: from gm.api import run
39/2: help(run)
40/1:
self.anno_detail = os.path.join(db_path, genome_info["anno_path_v2"],
                                "annot_class/anno_stat/all_anno_detail.xls")
41/1:
# -*- coding: utf-8 -*-
# __author__ = 'liubinxu'
import re
import os
import sys
import math
import pandas as pd


class Enrich(object):
    def __init__(self):
        self.diff_fc = {}
        self.max_gene_num = 100
        self.max_term_num = 1000
        self.min_go_dep = 3
        self.max_go_dep = 7
        self.max_p_value = 1
        self.max_padj_value = 1
        self.anno_list = []
        self.gene_list = []
        self.top_enrich_num = 10
        self.seq_id2name = dict()

    def df_to_circ(self, enrich_table=None):
        '''
        读取表达量上下调信息
        '''
        enrich_df = pd.read_table(enrich_table, header=0)
        circle_top_df = enrich_df[: self.top_enrich_num + 1]
        circle_top_df['study_count'] =  circle_top_df['Up_gene'] + circle_top_df['Down_gene']
        self.top_num = max(circle_top_df['All_gene'])

        record_list = circle_top_df.to_dict('records')
        circ1 = self.get_circ1(record_list)


    def get_circ1(self, record_list):
        '''
        外圈
        '''
        source_data = list()
        for rec in record_list:
            source_data.append(
                [rec['ID'], self.top_num]
            )

    def get_circ(self, record_list):
        '''
        2圈
        '''
        source_data = list()
        for rec in record_list:
            source_data.append(
42/1: import vnpy
42/2: vnpy.__file__
44/1: import vnpy
45/1: ls -rlt
45/2: import vnpy
45/3: vnpy.__file__
46/1: from typing import List
46/2: List
46/3: type(List)
46/4: Vector = List[str]
46/5: Vector([1,2,3])
46/6: Vector(["123"])
46/7: a = Vector()
46/8: Vector = List[float]
46/9: Vector
46/10: Vector()
46/11: a = Vector
46/12: a = Vector()
47/1: bool("TRue")
47/2: bool("Flase")
47/3: bool("False")
47/4: str(False)
47/5: bool(str(False))
48/1: a= {"a":1}
48/2: a.updated({"b": 2})
48/3: a.update({"b": 2})
48/4: b = a.update({"b": 2})
48/5: b
48/6: b = a.update({"b": 2}, )
48/7: dict(a, {"b": 3})
48/8: dict(a, **{"b": 3})
49/1: from collections import OrderedDict
49/2: a= OrderedDict(("a":1))
49/3: a= OrderedDict(("a", 1))
49/4: a= OrderedDict(("a", 1))
49/5: a= OrderedDict([("a", 1)])
49/6: a
50/1: from cstock.request import Requests from cstock.hexun_engine import HexunEngine
50/2: from cstock.request import Requests
50/3: from cstock.request import Requester
50/4: from cstock.request
51/1: from cstock.request import Requester
51/2: from cstock.request import Requests
52/1: from cstock.request import Requester
53/1: from cstock.request import Requests
54/1: import argparse
54/2: parser = argparse.ArgumentParser()
54/3: parser.parse_args("-a 122 -b 122")
54/4: a = parser.parse_args("-a 122 -b 122")
55/1: from core.function import load_class_bny_path
55/2: from core.function import load_class_by_path
56/1: a = "sdsd"
56/2: a.capitalize
56/3: a.capitalize()
57/1:
print("开始检测文件%s,格式：%s, 函数:%s" % (path, format_path, "check")

)
57/2: path = '/home/liubinxu/work/rnawl/test/expression_matrix.xls'
57/3: format_path =  'ref_rna_v2.express_matrix'
57/4:
print("开始检测文件%s,格式：%s, 函数:%s" % (path, format_path, "check")

)
57/5: path = u'/home/liubinxu/work/rnawl/test/expression_matrix.xls'
57/6: path
57/7:
print("开始检测文件%s,格式：%s, 函数:%s" % (path, format_path, "check")

)
57/8: import pickle
57/9: a= pickle.load("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk")
57/10: a = a= pickle.load("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk")
57/11: a = a= pickle.loads("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk")
57/12: a = a= pickle.load(open("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk", "r"))
57/13: a = a= pickle.load(open("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk", "r"))
57/14: a= pickle.load(open("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk", "r"))
57/15: d = open("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk", "r")
57/16: d
57/17: a= pickle.load(a)
57/18: a= pickle.load(d)
57/19: d
57/20: a= pickle.loads(d)
57/21: a
57/22: a= pickle.loads(d)
57/23: d
57/24: a = pickle.load(d)
57/25: a
57/26: aa = pickle.load(d)
57/27: aa = pickle.loads(d.read())
57/28: aa = pickle.load(d.read())
57/29: aa = pickle.load(d)
57/30: d
57/31: d = open("/home/liubinxu/work/rnawl/test/ExpCorr/ExpCorr.pk", "r")
57/32: str = d.read()
57/33: str
57/34: aa = pickle.load(str)
57/35: aa = pickle.loads(str)
59/1:
a = [
            [r"03Align/chr_circos/.*_circos\.svg", "svg", "不同样本染色体Reads分布circos图", 0],
            [r"04sRNA_Analysis/01Known_miRNA/known_pre_structure/.*\.pdf", "pdf", "已知miRNA前体结构图", 0],
            [r"04sRNA_Analysis/02Novel_miRNA/novel_pre_structure/.*\.pdf", "pdf", "新miRNA前体结构图", 0],
            [r"04miRNA_Analysis/miRNA_pre_structure/.*\.pdf", "pdf", "miRNA前体结构图", 0],

            [r"06Diff_Express/diff_stat_.*", "xls", "差异表达miRNA统计表", 0],
            [r"06Diff_Express/total_diff_stat_.*", "xls", "差异表达miRNA详情表（所有比较组）", 0],
            [r"06Diff_Express/.*_vs_.*\.xls", "xls", "差异表达miRNA详情表（单个比较组）", 0],
            [r"07miRNA_Target/known_.*_detail\.txt\.gz", "gz", "已知miRNA靶基因比对详细信息", 0],
            [r"07miRNA_Target/novel_.*_detail\.txt\.gz", "gz", "新miRNA靶基因比对详细信息", 0],
            [r"02QC/.*raw_qc_qual\.box\.pdf", 'pdf', '原始数据碱基质量分布图', 0],
            [r"02QC/.*raw_qc_error\.line\.pdf", 'pdf', '原始数据碱基错误率分布图', 0], #*sequence.length.distribution*.pdf
            [r"02QC/.*raw_qc_base\.line\.pdf", 'pdf', '原始数据碱基含量分布图', 0],
            [r"02QC/.*clean_qc_qual\.box\.pdf", 'pdf', '质控数据碱基质量分布图', 0],
            [r"02QC/.*clean_qc_error\.line\.pdf", 'pdf', '质控数据碱基错误率分布图', 0],
            [r"02QC/.*clean_qc_base\.line\.pdf", 'pdf', '质控数据碱基含量分布图', 0],
            [r"02QC/.*sequence.length.distribution*\.pdf", 'pdf', '--useful reads长度分布图', 0],
            [r"03Align/QualityAssessment/.*chromo.reads.distribution*\.pdf", 'pdf', '染色体分布统计图', 0], #*chromo.reads.distribution*.pdf
            [r"03Align/QualityAssessment/.*align_pos_dist.*\.pdf", 'pdf', '不同区域Reads分布统计饼图', 0],
            [r"03Align/QualityAssessment/.*align_pos_dist.*\.pdf", 'pdf', '不同区域Reads分布统计饼图', 0],
            [r"03Align/QualityAssessment/.*align_coverage.*\.pdf", 'pdf', '测序覆盖度分布图', 0],
            [r"03Align/QualityAssessment/.*align_chr_dist.*\.pdf", 'pdf', '不同染色体Reads分布统计柱状图', 0],
            [r"04sRNA_Analysis/all\.assemble.*\.column.pdf", 'pdf', '转录本长度分布柱状图', 0],
            [r"04sRNA_Analysis/all\.assemble.*\.pie.pdf", 'pdf', '转录本长度分布饼图', 0],
            [r"04sRNA_Analysis/.*assemble_relation.*\.columns\.pdf", 'pdf', '基因与转录本关系柱状图', 0],
            [r"04sRNA_Analysis/*ncrna.stat.pie*\.pdf", 'pdf', 'sRNA统计图', 0], # *chart.mirna.statistic*.pdf
            [r"04sRNA_Analysis/.*chart.mirna.statistic*\.pdf", 'pdf', 'miRNA统计图', 0],
            ("all.exp.dist.stack.pdf", '05Express/'),
            ("*exp_distribution.box.pdf", '05Express/'),
            ("*exp_distribution.density.pdf", '05Express/'),
            ("*exp_distribution.violin.pdf", '05Express/'),
            [r"05Express/all.exp.dist.stack.pdf", 'pdf', '表达量分布堆叠图', 0],
            [r"05Express/.*exp_distribution\.box\.pdf", 'pdf', '表达量分布盒型图', 0],
            [r"05Express/.*exp_distribution\.density\.pdf", 'pdf', '表达量分布密度图', 0],
            [r"05Express/.*exp_distribution\.violin\.pdf", 'pdf', '表达量分布小提琴图', 0],
            [r"05Express/02Exp_Corr/.all.exp.heat_corr\.pdf", 'pdf', '样本间相关性热图', 0],
            [r"05Express/03Exp_PCA/.all.exp_relation_pca.scatter.pdf", 'pdf', '样本间PCA图', 0],
            [r"05Express/AnnotStatistics/.*annot_gene_stat.*\.upset\.pdf", 'pdf', '功能注释统计upset图', 0],
            [r"06Diff_Express/all.diffexp_summary.bar.pdf", 'pdf', '表达量差异统计柱状图', 0],
            [r"06Diff_Express/ExpAnnalysis/.*exp_distribution\.box\.pdf", 'pdf', '表达量分布盒型图', 0],
            [r"06Diff_Express/ExpAnnalysis/.*exp_distribution\.density\.pdf", 'pdf', '表达量分布密度图', 0],
            [r"06Diff_Express/ExpAnnalysis/.*exp_distribution\.violin\.pdf", 'pdf', '表达量分布小提琴图', 0],
            [r"06Diff_Express/ExpVenn/.*\.venn\.pdf", 'pdf', '样本间venn图', 0],
            [r"06Diff_Express/ExpVenn/.*\.upset\.pdf", 'pdf', '样本间upset图', 0],
            [r"06Diff_Express/ExpPCA/.*all\.exp_relation.*\.pdf", 'pdf', '样本间PCA图', 0],
            [r"06Diff_Express/ExpCorr/.*all\.exp\.heat_corr.*\.pdf", 'pdf', '样本间相关性热图', 0],
            [r"07miRNA_Target/all\.diffexp.*\.pdf", 'pdf', '表达量差异统计图', 0],
            [r"07miRNA_Target/.*diffexp\.volcano.*\.pdf", 'pdf', '表达量差异火山图', 0],
            [r"07miRNA_Target/.*diffexp\.scatter.*\.pdf", 'pdf', '表达量差异散点图', 0],
            [r"09AS/.*splice_stat.*\.pdf", 'pdf', '可变剪切事件统计图', 0],
            [r"09AS/.*_vs_.*/.*splice_stat\.*pie\.pdf", 'pdf', '组内差异可变剪切事件统计饼状图', 0],
            [r"09AS/.*_vs_.*/.*splice_stat\.*column\.pdf", 'pdf', '组内差异可变剪切事件统计柱状图', 0],
            [r"08miRNA_Structure/.*snp\.pos_stat\.pie\.pdf", 'pdf', 'SNP不同区域分布饼图', 0],
            [r"08miRNA_Structure/.*snp\.type_stat\.column\.pdf", 'pdf', 'SNP类型统计图', 0],
            [r"08miRNA_Structure/.*snp\.type_stat\.pie\.pdf", 'pdf', 'SNP类型饼图', 0],
            [r"08miRNA_Structure/.*snp\.depth_stat\.column\.pdf", 'pdf', 'SNP深度统计图', 0],
            [r"08miRNA_Structure/.*snp\.depth_stat\.pie\.pdf", 'pdf', 'SNP深度饼图', 0]
        ]
59/2: a
59/3: import re
59/4:
for r in a:
    re.compile(r[0])
59/5:
for r in a:
    print(r)
    re.compile(r[0])
59/6: r
59/7: r【0】
59/8: r[0]
59/9: re.compile(r[0])
59/10: re.compile("." + r[0])
   1: import akshare
   2: import akshare as ak
   3: stock_comment_em_df = ak.stock_comment_em()
   4: stock_comment_em_df = ak.stock_comment_em()
   5: stock_comment_em_df = ak.stock_a_all_pb()
   6: stock_comment_em_df
   7: stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol="600000")
   8: stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol="600000")
   9: stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_a_all_pb(symbol="600000")
  10: stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_zh_ah_daily(symbol="600000")
  11: aadf = stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_zh_ah_daily(symbol="600000")
  12: aadf
  13: aadf = stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_zh_ah_daily(symbol="000001")
  14: aadf
  15: aadf = ak.stock_zh_ah_daily(symbol="000001")
  16: ak.stock_zh_ah_daily(symbol="561550")
  17: ak.stock_zh_ah_daily(symbol="561550", start_year="2016")
  18: aaa = ak.stock_zh_ah_daily(symbol="561550", start_year="2016")
  19: print(aaa)
  20: aaa = ak.stock_zh_ah_daily(symbol="561550", start_year="2016")
  21: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2000", end_year="2019", adjust="")
  22: print(stock_zh_ah_daily_df)
  23: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="002318", start_year="2019", end_year="2019", adjust="")
  24: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2019", end_year="2019", adjust="")
  25: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2019", end_year="2019")
  26: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2022")
  27: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2022")
  28: print(stock_zh_ah_daily_df)
  29: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2000", end_year="2019", adjust="")
  30: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="02318", start_year="2021", end_year="2022", adjust="")
  31: print(stock_zh_ah_daily_df)
  32: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="002318", start_year="2021", end_year="2022", adjust="")
  33: print(stock_zh_ah_daily_df)
  34: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="O02318", start_year="2021", end_year="2022", adjust="")
  35: print(stock_zh_ah_daily_df)
  36: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="1b0016", start_year="2021", end_year="2022", adjust="")
  37: print(stock_zh_ah_daily_df)
  38: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="01211", start_year="2021", end_year="2022", adjust="")
  39: print(stock_zh_ah_daily_df)
  40: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="000016.SH", start_year="2021", end_year="2022", adjust="")
  41: print(stock_zh_ah_daily_df)
  42: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="000016", start_year="2021", end_year="2022", adjust="")
  43: print(stock_zh_ah_daily_df)
  44: stock_zh_ah_daily_df = ak.stock_zh_ah_daily(symbol="sh000016", start_year="2021", end_year="2022", adjust="")
  45: print(stock_zh_ah_daily_df)
  46:  ak.stock_zh_index_daily(symbol="sh000001")
  47: sh000001=  ak.stock_zh_index_daily(symbol="sh000001")
  48: sh000001=  ak.stock_zh_index_daily(symbol="510300")
  49: aa = =  ak.stock_zh_index_daily(symbol="510300")
  50: aa =  ak.stock_zh_index_daily(symbol="510300")
  51:  ak.stock_zh_index_daily(symbol="sh000001")
  52: sh000001=  ak.stock_zh_index_daily(symbol="510300")
  53: sh000001=ak.stock_zh_index_daily(symbol="sh000001")
  54: sh000001
  55: sh000001=
  56: fund_name_em_df = ak.fund_name_em()
  57: fund_name_em_df
  58: fund_name_em_df["基金代码"]
  59: fund_name_em_df["基金代码"] == "159919"
  60: fund_name_em_df[ fund_name_em_df["基金代码"] == "159919",]
  61: fund_name_em_df[,fund_name_em_df["基金代码"] == "159919"]
  62: fund_name_em_df[fund_name_em_df["基金代码"] == "159919"]
  63: fund_name_em_df[fund_name_em_df["基金代码"] == "501300"]
  64: ？ak.fund_open_fund_daily_em
  65: help(ak.fund_open_fund_daily_em)
  66: help(ak.fund_open_fund_daily_em)
  67: ak.fund_open_fund_daily_em(symbol="501300")
  68: ak.fund_open_fund_info_em(symbol="501300")
  69: ak.fund_open_fund_info_em(fund="501300")
  70: df501300 =  ak.fund_open_fund_info_em(fund="501300")
  71: df501300["净值日期"]
  72: sh000001
  73: a = [sh000001["date"] in df501300["净值日期"]]
  74:
a = [sh000001["date"] in df501300["净值日期"]

]
  75: sh000001
  76: sh000001_choose = sh000001[["data", "close"]]
  77: sh000001_choose = sh000001[["data", "close"],]
  78: sh000001_choose = sh000001[["date", "close"],]
  79: sh000001_choose = sh000001[,["date", "close"]]
  80: sh000001_choose = sh000001[["date", "close"]]
  81: df501300
  82: df501300_choose=df501300[["净值日期","单位净值"]]
  83: df501300_choose.rename(columns={"净值日期", "date", "单位净值": "jinzhi"})
  84: df501300_choose.rename(columns={"净值日期":"date", "单位净值": "jinzhi"})
  85: df501300_choose.rename(columns={"净值日期":"date", "单位净值": "jinzhi"}, inplace=True)
  86: import pandas as pd
  87: pd.merge(sh000001_choose, df501300_choose, on=[])
  88: pd.merge(sh000001_choose, df501300_choose, on=[])
  89: pd.merge(sh000001_choose, df501300_choose, on=["date", "date"], how="inter")
  90: pd.merge(sh000001_choose, df501300_choose, on=["date", "date"], how="inner")
  91: mergepd = pd.merge(sh000001_choose, df501300_choose, on=["date", "date"], how="inter")
  92: mergepd = pd.merge(sh000001_choose, df501300_choose, on=["date", "date"], how="inner")
  93: mergepd.corr("pearson")
  94: mergepd
  95: mergepd[mergepd["date"]>"2019"]
  96: mergepd[mergepd["date"]>"2019",]
  97: import datetime
  98: a = datetime.date("2021")
  99: a
 100: a = datetime.date()
 101: a = datetime.date(year="2021")
 102: a = datetime.date(year=2021)
 103: a = datetime.date(year=2021, month=1)
 104: a = datetime.date(year=2021, month=1, day=1)
 105: a
 106: print(a)
 107: mergepd[mergepd["date"]>a,]
 108: mergepd[mergepd["date"]>a]
 109: mergepd_choose = mergepd[mergepd["date"]>a]
 110: history -g -f "aks.py"
 111: history -g -f aks.py
