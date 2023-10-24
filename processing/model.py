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

##### Plot the model #####
# Fan Speed
x_m = np.linspace(350, 1700, 1200)

# Velocity, Reynolds number, Nusselt number, and heat transfer coefficient respectively
v = (93.4 * (x_m/1500) * (1/3600)) / pow(0.12, 2)
r = (v * 0.05) / (1.70 * pow(10, -5))
n = 0.664 * pow(r, (1/2)) * pow(0.724, (1/3))
h = (n * 0.0266) / 0.05


y_m = 22.2 + (37.8) * np.exp(-0.0158 * pow(x_m, 0.5))

# Plot the model
ax.plot(x_m, y_m, label='Copper Plate Temperature Model', color='r')
plt.legend()


y_m_upper = 22.3 + (38.7) * np.exp(-0.0150 * pow(x_m, 0.5))
y_m_lower = 22.1 + (36.9) * np.exp(-0.0166 * pow(x_m, 0.5))
ax.fill_between(x_m, y_m_lower, y_m_upper, alpha=0.2, color='r', label='Model Uncertainty')
plt.legend()

# Add labels
plt.xlabel('Fan Speed (RPM)', labelpad=6, fontsize=12)
plt.ylabel('Final Temperature ($^\circ C$)', labelpad=6, fontsize=12)
plt.title('Final Temperature vs. Fan Speed', fontsize=16, pad=10)

# Change axes


plt.grid(True, color='#C5C5CA')

plt.xlim(350, 1700)

# Save the plot to a file
plt.savefig('images/model.png')