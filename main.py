import methods
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def F_eq(s, x):
    try:
        dzdx = methods.fz1(x, s[0], s[1])
        dydx = methods.fy1(x, s[0], s[1])
    except ZeroDivisionError:
        dydx = s[0]
    return [dydx, dzdx]

def F_sys(s, x):
    try:
        dzdx = methods.fz2(x, s[0], s[1])
        dydx = methods.fy2(x, s[0], s[1])
    except ZeroDivisionError:
        dydx = s[0]
    return [dydx, dzdx]

def get_lsts():
    with open("output_data.json") as f:
        d = methods.json.load(f)
    return d['lst_x'], d['lst_y'], d['lst_z']


choice = input('''
0. Тестовая задача
1. 1-ая задача
2. 2-ая задача (система)
''')

if choice == '0':
    pass
elif choice == '1':
    with open("1_input_data.json") as input_f:
        d = methods.json.load(input_f)

    x0 = d['x0']
    y0 = d['y0']
    z0 = d['z0']
    h = d['h']
    x_fin = d['x_fin']

    #график "точного" решения модуля scipy
    x = np.linspace(x0, x_fin, 100)
    s0 = [y0, z0]
    s = odeint(F_eq, s0, x)
    plt.plot(x, s[:, 0], 'r--', label='y(x)')

    rk = methods.Rk(x0, y0, z0, h, x_fin)
    method = input('''
    Введите последовательность цифер для отображения методов:
    1. Рунге-Кутта 2 порядка с постоянным шагом
    2. Рунге-Кутта 2 порядка с переменным шагом
    3. Рунге-Кутта 3 порядка с постоянным шагом
    4. Рунге-Кутта 3 порядка с переменным шагом
    5. Рунге-Кутта 4 порядка с постоянным шагом
    6. Рунге-Кутта 4 порядка с переменным шагом
    ''')

    if '1' in method:
        rk.rk2_const(methods.fy1, methods.fz1)
        x, y, z = get_lsts()
        plt.plot(x, y, 'k-v', label = 'y(x) rk2')
    if '2' in method:
        rk.rk2_err_control(methods.fy1, methods.fz1)
        x, y, z = get_lsts()
        plt.plot(x, y, 'b-4', label = 'y(x) rk2 err')
    if '3' in method:
        rk.rk3_const(methods.fy1, methods.fz1)
        x, y, z = get_lsts()
        plt.plot(x, y, 'y-x', label = 'y(x) rk3')
    if '4' in method:
        rk.rk3_err_control(methods.fy1, methods.fz1)
        x, y, z = get_lsts()
        plt.plot(x, y, 'g-s', label = 'y(x) rk3 err')
    if '5' in method:
        rk.rk4_const(methods.fy1, methods.fz1)
        x, y, z = get_lsts()
        plt.plot(x, y, 'r-3', label = 'y(x) rk4')
    if '6' in method:
        rk.rk4_err_control(methods.fy1, methods.fz1)
        x, y, z = get_lsts()
        plt.plot(x, y, 'm-p', label = 'y(x) rk4 err')
else:
    with open("2_input_data.json") as input_f:
        d = methods.json.load(input_f)

    x0 = d['x0']
    y0 = d['y0']
    z0 = d['z0']
    h = d['h']
    x_fin = d['x_fin']

    #график "точного" решения модуля scipy
    x = np.linspace(x0, x_fin, 100)
    s0 = [y0, z0]
    s = odeint(F_sys, s0, x)
    plt.plot(x, s[:, 0], 'r--', label='y(x)')
    plt.plot(x, s[:, 1], 'r--', label='z(x)')

    rk = methods.Rk(x0, y0, z0, h, x_fin)
    
    method = input('''
    Введите последовательность цифер для отображения методов:
    1. Рунге-Кутта 2 порядка с постоянным шагом
    2. Рунге-Кутта 2 порядка с переменным шагом
    3. Рунге-Кутта 3 порядка с постоянным шагом
    4. Рунге-Кутта 3 порядка с переменным шагом
    5. Рунге-Кутта 4 порядка с постоянным шагом
    6. Рунге-Кутта 4 порядка с переменным шагом
    ''')

    if '1' in method:
        rk.rk2_const(methods.fy2, methods.fz2)
        x, y, z = get_lsts()
        plt.plot(x, y, 'k-v', label = 'y(x) rk2')
        plt.plot(x, z, 'k-v', label = 'z(x) rk2')
    if '2' in method:
        rk.rk2_err_control(methods.fy2, methods.fz2)
        x, y, z = get_lsts()
        plt.plot(x, y, 'b-4', label = 'y(x) rk2 err')
        plt.plot(x, z, 'b-4', label = 'z(x) rk2 err')
    if '3' in method:
        rk.rk3_const(methods.fy2, methods.fz2)
        x, y, z = get_lsts()
        plt.plot(x, y, 'y-x', label = 'y(x) rk3')
        plt.plot(x, z, 'y-x', label = 'z(x) rk3')
    if '4' in method:
        rk.rk3_err_control(methods.fy2, methods.fz2)
        x, y, z = get_lsts()
        plt.plot(x, y, 'g-s', label = 'y(x) rk3 err')
        plt.plot(x, z, 'g-s', label = 'z(x) rk3 err')
    if '5' in method:
        rk.rk4_const(methods.fy2, methods.fz2)
        x, y, z = get_lsts()
        plt.plot(x, y, 'r-3', label = 'y(x) rk4')
        plt.plot(x, z, 'r-3', label = 'z(x) rk4')
    if '6' in method:
        rk.rk4_err_control(methods.fy2, methods.fz2)
        x, y, z = get_lsts()
        plt.plot(x, y, 'm-p', label = 'y(x) rk4 err')
        plt.plot(x, z, 'm-p', label = 'z(x) rk4 err')

plt.legend(loc='upper left')
plt.grid()
plt.show()
