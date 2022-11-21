import source.methods as methods
import numpy as np
import source.functions as functions
from scipy.integrate import odeint
import matplotlib.pyplot as plt


choice = input('''
0. Тестовая задача
1. 1-ая задача
2. 2-ая задача (система)
''')

if choice == '0':
    with open("inputdata/test_input_data.json") as input_f:
        d = methods.json.load(input_f)

    x0 = d['x0']
    y0 = d['y0']
    z0 = d['z0']
    h = d['h']
    x_fin = d['x_fin']

    x = [i/100 for i in range(x0*100, x_fin*100 + 1, int(h*100))]
    y = [functions.F_test(i) for i in x]
    plt.plot(x, y, 'r--', label='y(x)')

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
        rk.rk2_const(functions.test_fy, functions.test_fz)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'k-', label = 'y(x) rk2')
    if '2' in method:
        rk.rk2_err_control(functions.test_fy, functions.test_fz)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'b-', label = 'y(x) rk2 err')
    if '3' in method:
        rk.rk3_const(functions.test_fy, functions.test_fz)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'y-', label = 'y(x) rk3')
    if '4' in method:
        rk.rk3_err_control(functions.test_fy, functions.test_fz)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'g-', label = 'y(x) rk3 err')
    if '5' in method:
        rk.rk4_const(functions.test_fy, functions.test_fz)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'r-', label = 'y(x) rk4')
    if '6' in method:
        rk.rk4_err_control(functions.test_fy, functions.test_fz)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'm-', label = 'y(x) rk4 err')
elif choice == '1':
    with open("inputdata/1_input_data.json") as input_f:
        d = methods.json.load(input_f)

    x0 = d['x0']
    y0 = d['y0']
    z0 = d['z0']
    h = d['h']
    x_fin = d['x_fin']

    choice_scipy = input('''
    Отображать график точного решения? [Y/N]
    ''')
    if choice_scipy.lower() == 'y':
        #график "точного" решения модуля scipy
        x = np.linspace(x0, x_fin, 100)
        s0 = [y0, z0]
        s = odeint(functions.F_eq, s0, x)
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
        rk.rk2_const(functions.fy1, functions.fz1)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'k-', label = 'y(x) rk2')
    if '2' in method:
        rk.rk2_err_control(functions.fy1, functions.fz1)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'b-', label = 'y(x) rk2 err')
    if '3' in method:
        rk.rk3_const(functions.fy1, functions.fz1)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'y-', label = 'y(x) rk3')
    if '4' in method:
        rk.rk3_err_control(functions.fy1, functions.fz1)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'g-', label = 'y(x) rk3 err')
    if '5' in method:
        rk.rk4_const(functions.fy1, functions.fz1)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'r-', label = 'y(x) rk4')
    if '6' in method:
        rk.rk4_err_control(functions.fy1, functions.fz1)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'm-', label = 'y(x) rk4 err')
else:
    with open("inputdata/2_input_data.json") as input_f:
        d = methods.json.load(input_f)

    x0 = d['x0']
    y0 = d['y0']
    z0 = d['z0']
    h = d['h']
    x_fin = d['x_fin']

    choice_scipy = input('''
    Отображать график точного решения? [Y/N]
    ''')
    if choice_scipy.lower() == 'y':
        # график "точного" решения модуля scipy
        x = np.linspace(x0, x_fin, 100)
        s0 = [y0, z0]
        s = odeint(functions.F_sys, s0, x)
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
        rk.rk2_const(functions.fy2, functions.fz2)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'k-', label = 'y(x) rk2')
        plt.plot(x, z, 'k-', label = 'z(x) rk2')
    if '2' in method:
        rk.rk2_err_control(functions.fy2, functions.fz2)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'b-', label = 'y(x) rk2 err')
        plt.plot(x, z, 'b-', label = 'z(x) rk2 err')
    if '3' in method:
        rk.rk3_const(functions.fy2, functions.fz2)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'y-', label = 'y(x) rk3')
        plt.plot(x, z, 'y-', label = 'z(x) rk3')
    if '4' in method:
        rk.rk3_err_control(functions.fy2, functions.fz2)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'g-', label = 'y(x) rk3 err')
        plt.plot(x, z, 'g-', label = 'z(x) rk3 err')
    if '5' in method:
        rk.rk4_const(functions.fy2, functions.fz2)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'r-', label = 'y(x) rk4')
        plt.plot(x, z, 'r-', label = 'z(x) rk4')
    if '6' in method:
        rk.rk4_err_control(functions.fy2, functions.fz2)
        x, y, z = functions.get_lsts()
        plt.plot(x, y, 'm-', label = 'y(x) rk4 err')
        plt.plot(x, z, 'm-', label = 'z(x) rk4 err')

plt.legend(loc='upper left')
plt.grid()
plt.show()
