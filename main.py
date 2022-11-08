import json
import methods
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def F(s, x):
    try:
        dzdx = methods.fz2(x, s[0], s[1])
        dydx = methods.fy2(x, s[0], s[1])
    except ZeroDivisionError:
        dydx = s[0]
    return [dydx, dzdx]


choice = input('''
0. Тестовая задача
1. 1-ая задача
2. 2-ая задача (система)
''')

if choice == 0:
    pass
elif choice == 1:
    pass
else:
    with open("2_input_data.json") as input_f:
        d = json.load(input_f)

    x0 = d['x0']
    y0 = d['y0']
    z0 = d['z0']
    h = d['h']
    x_fin = d['x_fin']

    #график "точного" решения модуля scipy
    x = np.linspace(x0, x_fin, 100)
    s0 = [y0, z0]
    s = odeint(F, s0, x)
    plt.plot(x, s[:, 0], 'r--', label='y(x)')
    plt.plot(x, s[:, 1], 'r--', label='z(x)')
    
    rk = methods.Rk(x0, y0, z0, h, x_fin)

# rk.rk4_err_control(methods.test_fy, methods.test_fz)
# y_rk2, z_rk2 = rk.lst_y, rk.lst_z
# x = rk.lst_x

# plt.plot(x, y_rk2, 'k-v', label = 'y(x) rk2')
# plt.plot(x, z_rk2, 'k-v', label = 'z(x) rk2')

plt.legend(loc='upper left')
plt.grid()
plt.show()
