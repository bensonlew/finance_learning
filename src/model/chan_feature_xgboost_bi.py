import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
import sys
import sklearn
import sklearn.model_selection
import xgboost as xgb
import glob
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ParameterGrid
import os
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
from sklearn.preprocessing import LabelBinarizer
import sys
sys.setrecursionlimit(10000)


chan_feature_files = glob.glob(sys.argv[1])
label_index = int(sys.argv[2])
time_stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

if os.path.exists("chan_feature_df.parquet"):
    chan_feature_df = pd.read_parquet("chan_feature_df.parquet")
else:
    dfs = []  # 存储每个文件的DataFrame
    for chan_feature_file in chan_feature_files:
        print(chan_feature_file)
        feature_list = []  # 临时存储单个文件的特征
        with open(chan_feature_file) as f:
            for line in f:
                cols = line.strip().split("\t")
                label = cols[1].split("__")[label_index]
                if label not in ["1low", "1high", "2low", "2high", "0"]:
                    continue
                try:
                    fea_dict = json.loads(cols[-1])
                    fea_dict["time"] = cols[0]
                    fea_dict["label"] = label
                    feature_list.append(fea_dict)
                except Exception as e:
                    print("error {} {}".format(chan_feature_file, line))
        
        # 将单个文件的数据转换为DataFrame并添加到列表中
        if feature_list:
            df = pd.DataFrame(feature_list)
            dfs.append(df)
            del feature_list  # 释放内存
        
    # 使用concat合并所有DataFrame
    chan_feature_df = pd.concat(dfs, ignore_index=True)
    del dfs
    chan_feature_df.to_parquet("chan_feature_df.parquet")
# chan_feature_df = pd.read_parquet("chan_feature_df.parquet")
# frange__now_seg__range: object, fcmp__now_seg__range_rate12_cmp: object, fcmp__now_seg__range_rate13_cmp: object, feachan__last_seg__is_sure: object, frange__last_seg__range: object, fcmp__last_seg__range_rate12_cmp:
#  object, fcmp__last_seg__range_rate13_cmp: object, frange__now_seg__zs1: object, frange__now_seg__zs1after: object, frange__now_seg__zs1before: object, frange__last_seg__zs1: object, frange__last_seg__zs1after: 
# object, frange__last_seg__zs1before: object, feachan__now_segseg__is_sure: object, frange__now_segseg__range: object, feachan__last_segseg__is_sure: object, frange__last_segseg__range: object, fcmp__now_segseg__
# range_rate12_cmp: object, fcmp__now_segseg__range_rate13_cmp: object, fcmp__last_segseg__range_rate12_cmp: object, fcmp__last_segseg__range_rate13_cmp: object, frange__now_segseg__zs1: object, frange__now_segseg
# __zs1after: object, frange__now_segseg__zs1before: object, frange__last_segseg__zs1: object, frange__last_segseg__zs1after: object, frange__last_segseg__zs1before
print("read data finish")
chan_feature_df.fillna(np.nan, inplace=True)
if "type" in chan_feature_df.columns:
    chan_feature_df["type"] = chan_feature_df["type"].map(lambda x:x[0])
    chan_feature_df = pd.get_dummies(chan_feature_df, columns=['type'])


X_drop_list = ["now_seg", "last_seg", "now_segseg", "last_segseg", "now_segzs", "last_segzs", "now_seg_segzs", "last_seg_segzs"]

X_drop_list += ["time", "label"]
X_drop_list += [c for c in chan_feature_df.columns if c.startswith("fcmp__") or c.startswith("frange__") or c.startswith("fpoint__") or c.endswith("__is_sure")]

X_drop_list += [c for c in chan_feature_df.columns if c.endswith("1__point")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("2__point")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("3__point")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("4__point")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("now__point")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("1__range_mean")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("2__range_mean")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("3__range_mean")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("4__range_mean")]
X_drop_list += [c for c in chan_feature_df.columns if c.endswith("now__range_mean")]

X_contain = [c for c in chan_feature_df.columns if c not in X_drop_list]
# 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train = chan_feature_df[chan_feature_df["time"] <="2022/07"]
test = chan_feature_df[chan_feature_df["time"] >"2022/07"]
# X_train = train
del chan_feature_df
y_train = train["label"]
X_train = train[X_contain]
X_train = X_train.replace([np.inf, -np.inf], np.nan)
y_train[y_train=="1low"] = 1
y_train[y_train=="1high"] = 0
y_train[y_train=="2low"] = 1
y_train[y_train=="2high"] = 0
y_train[y_train=="0"] = 0
# y_train[y_train=="1unknown"] = 0
# y_train[y_train=="2unknown"] = 0
# 创建 NaN 的标记列
# X_train['NaN_flag'] = X_train.isna().any(axis=1).astype(int)
# imputer = KNNImputer(n_neighbors=5)
# 1. 临时用特定值填充 NaN（比如 -999），并进行 SMOTE 过采样

# X_train_filled = pd.DataFrame(X_train_filled, columns=X_train.columns)

# X_train_filled = imputer.fit_transform(X_train)
# y_train = pd.Series(y_train).astype('category')

# # 使用 SMOTE 进行过采样
# smote = SMOTE(random_state=42)
# X_resampled, y_resampled = smote.fit_resample(X_train_filled, y_train)




y_test = test["label"]
X_test = test[X_contain]
X_test = X_test.replace([np.inf, -np.inf], np.nan)

y_test[y_test=="1low"] = 1
y_test[y_test=="1high"] = 0
y_test[y_test=="2low"] = 1
y_test[y_test=="2high"] = 0
y_test[y_test=="0"] = 0
# y_test[y_test=="1unknown"] = 0
# y_test[y_test=="2unknown"] = 0

