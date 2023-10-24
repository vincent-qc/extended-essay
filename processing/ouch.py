import numpy as np
import math
import matplotlib.pyplot as plt
import scipy as sp



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
    fmt='.', capsize=0, elinewidth=0.5, color='#6022bd',
    label='Trial Averages',
    zorder=20
)
plt.legend()



##### Calculate the bestfit #####
def f(x, a, b, c):
    return a + (b - a) * pow(math.e, (-c * pow(x, 0.5)))
    # return a + ((b - a) * np.exp(-c * (pow(x, 0.5))))

popt, pcov = sp.optimize.curve_fit(f, x_p, y_p, [23, 60, 0.02], bounds=([20, 50, 0], [30, 70, 1]))



# Plot the bestfit
x_b= np.linspace(0, 3000, 3000)

# Final Temperature
y_b = f(x_b, *popt)

x_b_lower = x_b + (x_b * 0.10)
x_b_upper = x_b - (x_b * 0.10)

y_b_upper = f(x_b_upper, *popt) + 2
y_b_lower = f(x_b_lower, *popt) - 2

# Plot the bestfit
ax.plot(x_b, y_b, label='Best Fit', color='#63d0f7', zorder=10)
# plt.fill_between(x_b, y_b_lower, y_b_upper, alpha=0.2, color='#15c2ed', label='Bestfit Error') 
plt.legend()


##### Plot the model #####
# Fan Speed
x_m = np.linspace(0, 3000, 3000)

# Velocity, Reynolds number, Nusselt number, and heat transfer coefficient respectively
v = (93.4 * (x_m/1500) * (1/3600)) / pow(0.12, 2)
r = (v * 0.05) / (1.70 * pow(10, -5))
n = 0.664 * pow(r, (1/2)) * pow(0.7255, (1/3))
h = (n * 0.02662) / 0.05

temp = 22.2

def f(t, y, h):
    conv = ((-h) / (386 * 0.00439)) * (0.05 * 0.015) * (y - temp)
    cond = ((0.04 * (0.05 * 0.015) * (y - temp)) / (386 * 0.00439 * 0.004))
    rad =  ((0.02) / (386 * 0.00439)) * 5.67 * pow(10, -8) * (0.05 * 0.015 * 2) * (pow(y + 273, 4) - pow(temp + 273, 4))
    return (conv - rad - cond)

def f_l(t, y, x):
    conv = ((-1.13 * np.sqrt(x) * 0.02662 * 0.00078) / (386 * 0.00438 * 0.0495)) * (y - temp)
    cond = ((0.04 * (0.00078) * (y - temp)) / (386 * 0.00438 * 0.0035))
    rad =  ((0.02) / (386 * 0.00438)) * 5.67 * pow(10, -8) * (0.0016) * (pow(y + 273.15, 4) - pow(22.1 + 273.15, 4))
    return (conv - rad - cond)

def f_u(t, y, x):
    conv = ((-1.11 * np.sqrt(x) * 0.02662 * 0.00072) / (386 * 0.00440 * 0.0505)) * (y - temp)
    cond = ((0.04 * (0.00072) * (y - temp)) / (386 * 0.00440 * 0.0045))
    rad =  ((0.02) / (386 * 0.00440)) * 5.67 * pow(10, -8) * (0.0014) * (pow(y + 273.15, 4) - pow(22.3 + 273.15, 4))
    return (conv - rad - cond)

y_m = np.empty(0)
y_m_l = np.empty(0)
y_m_u = np.empty(0)

with open('data/generated.csv', 'a') as w:
    # clear the entire file first
    w.seek(0)
    w.truncate()

counter = 250
for gen in h:
    solved = sp.integrate.solve_ivp(f, (0, 60), (60,), 'RK45', args=(gen,))
    y_m = np.append(y_m, solved.y[0][-1])

    if counter % 50 == 0 and counter >= 300 and counter <= 1500:
        # write to csv file of data/generated.csv with counter,y_m[solved] and y_m rounded to 2 decimal places
        with open('data/generated.csv', 'a') as w:
            w.write('{},{}\n'.format(counter, round(y_m[-1], 2)))

    counter += 1

for x in x_m:
    lower = sp.integrate.solve_ivp(f_l, (0, 60), (59.2,), 'RK45', args=(x,))
    y_m_l = np.append(y_m_l, lower.y[0][-1])
    upper = sp.integrate.solve_ivp(f_u, (0, 60), (60.8,), 'RK45', args=(x,))
    y_m_u = np.append(y_m_u, upper.y[0][-1])


# Plot the model
ax.plot(x_m, y_m, label='Model', color='r')
plt.legend()

# Plot the model error
plt.fill_between(x_m, y_m_l, y_m_u, alpha=0.2, color='r', label='Model Uncertainty')
plt.legend()


def fit(x, a, b, c):
    return a + b * np.exp(-c * np.sqrt(x))


