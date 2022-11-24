import json
import cmethods


class Rk:
    EPS = 0.00001
    ITERATION = 10000000

    def __init__(self, x0, y0, z0, h, x_fin):
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0
        self._h0 = h
        self._x_fin = x_fin

        self._clear()

    def _clear(self):
        self._x_lst = []
        self._y_lst = []
        self._z_lst = []

        self._x = self._x0
        self._y = self._y0
        self._z = self._z0
        self._h = self._h0

        self._div_numb = 0
        self._doubl_numb = 0
        self._max_h = self._h
        self._min_h = self._h
        self._local_err = [0]

    @property
    def lst_y(self):
        return self._y_lst

    @property
    def lst_z(self):
        return self._z_lst

    @property
    def lst_x(self):
        return self._x_lst 

    def _additional_h(self, f, fy, fz, ret=False):
        y2, z2 = f(self._y, self._z, self._x, self._h, fy, fz)

        y1, z1 = f(self._y, self._z, self._x, self._h*0.5, fy, fz)
        x1 = self._x + self._h * 0.5

        y3, z3 = f(y1, z1, x1, self._h*0.5, fy, fz)
        x3 = x1 + self._h * 0.5

        self._local_err.append(abs(y3 - y2))
        self._local_err.append(abs(z3 - z2))

        if ret:
            return y2, z2, y3, z3, x3

    def _push(self, x, y, z):
        self._x_lst.append(x)
        self._y_lst.append(y)
        self._z_lst.append(z)

    def _local_err_control(self, S_y, S_z, p, x3, y3, z3):
        # ?
        if self._h < Rk.EPS:
            self._x = x3
            self._y = y3
            self._z = z3
            self._push(self._x, self._y, self._z)
            self._min_h = self._h if self._min_h > self._h else self._min_h
            self._h = Rk.EPS
        # 
        else:    
            if abs(S_y) > Rk.EPS or abs(S_z) > Rk.EPS:
                self._h *= 0.5
                self._div_numb += 1
                self._min_h = self._h if self._min_h > self._h else self._min_h
            else:
                if abs(S_y) < (Rk.EPS / 2 ** (p + 1)):
                    self._x = x3
                    self._y = y3
                    self._z = z3
                    self._h *= 2

                    self._push(self._x, self._y, self._z)

                    self._doubl_numb += 1
                    self._max_h = self._h if self._max_h < self._h else self._max_h
                elif (Rk.EPS / 2 ** (p + 1)) <= abs(S_y) <= Rk.EPS:
                    self._x = x3
                    self._y = y3
                    self._z = z3
                    self._push(self._x, self._y, self._z)

    def _rk_const(self, fy, fz, rk):
        n = int((self._x_fin - self._x)/self._h)

        for _ in range(1, n + 1):
            # контроль итерации
            self.ITERATION -= 1
            if self.ITERATION == 0:
                break

            # Оценкка локальной погрешности
            self._additional_h(rk, fy, fz)
            
            # Вычисление y, z, x с постоянным шагом
            self._push(self._x, self._y, self._z)
            self._y, self._z = rk(self._y, self._z, self._x, self._h, fy, fz)
            self._x += self._h

        self._push(self._x, self._y, self._z)

    def _rk2(self, y, z, x, h, fy, fz):
        try:
            res_y, res_z = cmethods.c_rk2(y, z, x, h, fy, fz)
        except ZeroDivisionError:
            res_y, res_z = cmethods.c_rk2(y, z, self.EPS*1000, h, fy, fz)
        return res_y, res_z

    def rk2_const(self, fy, fz):
        self._clear()
        self._butch_scheme('rk2')

        self._rk_const(fy, fz, self._rk2)
        # Вывод данных в файл
        self._out()

    def rk2_err_control(self, fy, fz):
        self._clear()
        self._butch_scheme('rk2')

        self._push(self._x, self._y, self._z)

        while self._x < self._x_fin:
            # Контроль максимального количства итераций
            self.ITERATION -= 1
            if self.ITERATION == 0:
                break
            
            y2, z2, y3, z3, x3 = self._additional_h(self._rk2, fy, fz, ret=True)

            S_y = (y3 - y2) / 3
            S_z = (z3 - z2) / 3
            # Контроль локальной погрешности
            self._local_err_control(S_y, S_z, 2, x3, y3, z3)

        self._out()

    def _rk3(self, y, z, x, h, fy, fz):
        try:
            res_y, res_z = cmethods.c_rk3(y, z, x, h, fy, fz)
        except ZeroDivisionError:
            res_y, res_z = cmethods.c_rk3(y, z, self.EPS*1000, h, fy, fz)
        return res_y, res_z

    def rk3_const(self, fy, fz):
        self._clear()
        self._butch_scheme('rk3')

        self._rk_const(fy, fz, self._rk3)
        # Вывод данных в файл
        self._out()

    def rk3_err_control(self, fy, fz):
        self._clear()
        self._butch_scheme('rk3')

        self._push(self._x, self._y, self._z)

        while self._x < self._x_fin:
            # Контроль максимального количства итераций
            self.ITERATION -= 1
            if self.ITERATION == 0:
                break
            
            y2, z2, y3, z3, x3 = self._additional_h(self._rk3, fy, fz, ret=True)

            S_y = (y3 - y2) / 7
            S_z = (z3 - z2) / 7

            # Контроль локальной погрешности
            self._local_err_control(S_y, S_z, 3, x3, y3, z3)

        self._out()

    def _rk4(self, y, z, x, h, fy, fz):
        try:
            res_y, res_z = cmethods.c_rk4(y, z, x, h, fy, fz)
        except ZeroDivisionError:
            res_y, res_z = cmethods.c_rk4(y, z, self.EPS*1000, h, fy, fz)
        return res_y, res_z

    def rk4_const(self, fy, fz):
        self._clear()
        self._butch_scheme('rk4')

        self._rk_const(fy, fz, self._rk4)
        
        # Вывод данных в файл
        self._out()

    def rk4_err_control(self, fy, fz):
        self._clear()
        self._butch_scheme('rk4')

        self._push(self._x, self._y, self._z)

        while self._x < self._x_fin:
            # Контроль максимального количства итераций
            self.ITERATION -= 1
            if self.ITERATION == 0:
                break
            
            y2, z2, y3, z3, x3 = self._additional_h(self._rk4, fy, fz, ret=True)

            S_y = (y3 - y2) / 15
            S_z = (z3 - z2) / 15

            # Контроль локальной погрешности
            self._local_err_control(S_y, S_z, 4, x3, y3, z3)

        self._out()

    def _out(self):
        b = abs(self._x_fin - self._x_lst[-1])
        print(f"Разность правой границы и численного решения x = {b if b > Rk.EPS else 0}")
        print(f"Максимальная оценка локальной погрешности = {max(self._local_err)}")
        print(f"Число делений шага = {self._div_numb}")
        print(f"Число удвоений шага = {self._doubl_numb}")
        print(f"Максимальный шаг = {self._max_h}")
        print(f"Минимальный шаг = {self._min_h}\n")

        data = {'lst_x': self.lst_x, 'lst_y': self.lst_y, 'lst_z': self.lst_z, 
        'b': b, 'max_LEE': max(self._local_err), 'max_h': self._max_h, 'min_h': self._min_h, 
        'div_numb': self._div_numb, 'doubl_numb': self._doubl_numb}

        with open('output_data.json', 'w') as f:
            f.write(json.dumps(data))

    def _butch_scheme(self, method):
        print(f"Butcher scheme for: {method}")
        if method == 'rk2':
            print('''
            0| 0    0
            1| 1    0
             |---------
             | 1/2 1/2
            ''')
        elif method == 'rk3':
            print('''
            0  |  0   0   0
            1/2| 1/2  0   0
            1  | -1   2   0
               |------------
               | 1/6 2/3 1/6
            ''')
        else:
            print('''
            0  | 0    0   0   0
            1/2|1/2   0   0   0
            1/2| 0   1/2  0   0
            1  | 0    0   1   0
               |----------------
               | 1/6 1/3 1/3 1/6
            ''')
