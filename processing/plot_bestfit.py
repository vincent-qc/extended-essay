import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

TRIALS = 3

##### Read and calculate average data points #####
x_p = []
y_p = np.empty(11)

for i in range(1, TRIALS + 1):
    
    # Read the data
    data = np.genfromtxt('data/trial_{}.csv'.format(i), delimiter=',')
    x = data[:, 0]
    y = data[:, 1]

    # Add to the average
    x_p = x
    y_p = np.add(y_p, y)

# Divide by the number of trials
y_p = np.divide(y_p, TRIALS)


##### Calculate the bestfit #####
def f(x, a, b, c, d):
    return a * np.exp(-b * (pow((d * x), 0.5))) + c

popt, pcov = curve_fit(f, x_p, y_p, [(60 - 23), 0, 23, 3])

##### Plot the model #####
# Fan Speed
x_m = np.linspace(350, 1750, 1400)

# Velocity, Reynolds number, Nusselt number, and heat transfer coefficient respectively
v = (93.4 * (x_m/1500) * (1/3600)) / pow(0.12, 2)
r = (v * 0.05) / (1.70 * pow(10, -5))
n = 0.664 * pow(r, (1/2)) * pow(0.724, (1/3))
h = (n * 0.0266) / 0.05

# Final Temperature
y_m = 23 + (60 - 23) * pow(math.e, (-h * 0.05 * 0.015 * 60))

# Plot the model
plt.plot(x_m, y_m, label='Model')
plt.legend()


##### Plot the bestfit #####
x_b= np.linspace(350, 1750, 1400)

# Final Temperature
y_b = f(x_m, *popt)

# Plot the bestfit
plt.plot(x_b, y_b, label='Bestfit')
plt.legend()

# Save the bestfit plot
plt.savefig('images/bestfit.png')