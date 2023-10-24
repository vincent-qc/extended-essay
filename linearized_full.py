import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

TRIALS = 5
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

##### Linearize the data #####
x_p_lin = np.sqrt(x_p)
y_p_lin = np.log(y_p - 20)

plt.figure(figsize=(10,6))

y_lin_upper = np.log(y_p + y_unc - 20) 
y_lin_lower = np.log(y_p - y_unc - 20)

y_lin_uncertainity = (y_lin_upper - y_lin_lower)/2

##### Plot the data points #####
plt.errorbar(
    x_p_lin, y_p_lin, xerr=0.05*x_p_lin, yerr=y_lin_uncertainity,
    fmt='.', capsize=3, capthick=0.5, elinewidth=0.5, color='#6022bd',
    label='Trial Averages'
)
plt.legend()

##### Calculate the bestfit #####
def f(x, b,):
    return -0.0181 * x + b

popt, pcov = curve_fit(f, x_p_lin, y_p_lin)


##### Plot the model #####
# Fan Speed
x_m = np.linspace(250, 1750, 1500)

# Final Temperature
y_m = 22.2 + (60 - 22.2) * np.exp(-0.0158 * np.sqrt(x_m))

x_m_lin = np.sqrt(x_m)
y_m_lin = np.log(y_m - 22.2)

y_m_lin_upper = np.log(0.2 + (38.7) * np.exp(-0.0150 * pow(x_m, 0.5)))
y_m_lin_lower = np.log(-0.2 + (36.9) * np.exp(-0.0166 * pow(x_m, 0.5)))


# Plot the model
plt.plot(x_m_lin, y_m_lin, label='Model', color='r')
plt.legend()

# Plot the uncertainties
plt.fill_between(
    x_m_lin, y_m_lin_upper, y_m_lin_lower,
    color='#ff7f7f', alpha=0.5, label='Model Uncertainty'
)
plt.legend()

# Add labels
plt.title(r'ln(Temperature above Environment) vs. $\sqrt{\mathrm{Fan\;Speed}}$', fontdict={'fontsize': 18})

plt.xlabel(r'$\sqrt{\mathrm{Fan\;Speed}\;(RPM)}$', fontdict={'fontsize': 14})
plt.ylabel(r'$\ln(T-T_{\infty})$', fontdict={'fontsize': 14})


# Plot the bestfit
x_b = np.linspace(x_m_lin[0], x_m_lin[-1], 100)

# Final Temperature
y_b = f(x_b, *popt)

# Plot the bestfit
plt.plot(x_b, y_b, label='Bestfit', color='#0d9dd6')
plt.legend()

bftext = "Best fit equation: $\ln(T - T_\infty) = -0.0181 \sqrt{{n_f}} + {}$".format(
    round(popt[0], 2),
)

mdtext = "Model equation: $\ln(T - T_\infty) = -(0.0158 \pm 0.0008) \sqrt{{n_f}} + (3.63 \pm 0.02)$"

plt.text(
    0.02, 0.03,
    bftext + "\n" + mdtext,
    transform=ax.transAxes,
    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round', pad=0.5, edgecolor='grey')
)

# Change axes
plt.xlim(x_m_lin[0], x_m_lin[-1])
#plt.ylim(31, 49)

plt.grid(True, color='#C5C5CA')

# Save the plot to a file
plt.savefig('images/linearized.png')

