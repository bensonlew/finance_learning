# 使用pso计算PipPatternModel的最优参数
import numpy as np
# from pyswarm import pso
from sko.PSO import PSO
from sko.tools import set_run_mode
import json
import copy
import time
from pip_pattern_model import PipPatternModel
import os
import gc

amount = ['amount_normalize20_rolling_24_mean', 'amount_normalize20_rolling_24_exp_mean',
            'amount_normalize20_rolling_96_mean', 'amount_normalize20_rolling_96_exp_mean',
            'amount_normalize20_rolling_480_mean', 'amount_normalize20_rolling_480_exp_mean']
reg = ["close24_close480", "close480_close2880"]
# reg_type = ["all", "up", "down"]
# reg_type = ["down"]
# k_type = ["K18", "K36", "K72"]
k_type = ["K36", "K72"]
n_pips = [5, 6, 7, 8, 9]
look_back = [240, 480, 960, 2880]
# hold_period=[3, 6, 12, 36]
amount_type = ["no", "begin_end", "tail", "tree", "half", "all"]
target_close = ["target_close1", "target_close2", "target_close5", "target_close10"]

params_ranges = [
    amount,
    reg,
    # reg_type,
    k_type,
    n_pips,
    look_back,
    amount_type
    # hold_period
]


model_params = {
    "train": {
        "amount": "amount_normalize20_rolling_96_exp_mean",
        "reg": "close480_close2880",
        "reg_type": "down",
        "k_type": "K72",
        "n_pips": 9,
        "lookback": 480,
        "hold_period": 3,
        "k_range": 150,
        "amount_type": "tree",
        "close_std_type": "tree",
        "k_parent_retain": False,
        "amount_pct":0.1,
        "close_std_pct": 1.0
    },
    "test": {
        # 减少计算每个模型里保存不同的k
        "k_parent": None,
    },
    "evaluate": {
        "target_close": "target_close1"
    }
}

def convert_params(params):
    # Convert the parameters to the correct format
    model_params1 = copy.deepcopy(model_params)
    
    for n, param_name in enumerate(["amount", "reg", "k_type", "n_pips", "lookback", "amount_type"]):
        model_params1["train"][param_name] = params_ranges[n][int(np.round(params[n]))]
    name = "_".join([str(x) for x in model_params1["train"].values()])
    with open("params{}.json".format(name), "w") as f:
        json.dump(model_params1, f)
    return "params{}.json".format(name)


def convert_params2(params):
    # Convert the parameters to the correct format
    model_params1 = copy.deepcopy(model_params)
    
    for n, param_name in enumerate(["amount_pct", "close_std_pct"]):
        model_params1["train"][param_name] = round(params[n], 3)
    name = "_".join([str(x) for x in model_params1["train"].values()])
    with open("params_amount_std{}.json".format(name), "w") as f:
        json.dump(model_params1, f)
    return "params_amount_std{}.json".format(name)

# Define the objective function
def objective_function(params):
    # TODO: Define your objective function based on the PipPatternModel
    # Use the params variable to set the parameter values
    
    # Return the objective value
    model = PipPatternModel()

    params_file = convert_params2(params)
    if os.path.exists("{}.result".format(params_file)):
        with open("{}.result".format(params_file), 'r') as f:
            return - float(f.readline().strip())       

    elif os.path.exists("{}.start".format(params_file)):
        print("{} is running watting 100s".format(params_file))
        while True:
            time.sleep(100)
            print("{} is running watting 100s".format(params_file))
            if os.path.exists("{}.result".format(params_file)):
                break
        with open("{}.result".format(params_file), 'r') as f:
            return - float(f.readline().strip())
    os.system("touch {}.start".format(params_file))

    cmd = "python ../../../finance_learning/src/model/pip_pattern_model.py {}  train_test 1 > {}.log ".format(params_file, params_file)
    os.system(cmd)
    with open("{}.result".format(params_file), 'r') as f:
        getting = f.readline().strip() 

    # 多线程无法释放内存

    # version = "1"
    # model.version = version
    # model.load_params_from_file(params_file)
    # model.set_train_test_data()

    # getting = model.train_and_test_run()
    # with open("{}.result".format(params_file), 'w') as f:
    #     f.write("{}".format(getting))

    # 删除变量释放内存
    # del model
    # gc.collect()
    os.system("rm {}.start".format(params_file))
    
    return - float(getting)

def test_objective_function(params):
    # Test the objective function
    # 对params求平方和
    print("params is {}".format(params))
    time.sleep(2)
    return - np.sum(np.array(params) ** 2)

    
# Define the bounds for each parameter
# TODO: Set the appropriate bounds for each parameter
# lower_bounds = [0 for i in params_ranges]
# upper_bounds = [len(i) -1 for i in params_ranges]

lower_bounds = [0.2, 0.5]
upper_bounds = [0.4, 20.0]

# Set the number of particles and iterations for PSO
num_particles = 30
num_iterations = 100

# Run PSO optimization
# best_params, best_value = pso(objective_function, lower_bounds, upper_bounds, swarmsize=num_particles, maxiter=num_iterations)
set_run_mode(objective_function, 'multiprocessing')
# pso = PSO(func=objective_function, dim=len(params_ranges), pop=20, max_iter=50, lb=lower_bounds, ub=upper_bounds)
pso = PSO(func=objective_function, dim=2, pop=20, max_iter=50, lb=lower_bounds, ub=upper_bounds)
best_params, best_performance = pso.run()
# Print the best parameters and objective value
print("Best Parameters:", best_params)
print("Best Objective Value:", best_performance)