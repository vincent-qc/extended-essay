import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Settings
plt.rcParams['figure.dpi'] = 300
fig, ax = plt.subplots()

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



##### Plot the data points #####
plt.errorbar(
    x_p, y_p, xerr=x_p*0.10, yerr=2,
    fmt='.', capsize=3, capthick=0.5, elinewidth=0.5, color='#6022bd',
    label='Trial Averages'.format(i)
)
plt.legend()

##### Calculate the bestfit #####
def f(x, a, b, c):
    return a + (b - a) * pow(math.e, (-c * pow(x, 0.5)))
    # return a + ((b - a) * np.exp(-c * (pow(x, 0.5))))

popt, pcov = curve_fit(f, x_p, y_p, [23, 60, 0.02], bounds=([20, 50, 0], [30, 70, 1]))

print(popt)
print("A: {}".format(popt[0]))
print("B: {}".format(popt[1]))
print("C: {}".format(popt[2]))


# Plot the bestfit
x_b= np.linspace(350, 1750, 1400)

# Final Temperature
y_b = f(x_b, *popt)

x_b_lower = x_b + (x_b * 0.10)
x_b_upper = x_b - (x_b * 0.10)

y_b_upper = f(x_b_upper, *popt) + 2
y_b_lower = f(x_b_lower, *popt) - 2

# Plot the bestfit
ax.plot(x_b, y_b, label='Best Fit', color='#63d0f7')
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

# Plot the model
ax.plot(x_m, y_m, label='Model', color='r')
plt.legend()

# Add labels
plt.xlabel('Fan Speed (RPM)')
plt.ylabel('Final Temperature ($^\circ C$)')
plt.title('Final Temperature vs. Fan Speed')

# Change axes
plt.xlim(350, 1750)
plt.ylim(31, 49)

plt.grid(True, color='#C5C5CA')


# Save the plot to a file
plt.savefig('images/full.png')