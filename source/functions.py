import math
from source.methods import json


# Тестовая задача
def test_fy(x, y, z):
    return 0.58 * y

def test_fz(x, y, z):
    return 0

# 1-ая задача
def fy1(x, y, z):
    return y/x - y ** 2

def fz1(x, y, z):
    return 0

# 2-ая задача
def fy2(x, y, z):
    return y * z + math.cos(x) / x

def fz2(x, y, z):
    return - z ** 2 + 2.5/(1 + x ** 2)


# Точное решение
def F_test(x):
    return math.exp(0.58*x)

def F_eq(s, x):
    try:
        dzdx = fz1(x, s[0], s[1])
        dydx = fy1(x, s[0], s[1])
    except ZeroDivisionError:
        dydx = 0.001
    return [dydx, dzdx]

def F_sys(s, x):
    try:
        dzdx = fz2(x, s[0], s[1])
        dydx = fy2(x, s[0], s[1])
    except ZeroDivisionError:
        dydx = s[0]
    return [dydx, dzdx]

#######

def get_lsts():
    with open("output_data.json") as f:
        d = json.load(f)
    return d['lst_x'], d['lst_y'], d['lst_z']