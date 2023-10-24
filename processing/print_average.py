# Get data from trials and take average
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

TRIALS = 6

##### Read and calculate average data points #####

y_p = np.empty(11)

for i in range(1, TRIALS + 1):
    
    # Read the data
    data = np.genfromtxt('data/trial_{}.csv'.format(i), delimiter=',')
    y = data[:, 1]

    # Add to the average
    y_p = np.add(y_p, y)

# Divide by the number of trials
y_p = np.divide(y_p, TRIALS)

# round to 1 dp
y_p = np.round(y_p, 1)

print(y_p)

# first clear file
with open('data/average.csv', 'w') as f:
    f.write('')


counter = 1500
for p in y_p:
    with open('data/average.csv', 'a') as f:
        f.write(str(counter) + ',' + str(p) + '\n')
    counter -= 100