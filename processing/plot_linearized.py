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

##### Linearize the data #####
x_p_lin = x_p
y_p_lin = pow(np.log((y_p - 23) / 37), 2)

plt.figure(figsize=(10,6))

##### Plot the data points #####
plt.errorbar(
    x_p_lin, y_p_lin, xerr=0.10, yerr=2/y_p,
    fmt='.', capsize=3, capthick=0.5, elinewidth=0.5, color='#1a61db',
    label='Trial Averages'.format(i)
)
plt.legend()

##### Calculate the bestfit #####
def f(x, a, b,):
    return a * x + b

popt, pcov = curve_fit(f, x_p_lin, y_p_lin)


# Plot the bestfit
x_b = np.linspace(350, 1750, 1400)

# Final Temperature
y_b = f(x_b, *popt)

"""x_b_lower = x_b + (x_b * 0.10)
x_b_upper = x_b - (x_b * 0.10)

y_b_upper = f(x_b_upper, *popt) + 2
y_b_lower = f(x_b_lower, *popt) - 2"""

# Plot the bestfit
plt.plot(x_b, y_b, label='Bestfit', color='#0d9dd6')
# plt.fill_between(x_b, y_b_lower, y_b_upper, alpha=0.2, color='#15c2ed', label='Bestfit Error') 
plt.legend()


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

x_m_lin = x_m
y_m_lin = pow(np.log((y_m - 23) / 37), 2)


# Plot the model
plt.plot(x_m_lin, y_m_lin, label='Model', color='r')
plt.legend()

# Add labels
plt.title('Final Temperature vs. Fan Speed', fontdict={'fontsize': 18})

plt.xlabel('Fan Speed (RPM)', fontdict={'fontsize': 14})
plt.ylabel('$\ln(\\frac{ T - T_{\infty}}{T_0 - T_{\infty}})^2$', fontdict={'fontsize': 14})


# Change axes
#plt.xlim(350, 1750)
#plt.ylim(31, 49)


# Save the plot to a file
plt.savefig('images/linearized.png')

