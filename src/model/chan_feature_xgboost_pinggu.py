import pandas as pd
import matplotlib.pyplot as plt
import json
import datetime
import numpy as np
import sys
import xgboost as xgb
import glob
from sklearn.model_selection import GridSearchCV
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc, precision_recall_curve

model = sys.argv[1]


# y_test[y_test=="2unknown"] = 0


y_test = pd.read_pickle("y_test.pickle")
X_test = pd.read_parquet("X_test.parquet")

# 加载模型


bst = xgb.Booster()
bst.load_model(model)

feature_names = X_test.columns.tolist()
bst.feature_names = feature_names
tree_df = bst.trees_to_dataframe()
tree_df.to_csv("{}.tree.xls".format(model), index=False)

dot_data = xgb.to_graphviz(bst, num_trees=0)
try:
    dot_data.render("{}.tree".format(model), format="svg")
    with open("{}.xgb.model.dot".format(model), "w") as f:
        f.write(dot_data.source)
except Exception as e:
    print(e)

# 预测
y_pred = bst.predict(xgb.DMatrix(X_test))
y_pred1 = y_pred.argmax(axis=1)
y_test = y_test.to_list()

# 评估模型
accuracy = accuracy_score(y_test, y_pred1)
precision = precision_score(y_test, y_pred1, average='macro')
recall = recall_score(y_test, y_pred1, average='macro')
f1 = f1_score(y_test, y_pred1, average='macro')
roc_auc = roc_auc_score(y_test, y_pred, multi_class='ovr')
confusion_matrix = confusion_matrix(y_test, y_pred1)
classification_report = classification_report(y_test, y_pred1)

print("准确率：", accuracy)
print("精确率：", precision)
print("召回率：", recall)
print("F1-score：", f1)
print("混淆矩阵：\n", confusion_matrix)
print("ROC-AUC：", roc_auc)
print("分类报告：\n", classification_report)




for i in range(5):
    y_pred_proba_class = y_pred[:, i]
    y_test_class = (np.array(y_test) == i).astype(int)  
    # fpr, tpr, thresholds = roc_curve(y_test_class, y_pred_proba_class)
    print(len(y_pred_proba_class), len(y_test_class))
    precision, recall, thresholds = precision_recall_curve(y_test_class, y_pred_proba_class)
    print(len(precision), len(recall), len(thresholds))
    # 计算 AUC
    # auc_value = auc(fpr, tpr)
    roc_df = pd.DataFrame()
    roc_df["precision"] = precision 
    roc_df["recall"] = recall
    roc_df["thresholds"] = np.append(thresholds, [1.0])
    roc_df.to_csv("{}_{}_pr.csv".format(model, i), sep="\t")




