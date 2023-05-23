import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Settings
plt.rcParams['figure.dpi'] = 300
fig, ax = plt.subplots()

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
ax.plot(x_m, y_m, label='Copper Plate Temperature Model', color='r')
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
plt.savefig('images/model.png')