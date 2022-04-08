import numpy as np 

inputs = [[2, 3, 6, 7.8],
          [-3.0, 4.6, 9.3,-2.1],
          [5, 4, 8, 9.2]]

weights = [[0.2, 0.8, -0.5, 1.0],
           [0.5, -0.91, 0.26, -0.5],
           [-0.26, -0.27, 0.17, 0.87]]

biases = [2, 3, 0.8] 

output = np.dot(weights, inputs) + biases
print(output)