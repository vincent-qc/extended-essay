import numpy as np
import math
import matplotlib.pyplot as plt
import scipy as sp


TRIALS = 6

##### Read and calculate average data points #####
x_p = []
y_p = np.empty(11)

# Create array to calculate standard of sample deviation for every fan speed
y_s = np.empty(11)

def sample_standard_deviation(*arrays):
    stacked_arrays = np.stack(arrays)
    deviations = np.std(stacked_arrays, axis=0, ddof=1)
    return deviations

arrays = []

for i in range(1, TRIALS + 1):
    
    # Read the data
    data = np.genfromtxt('data/trial_{}.csv'.format(i), delimiter=',')
    y = data[:, 1]

    arrays.append(y)

uncertainties = sample_standard_deviation(*arrays)

with open('data/uncertainties.csv', 'w') as f:
    f.write('')

counter = 1500
for s in uncertainties:
    s = round(s, 1)
    with open('data/uncertainties.csv', 'a') as f:
        f.write(str(counter) + ',' + str(s) + '\n')
    counter -= 100