X_test.to_parquet("X_testbi.parquet")
y_test.to_pickle("y_testbi.pickle")
X_train.to_parquet("X_trainbi.parquet")
y_train.to_pickle("y_trainbi.pickle")




# xgb_clf = xgb.XGBClassifier(objective='multi:softmax', num_class=5, max_depth=7, learning_rate=0.1, n_jobs=16)
# xgb_clf.fit(X_train, y_train)
# xgb_clf.save_model("xgb.model.json")

# # 转换为 XGBoost 数据格式
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# 设置 XGBoost 参数
params = {
    'objective': 'binary:logistic',  # 多分类问题，输出类别概率
    'num_class': 2,                # 类别数
    'max_depth': 7,                #  树的最大深度
    'eta': 0.3,                    # 学习率
    'eval_metric': 'mlogloss',     # 使用log损失作为评价指标
}

# 
# #
train_size = len(X_train)
pct = 0.1
eval_size = int(train_size * pct)
print("eval_size", eval_size)

xgb_model = xgb.XGBClassifier(random_state=42, n_jobs=30, eval_metric='map@{}'.format(eval_size))
# xgb_model = xgb.XGBClassifier(random_state=42, n_jobs=100, eval_metric='aucpr')
# feature_weights=feature_weight, 

# 4. 设置参数网格
param_grid = {
    'eta': [0.1],  # 学习率
    'n_estimators': [100],    # 弱学习器的个数
    # 'max_delta_step': [1, 2, 3],  # 有助于类别不平衡
    'scale_pos_weight': [2,3],  # 控制正负样本权重
    'max_depth': [5,6,7,8,9,10,11,12,13],             # 树的最大深度
    'subsample': [0.9],       # 每棵树使用数据的比例
    'colsample_bytree': [0.5],# 每棵树随机采样的特征比例
    'gamma': [0.2],             # 惩罚项
    'min_child_weight': [5]       # 最小叶子节点样本权重和
}

# param_grid = {

#     'learning_rate': [0.01, 0.1, 0.3],  # 学习率

# }

# 5. 初始化 GridSearchCV
# grid_search = GridSearchCV(estimator=xgb_model, 
#                            param_grid=param_grid, 
#                            scoring='accuracy', 
#                            cv=5, 
#                            n_jobs=1,
#                            )

# # 6. 执行超参数搜索
# grid_search.fit(X_train, list(y_train))

# # 7. 输出最优参数
# print("最优参数组合：", grid_search.best_params_)
# print("最优得分：", grid_search.best_score_)

# # 8. 使用最优模型预测测试集
# bst = grid_search.best_estimator_
# bst.save_model("{}.xgb.model.json".format(time_stamp))

# print("feature", X_resampled.columns)

# 保存每一个超参数组合对应的模型
all_models = []
for params in ParameterGrid(param_grid):
    # 设置模型参数
    xgb_model.set_params(**params)
    xgb_model.fit(X_train, y_train)
    
    # 保存模型
    model_filename = f'{time_stamp}.model_lr_depth_{params["max_depth"]}.scale_pos_weight_{params["scale_pos_weight"]}.joblib'
    xgb_model.save_model(model_filename)
    try:
        dot_data = xgb.to_graphviz(xgb_model, num_trees=0)
        dot_data.render("{}.svg".format(model_filename), format="svg")
    except Exception as e:
        print(e)

    try:
        # df1 = xgb_model.trees_to_dataframe()
        gain = xgb_model.feature_importances__score(importance_type='gain')
        weight = xgb_model.get_score(importance_type='weight')
        cover =  xgb_model.get_score(importance_type="cover")
        dfg = pd.DataFrame(list(gain.items()), columns=['feature', 'gain'])
        dfw = pd.DataFrame(list(weight.items()), columns=['feature', 'weight'])
        dfc = pd.DataFrame(list(cover.items()), columns=['feature', 'cover'])
        dfg["cover"] = dfc["cover"]
        dfg["weight"] = dfw["weight"]
        dfg.to_csv("{}.tree.xls".format(model_filename), index=False)
    except Exception as e:
        print(e)
    all_models.append(model_filename)
    
bst = xgb_model


y_pred_prob = bst.predict(X_test)
# y_pred = y_pred_prob.argmax(axis=1)

# 保存每一个参数组合的模型
# models = grid_search.cv_results_['models']
# for i, model in enumerate(models):
#     model.save_model("{}.xgb.model_{}.json".format(time_stamp, i))




lb = LabelBinarizer()
y_true_binary = lb.fit_transform(list(y_test))

# 9. 计算并输出准确率
try:
    accuracy = accuracy_score(y_true_binary, y_pred_prob)

    print("测试集准确率：", accuracy)

except Exception as e:
    print(e)





# # 训练模型
# num_round = 50  # 决策树的数量（即迭代次数）
# bst = xgb.train(params, dtrain, num_boost_round=num_round)

# 预测 (概率分布)
# y_pred_prob = bst.predict(dtest)

dot_data = xgb.to_graphviz(bst, num_trees=0)
try:
    dot_data.render("tree", format="svg")
    with open("{}.xgb.model.dot".format(time_stamp), "w") as f:
        f.write(dot_data.source)
except Exception as e:
    print(e)

# 预测测试集
# y_pred = xgb_clf.predict(X_test)
# y_pred = y_pred_prob.argmax(axis=1)

# # 评估模型
# accuracy = accuracy_score(list(y_test), y_pred)
# print("Accuracy:", accuracy)