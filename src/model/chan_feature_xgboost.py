
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


chan_feature_files = glob.glob(sys.argv[1])

feature_list = []
for chan_feature_file in chan_feature_files:
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

X_drop_list = ["now_seg", "last_seg", "now_segseg", "last_segseg", "now_segzs", "last_segzs", "now_seg_segzs", "last_seg_segzs"]
X_drop_list += ["time", "label"]

X_contain = [c for c in chan_feature_df.columns if c not in X_drop_list]

# 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
train = chan_feature_df[chan_feature_df["time"] <="2023"]
test = chan_feature_df[chan_feature_df["time"] >"2023"]
# X_train = train
y_train = train["label"]
X_train = train[X_contain]
y_train[y_train=="1low"] = 3
y_train[y_train=="1high"] = 1
y_train[y_train=="2low"] = 4
y_train[y_train=="2high"] = 2
y_train[y_train=="0"] = 0
# y_train[y_train=="1unknown"] = 0
# y_train[y_train=="2unknown"] = 0


y_test = test["label"]
X_test = test[X_contain]

y_test[y_test=="1low"] = 3
y_test[y_test=="1high"] = 1
y_test[y_test=="2low"] = 4
y_test[y_test=="2high"] = 2
y_test[y_test=="0"] = 0
# y_test[y_test=="1unknown"] = 0
# y_test[y_test=="2unknown"] = 0




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
xgb_model = xgb.XGBClassifier(objective="multi:softprob", num_class=5, random_state=42, feature_weights=feature_weight, n_jobs=16)

# 4. 设置参数网格
param_grid = {
    'num_class': [5],
    'objective': ['multi:softprob'],
    'eta': [0.01, 0.1, 0.3],  # 学习率
    # 'n_estimators': [100, 200, 300],    # 弱学习器的个数
    'max_depth': [ 5, 6, 7],             # 树的最大深度
    # 'subsample': [0.5, 0.7, 0.9],       # 每棵树使用数据的比例
    # 'colsample_bytree': [0.5, 0.7, 0.9],# 每棵树随机采样的特征比例
    # 'gamma': [0, 0.1, 0.2],             # 惩罚项
    'min_child_weight': [3, 5]       # 最小叶子节点样本权重和
}

# param_grid = {

#     'learning_rate': [0.01, 0.1, 0.3],  # 学习率

# }

# 5. 初始化 GridSearchCV
grid_search = GridSearchCV(estimator=xgb_model, 
                           param_grid=param_grid, 
                           scoring='accuracy', 
                           cv=5, 
                           n_jobs=3,
                           )

# 6. 执行超参数搜索
grid_search.fit(X_train, list(y_train))

# 7. 输出最优参数
print("最优参数组合：", grid_search.best_params_)
print("最优得分：", grid_search.best_score_)

# 8. 使用最优模型预测测试集
bst = grid_search.best_estimator_
bst.save_model("xgb.model.json")

y_pred_prob = bst.predict(X_test)
# y_pred = y_pred_prob.argmax(axis=1)


# 9. 计算并输出准确率
try:
    accuracy = accuracy_score(list(y_test), y_pred_prob)
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
    with open("model.dot", "w") as f:
        f.write(dot_data.source)
except Exception as e:
    print(e)

# 预测测试集
# y_pred = xgb_clf.predict(X_test)
# y_pred = y_pred_prob.argmax(axis=1)

# # 评估模型
# accuracy = accuracy_score(list(y_test), y_pred)
# print("Accuracy:", accuracy)