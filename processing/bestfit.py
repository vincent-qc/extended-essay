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
    fmt='.', capsize=3, capthick=0.5, elinewidth=0.5, color='#6022bd',
    label='Trial Averages'
)
plt.legend()

##### Calculate the bestfit #####
def f(x, a, b, c):
    return a + b * np.exp(-c * np.sqrt(x))
    # return a + ((b - a) * np.exp(-c * (pow(x, 0.5))))

popt, pcov = curve_fit(f, x_p, y_p, [23, 40, 0.02], bounds=([20, 30, 0], [30, 50, 1]))

# Plot the bestfit
x_b= np.linspace(350, 1700, 1300)

# Final Temperature
y_b = f(x_b, *popt)

# Plot the bestfit
ax.plot(x_b, y_b, label='Best Fit', color='#63d0f7')
plt.legend()
text = "Best fit equation: $T = {} + {}e^{{ -{}n_f^{{ \\frac{{1}}{{2}} }} }}$".format(
    round(popt[0], 1),
    round(popt[1], 1),
    round(popt[2], 4)
)

plt.text(
    0.04, 0.06,
    text,
    transform=ax.transAxes,
    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round', pad=0.5, edgecolor='grey')
)


# Add labels
plt.xlabel('Fan Speed (RPM)', labelpad=6)
plt.ylabel('Final Temperature ($^\circ C$)', labelpad=6)
plt.title('Final Temperature vs. Fan Speed', pad=10, fontsize=12)

# Change axes
plt.xlim(350, 1700)
plt.ylim(35, 45)

plt.grid(True, color='#C5C5CA')


# Save the plot to a file
plt.savefig('images/bestfit.png')