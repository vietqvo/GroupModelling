from SALib.sample import saltelli
from SALib.sample import morris as morris_sample
from SALib.analyze import sobol
from SALib.analyze import morris
from SALib.test_functions import Ishigami

problem = {
  'num_vars': 4, 
  'names': ['x1', 'x2', 'x3','x4'], 
  'bounds': [[1.0,3.0], 
            [0.2,2.0], 
            [1.0,4.0],
            [0.2,2.0]]
}
param_values = saltelli.sample(problem, 1000, calc_second_order=False)
#print(len(param_values))
print(param_values)
Y = Ishigami.evaluate(param_values)
print(len(Y))
Si = sobol.analyze(problem, Y, print_to_console=True)



#morris method

#param_values = morris_sample.sample(problem, 10)
#print(len(param_values))