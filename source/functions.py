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

#######

import numpy as np
from scipy.integrate import odeint
import matplotlib
import matplotlib.pyplot as plt

class Portreit:
    @classmethod
    def _ode(cls, th, x):
            z, y = th
            dthdx = [-y*z+np.cos(x), -z**2 + 2.5/(1+x**2)]
            return dthdx

    @classmethod
    def _calcODE(cls, y0, dy0, ts = 10, nt = 101):
        y0 = [y0, dy0]
        t = np.linspace(0, ts, nt)
        sol = odeint(cls._ode, y0, t)
        return sol

    @classmethod
    def _drawPhasePortrait(cls, deltaX = 1, deltaDX = 1, startX = 0,  stopX = 1, startDX = 0, stopDX = 5, ts = 10, nt = 101):
        col = (np.random.random (), np.random.random (), np.random.random ())
        for y0 in range(startX, stopX, deltaX):
                for dy0 in range(startDX, stopDX, deltaDX):
                    sol = cls._calcODE(y0, dy0, ts, nt)
                    plt.plot(sol[:, 1], sol[:, 0], c=col)

    @classmethod
    def draw(cls):
        matplotlib.use("TkAgg")
        cls._drawPhasePortrait(deltaX = 1, deltaDX = 1, startX = 0,  stopX = 1, startDX = 0, stopDX = 5, ts = 20, nt = 101)
        cls._drawPhasePortrait(deltaX = 1, deltaDX = 1, startX = -1,  stopX = 1, startDX = 0, stopDX = 1, ts = 35, nt = 101)
        plt.suptitle('Фазовый портрет')
        plt.grid()
        plt.show()