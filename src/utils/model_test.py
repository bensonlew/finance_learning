import pandas as pd
import numpy as np
import sys
# 表格格式如下, 分别 统计最后1%。 2% ， 5%， 10%。. 20% 的数据 precision, recall, thresholds 的平均值
#         precision       recall  thresholds
# 0       0.15187289678380317     1.0     0.00018312197062186897
# 1       0.1518749913801426      1.0     0.00020458942162804306
# 2       0.15187708603425923     1.0     0.00023338115715887398

# 1% 2% 5% 10% 20% 的平均值

def calculate_metrics_averages(df):
    # 计算需要取的行数
    total_rows = len(df)
    percentages = {
        '1%': int(total_rows * 0.01),
        '2%': int(total_rows * 0.02),
        '5%': int(total_rows * 0.05),
        '10%': int(total_rows * 0.10),
        '20%': int(total_rows * 0.20)
    }
    
    results = {}
    for percent, n_rows in percentages.items():
        # 取最后n_rows行数据
        subset = df.tail(n_rows)
        
        # 计算平均值
        avg_values = subset.mean()
        
        
        results[percent] = {
            'precision': avg_values['precision'],
            'recall': avg_values['recall'],
            'thresholds': avg_values['thresholds']
        }
    
    return results

def stat_one_file(file_path):
    df = pd.read_table(file_path, header=0)  # 或者其他方式读取数据
    results = calculate_metrics_averages(df)
    # 打印结果
    deps = file_path.split('.')[1]
    res = {}
    res["deps"] = deps
    for percent, metrics in results.items():
        res["pre" + percent] = metrics['precision']
        res["rec" + percent] = metrics['recall']
        # print(f"\n{percent} 的平均值:")
        # print(f"Precision: {metrics['precision']:.4f}")
        # print(f"Recall: {metrics['recall']:.4f}")
        # print(f"Thresholds: {metrics['thresholds']:.4f}")
    return res

def stat_all_files(file_paths):
    res = []
    for file in file_paths:
        res.append(stat_one_file(file))
    res_df= pd.DataFrame(res)
    res_df.to_csv("res.csv", index=False, sep='\t')
    


if __name__ == "__main__":
    stat_all_files(sys.argv[1:])
