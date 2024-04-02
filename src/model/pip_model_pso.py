# 使用pso计算PipPatternModel的最优参数
import numpy as np
from pyswarm import pso
from sko.PSO import PSO
import json
import copy
from .pip_pattern_model import PipPatternModel

amount = ['amount_normalize20_rolling_24_mean', 'amount_normalize20_rolling_24_exp_mean',
            'amount_normalize20_rolling_96_mean', 'amount_normalize20_rolling_96_exp_mean',
            'amount_normalize20_rolling_480_mean', 'amount_normalize20_rolling_480_exp_mean']
reg = ["close24_close480", "close480_close2880"]
reg_type = ["all", "up", "down"]
k_type = ["K18", "K36", "K72"]
n_pips = [5, 6, 7, 8, 9]
look_back = [240, 480, 960, 2880]
hold_period=[3, 6, 12, 36]
target_close = ["target_close1", "target_close2", "target_close5", "target_close10"]

params_ranges = [
    amount,
    reg,
    reg_type,
    k_type,
    n_pips,
    look_back,
    hold_period
]


model_params = {
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
    
    for n, param_name in enumerate(["amount", "reg", "reg_type", "k_type", "n_pips", "lookback", "hold_period"]):
        model_params1["train"][param_name] = params_ranges[n][np.round(params[n])]
    name = "_".join([str(x) for x in model_params1["train"].values()])
    with open("params{}.json".format(name), "w") as f:
        json.dump(model_params1, f)
    return "params{}.json".format(name)


# Define the objective function
def objective_function(params):
    # TODO: Define your objective function based on the PipPatternModel
    # Use the params variable to set the parameter values
    
    # Return the objective value
    model = PipPatternModel()
    params_file = convert_params(params)
    version = "1"
    model.version = version
    model.load_params_from_file(params_file)
    model.set_train_test_data()
    return model.train_and_test_run()

    
# Define the bounds for each parameter
# TODO: Set the appropriate bounds for each parameter
lower_bounds = [0 for i in params_ranges]
upper_bounds = [len(i) -1 for i in params_ranges]

# Set the number of particles and iterations for PSO
num_particles = 30
num_iterations = 100

# Run PSO optimization
# best_params, best_value = pso(objective_function, lower_bounds, upper_bounds, swarmsize=num_particles, maxiter=num_iterations)
pso = PSO(func=objective_function, dim=len(params_ranges), pop=50, max_iter=800, lb=lower_bounds, ub=upper_bounds)
pso.set_run_mode('multiprocessing')
best_params, best_performance = pso.run()
# Print the best parameters and objective value
print("Best Parameters:"q, best_params)
print("Best Objective Value:", best_value)