
for c in `cat code.list `; do echo "python ../../../finance_learning/src/feature_engineering/etf_add_feature_day.py "$c" qfq.merge.kdj.parquet"; done > merge_future.sh
for c in `cat code.list `; do echo "python ../../../finance_learning/src/feature_engineering/chanfeature.py "$c" qfq.kdj.day.parquet "; done > chan_future.sh




~/sg-users/liubinxu/soft/finiance/stock_data/finiance/chan_train3




~/sg-users/liubinxu/soft/miniconda3_py312/bin/python ../../../finance_learning/src/model/chan_feature_xgboost_bi.py "*feature_chan.all.json" 1 > log 2> err

for f in `ls 20250119183232*2.joblib`; do ~/sg-users/liubinxu/soft/miniconda3_py312/bin/python ../../../finance_learning/src/model/chan_feature_xgboost_bi_pinggu.py $f & done
~/sg-users/liubinxu/soft/miniconda3_py312/bin/python ../../../finance_learning/src/utils/model_test.py  20250119183232.model_lr_depth_5.scale_pos_weight_3.joblib_pr.csv 20250119183232.model_lr_depth_6.sc
ale_pos_weight_3.joblib_pr.csv 20250119183232.model_lr_depth_7.scale_pos_weight_3.joblib_pr.csv 20250119183232.model_lr_depth_8.scale_pos_weight_3.joblib_pr.csv 20250119183232.model_lr_depth_9.scale_pos_weight_
3.joblib_pr.csv 20250119183232.model_lr_depth_10.scale_pos_weight_3.joblib_pr.csv 20250119183232.model_lr_depth_11.scale_pos_weight_3.joblib_pr.csv 20250119183232.model_lr_depth_12.scale_pos_weight_3.joblib_pr.
csv 20250119183232.model_lr_depth_13.scale_pos_weight_3.joblib_pr.csv

 ~/sg-users/liubinxu/soft/miniconda3_py312/bin/python ../../../finance_learning/src/utils/feature_des.py X_trainbi.parque