# scip fit line for model
popt2, pcov2 = sp.optimize.curve_fit(fit, x_m, y_m, [22.2, 40, 0.02])

# scipy fit for model upper
popt2_u, pcov2_u = sp.optimize.curve_fit(fit, x_m, y_m_u, [22.3, 40, 0.02])

# scipy fit for model lower
popt2_l, pcov2_l = sp.optimize.curve_fit(fit, x_m, y_m_l, [22.1, 40, 0.02])

# print out both upper and lower equations int he for of T = a + be^(-c*sqrt(nf))
print("Model upper equation: T = {} + {}e^{{-{} \sqrt{{n_f}}}}".format(
    round(popt2_u[0], 1),
    round(popt2_u[1], 1),
    round(popt2_u[2], 4),
))

# get b and c coefficient uncertainties using max-min/2 method
b_u = abs((popt2_u[1] - popt2_l[1]) / 2)
c_u = abs((popt2_u[2] - popt2_l[2]) / 2)

print("Model lower equation: T = {} + {}e^{{-{} \sqrt{{n_f}}}}".format(
    round(popt2_l[0], 1),
    round(popt2_l[1], 1),
    round(popt2_l[2], 4),
))

bftext = "Best fit equation: $T = 20.0 + 32.2e^{{-0.0161 \sqrt{{n_f}}}}$"

mdtext = "Model equation: $T = {} + (29 \pm 2)e^{{-({} \pm {}) \sqrt{{n_f}}}}$".format(
    round(popt2[0], 1),
    round(popt2[2], 3),
    round(c_u, 3),
)

plt.text(
    0.05, 0.15,
    bftext + "\n" + mdtext,
    transform=ax.transAxes,
    bbox=dict(facecolor='white', alpha=0.8, boxstyle='round', pad=0.5, edgecolor='grey')
)

# plot model asymptote
plt.axhline(y=22.2, color='#f763c3', linestyle='--', linewidth=0.8, label='Model Horizontal Asymptote')
plt.legend()

# plot bestfit asymptote
plt.axhline(y=20.0, color='#192fd1', linestyle='--', linewidth=0.8, label='Best Fit Horizontal Asymptote')
plt.legend()

# Add labels
plt.xlabel('Fan Speed (RPM)')
plt.ylabel('Final Temperature ($^\circ C$)')
plt.title('Final Temperature vs. Fan Speed')

# Change axes
plt.xlim(0, 3000)
plt.ylim(19, 53)

plt.grid(True, color='#C5C5CA')


# Save the plot to a file
plt.savefig('images/final.png')

x_gen = np.linspace(000, 3000, 3000)

# Reset model

v = (93.4 * (x_gen/1500) * (1/3600)) / pow(0.12, 2)
r = (v * 0.05) / (1.70 * pow(10, -5))
n = 0.664 * pow(r, (1/2)) * pow(0.7255, (1/3))
h = (n * 0.02662) / 0.05


# Clear the contents of data/generated.csv
with open('data/generated_sample.table', 'a') as w:
    w.seek(0)
    w.truncate()

for i in range(0, 3000, 20):

    # if i % 200 != 0:
    #     continue

    # 1st Col
    solved = sp.integrate.solve_ivp(f, (0, 60), (60,), 'RK45', args=(h[i],)).y[0][-1]
    solved_lower = sp.integrate.solve_ivp(f_l, (0, 60), (59.2,), 'RK45', args=(x_gen[i],)).y[0][-1]
    solved_upper = sp.integrate.solve_ivp(f_u, (0, 60), (60.8,), 'RK45', args=(x_gen[i],)).y[0][-1]
    temperature = round(solved, 1)
    uncertainty = round((solved_upper - solved_lower) / 2, 1)

    # 2nd Col
    solved_2 = sp.integrate.solve_ivp(f, (0, 60), (60,), 'RK45', args=(h[i + 1500],)).y[0][-1]
    solved_lower_2 = sp.integrate.solve_ivp(f_l, (0, 60), (59.2,), 'RK45', args=(x_gen[i],)).y[0][-1]
    solved_upper_2 = sp.integrate.solve_ivp(f_u, (0, 60), (60.8,), 'RK45', args=(x_gen[i],)).y[0][-1]
    temperature_2 = round(solved_2, 1)
    uncertainty_2 = round((solved_upper_2 - solved_lower_2) / 2, 1)

    # Open data/generated.csv in append mode
    with open('data/generated.table', 'a') as w:
        w.write('{} & {} & $\pm {}$ & {} & {} & $\pm {}$ \\\\ \n'.format(i, temperature, uncertainty, i + 1500, temperature_2, uncertainty_2))


    # # Open data/generated.csv in append mode
    # with open('data/generated_sample.table', 'a') as w:
    #     w.write('{} & {} & $\pm {}$ \\\\ \n'.format(i, temperature, uncertainty))
