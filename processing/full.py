import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Settings
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = "STIXgeneral"

# ensure tex is also in stixgeneral font
plt.rcParams['mathtext.fontset'] = 'stix'
fig, ax = plt.subplots()


# Read from data/average.csv
data = np.genfromtxt('data/average.csv', delimiter=',')
x_p = data[:, 0]
y_p = data[:, 1]

# read uncertainties from data/uncertainties.csv
uncertainties = np.genfromtxt('data/uncertainties.csv', delimiter=',')
y_unc = uncertainties[:, 1]

##### Plot the data points #####
plt.errorbar(
    x_p, y_p, xerr=x_p*0.10, yerr=y_unc,
    fmt='.', capsize=0, elinewidth=0.8, color='#6022bd',
    label='Trial Averages'
)
plt.legend()

##### Calculate the bestfit #####
def f(x, a, b, c):
    return a + b * pow(math.e, (-c * pow(x, 0.5)))
    # return a + ((b - a) * np.exp(-c * (pow(x, 0.5))))

popt, pcov = curve_fit(f, x_p, y_p, [23, 40, 0.02], bounds=([20, 30, 0], [30, 50, 1]))

# Plot the bestfit
x_b= np.linspace(0, 3000, 3000)

# Final Temperature
y_b = f(x_b, *popt)

# Plot the bestfit
ax.plot(x_b, y_b, label='Best Fit', color='#63d0f7')
# plt.fill_between(x_b, y_b_lower, y_b_upper, alpha=0.2, color='#15c2ed', label='Bestfit Error') 
plt.legend()

##### Plot the model #####
# Fan Speed
x_m = np.linspace(0, 3000, 3000)

# Velocity, Reynolds number, Nusselt number, and heat transfer coefficient respectively
v = (93.4 * (x_m/1500) * (1/3600)) / pow(0.12, 2)
r = (v * 0.05) / (1.70 * pow(10, -5))
n = 0.664 * pow(r, (1/2)) * pow(0.724, (1/3))
h = (n * 0.0266) / 0.05

# Final Temperature
y_m = 22.2 + (60 - 22.2) * pow(math.e, (-(h / (386 * 0.00439)) * 0.05 * 0.015 * 60))

# Plot the model
ax.plot(x_m, y_m, label='Model', color='r')
plt.legend()

y_m_upper = 22.3 + (38.7) * np.exp(-0.0150 * pow(x_m, 0.5))
y_m_lower = 22.1 + (36.9) * np.exp(-0.0166 * pow(x_m, 0.5))
ax.fill_between(x_m, y_m_lower, y_m_upper, alpha=0.2, color='r', label='Model Uncertainty')
plt.legend()



# Add labels
plt.xlabel('Fan Speed (RPM)', labelpad=6)
plt.ylabel('Final Temperature ($^\circ C$)', labelpad=6)
plt.title('Final Temperature vs. Fan Speed', pad=10, fontsize=16)

# Change axes
plt.xlim(0, 3000)
plt.ylim(19, 61)

# plot bestfit asymptote
plt.axhline(y=20.0, color='#192fd1', linestyle='--', linewidth=0.8, label="Best Fit Horizontal Asymptote")
plt.legend()

# plot model asymptote
plt.axhline(y=22.2, color='#f763c3', linestyle='--', linewidth=0.8, label="Model Horizontal Asymptote")
plt.fill_betweenx([22.1, 22.3], 0, 3000, alpha=0.2, color='#f763c3', label='Model Asymptote Uncertainty')
plt.legend()

plt.grid(True, color='#C5C5CA')


# Save the plot to a file
plt.savefig('images/full.png')