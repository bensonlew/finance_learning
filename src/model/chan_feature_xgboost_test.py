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
# 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train = chan_feature_df[chan_feature_df["time"] <="2023/07"]
test = chan_feature_df[chan_feature_df["time"] >"2023/07"]
# X_train = train
y_train = train["label"]
X_train = train[X_contain]
X_train = X_train.replace([np.inf, -np.inf], np.nan)
y_train[y_train=="1low"] = 3
y_train[y_train=="1high"] = 1
y_train[y_train=="2low"] = 4
y_train[y_train=="2high"] = 2
y_train[y_train=="0"] = 0
# y_train[y_train=="1unknown"] = 0
# y_train[y_train=="2unknown"] = 0
# 创建 NaN 的标记列
# X_train['NaN_flag'] = X_train.isna().any(axis=1).astype(int)
# imputer = KNNImputer(n_neighbors=5)
# 1. 临时用特定值填充 NaN（比如 -999），并进行 SMOTE 过采样
imputer = SimpleImputer(strategy='constant', fill_value=-99999)  # 临时填充 -999
X_train_temp = imputer.fit_transform(X_train)
y_train = pd.Series(y_train).astype('category')

# 2. 执行 SMOTE 过采样
# smote = SMOTE(random_state=42)
# X_resampled, y_resampled = smote.fit_resample(X_train_temp, y_train)

# # 3. 将临时值 (-999) 恢复为 NaN
# X_resampled = pd.DataFrame(X_resampled, columns=X_train.columns)
# X_resampled.columns = X_train.columns
# X_resampled.replace(-99999, np.nan, inplace=True)
# X_train_filled = pd.DataFrame(X_train_filled, columns=X_train.columns)

# X_train_filled = imputer.fit_transform(X_train)
# y_train = pd.Series(y_train).astype('category')

# # 使用 SMOTE 进行过采样
# smote = SMOTE(random_state=42)
# X_resampled, y_resampled = smote.fit_resample(X_train_filled, y_train)




y_test = test["label"]
X_test = test[X_contain]
X_test = X_test.replace([np.inf, -np.inf], np.nan)

y_test[y_test=="1low"] = 3
y_test[y_test=="1high"] = 1
y_test[y_test=="2low"] = 4
y_test[y_test=="2high"] = 2
y_test[y_test=="0"] = 0
# y_test[y_test=="1unknown"] = 0
# y_test[y_test=="2unknown"] = 0

X_test.to_parquet("X_test.parquet")
y_test.to_pickle("y_test.pickle")
# X_train.to_parquet("X_train.parquet")
# y_train.to_pickle("y_train.pickle")




# xgb_clf = xgb.XGBClassifier(objective='multi:softmax', num_class=5, max_depth=7, learning_rate=0.1, n_jobs=16)
# xgb_clf.fit(X_train, y_train)
# xgb_clf.save_model("xgb.model.json")

# # 转换为 XGBoost 数据格式
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# 设置 XGBoost 参数
params = {
    'objective': 'multi:softprob',  # 多分类问题，输出类别概率
    'num_class': 5,                # 类别数
    'max_depth': 7,                # 树的最大深度
    'eta': 0.3,                    # 学习率
    'eval_metric': 'mlogloss',     # 使用log损失作为评价指标
}

# 
# # 
# 3. 定义 XGBoost 模型
feature_weight_dict= {
    0: 1,
    1: 4,
    2: 12,
    3: 7,
    4: 12
}

feature_weight = np.array(list(feature_weight_dict.values()))
xgb_model = xgb.XGBClassifier(objective="multi:softprob", num_class=5, random_state=42, n_jobs=100, eval_metric='aucpr')
# feature_weights=feature_weight, 

# 4. 设置参数网格
param_grid = {
    'num_class': [5],
    'objective': ['multi:softprob'],
    'eta': [0.1],  # 学习率
    'n_estimators': [100],    # 弱学习器的个数
    'max_depth': [9, 10, 11, 12],             # 树的最大深度
    'subsample': [ 0.9],       # 每棵树使用数据的比例
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
# X_resampled.to_csv("X_resampled.csv")
