import numpy as np
import math
import matplotlib.pyplot as plt

TRIALS = 3

##### Read and Plot the data points #####
for i in range(1, TRIALS + 1):

    # Read the data
    data = np.genfromtxt('data/trial_{}.csv'.format(i), delimiter=',')
    x = data[:, 0]
    y = data[:, 1]

    # Plot the data
    plt.errorbar(
        x, y, xerr=x*0.10, yerr=2,
        fmt='.', capsize=3, capthick=0.5, elinewidth=0.5,
        label='Trial {}'.format(i)
    )
    plt.legend()


##### Plot the model #####
# Fan Speed
x_m = np.linspace(400, 1600, 1200)

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

# Add labels
plt.xlabel('Fan Speed (RPM)')
plt.ylabel('Final Temperature ($^\circ C$)')
plt.title('Final Temperature vs. Fan Speed')


# Save the plot to a file
plt.savefig('images/points.png')