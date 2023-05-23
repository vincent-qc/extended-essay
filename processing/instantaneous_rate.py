import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Settings
plt.rcParams['figure.dpi'] = 300
fig, ax = plt.subplots()

def f(x, a, b):
    return -a * pow(math.e, (-b * pow(x, 0.5))) * pow(x, -0.5)

# Bestfit and model
x_b = np.linspace(350, 1750, 1400)
x_m = np.linspace(350, 1750, 1400)

y_b = f(x_b, 0.423, 0.0221)
y_m = f(x_m, 0.496, 0.0268)

# Plot the model and bestfit
ax.plot(x_m, y_m, label='Model', color='#ed4f37')
ax.plot(x_b, y_b, label='Best Fit', color='#71f0e7')
plt.legend()

# Add labels
plt.xlabel('Fan Speed (RPM)')
plt.ylabel('Instantaneous Rate of Cooling ($^\circ C$)')
plt.title('Instantaneous Rate of Cooling vs. Fan Speed')

# Change axes
plt.xlim(350, 1750)
plt.ylim(-0.02, 0.005)

plt.grid(True, color='#C5C5CA')


# Save the plot to a file
plt.savefig('images/instantaneous.png')