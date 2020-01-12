'''
Task 1: plot a function y = np.sqrt( (x*x + np.sin(15*x)*np.sin(15*x)) ) / (1-x)
when x = [0, 1] with 50 intervals

Tast 2: plot the same function when x = [0, 0.5] with 100 intervals
'''

# Step 1: load modules
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.simplefilter('error') # Convert runtime warnings into errors

# Step 2: Define domain x
# TODO: complete the declaration of x
x = np.zeros(51)

# Step 3: Denote y as a function of x
# TODO: complete the declaration of y
y = x

# Step 4: Plot y
plt.plot(x, y, '-o')
plt.show()