import cython


cpdef list c_rk2(double y, double z, double x, double h, fy, fz):
    cdef double k1_y, k1_z, k2_y, k2_z
    cdef double res_y, res_z

    k1_y = fy(x, y, z)
    k1_z = fz(x, y, z)

    k2_y = fy(x + h, y + k1_y * h, z + k1_z * h)
    k2_z = fz(x + h, y + k1_y * h, z + k1_z * h)

    res_y = y + 0.5 * h * (k1_y + k2_y)
    res_z = z + 0.5 * h * (k1_z + k2_z)

    return [res_y, res_z]


cpdef list c_rk3(double y, double z, double x, double h, fy, fz):
    cdef long double k1_y, k1_z, k2_y, k2_z
    cdef long double k3_y, k3_z
    cdef long double res_y, res_z

    k1_y = fy(x, y, z)
    k1_z = fz(x, y, z)

    k2_y = fy(x + h*0.5, y + k1_y*h*0.5, z + k1_z*h*0.5)
    k2_z = fz(x + h*0.5, y + k1_y*h*0.5, z + k1_z*h*0.5)

    k3_y = fy(x + h, y - k1_y*h + 2*h*k2_y, z - k1_z*h + 2*h*k2_z)
    k3_z = fz(x + h, y - k1_y*h + 2*h*k2_y, z - k1_z*h + 2*h*k2_z)

    res_y = y + 1.0 / 6.0 * h * (k1_y + 4 * k2_y + k3_y)
    res_z = z + 1.0 / 6.0 * h * (k1_z + 4 * k2_z + k3_z)

    return [res_y, res_z]


cpdef list c_rk4(double y, double z, double x, double h, fy, fz):
    cdef double k1_y, k1_z, k2_y, k2_z, k3_y, k3_z, k4_y, k4_z
    cdef double res_y, res_z

    k1_y = fy(x, y, z)
    k1_z = fz(x, y, z)

    k2_y = fy(x + h*0.5, y + k1_y*h*0.5, z + k1_z*h*0.5)
    k2_z = fz(x + h*0.5, y + k1_y*h*0.5, z + k1_z*h*0.5)

    k3_y = fy(x + h*0.5, y + 0.5*h*k2_y, z + 0.5*h*k2_z)
    k3_z = fz(x + h*0.5, y + 0.5*h*k2_y, z + 0.5*h*k2_z)

    k4_y = fy(x + h, y + h*k3_y, z + h*k3_z)
    k4_z = fz(x + h, y + h*k3_y, z + h*k3_z)

    res_y = y + 1.0 / 6.0 * h * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
    res_z = z + 1.0 / 6.0 * h * (k1_z + 2 * k2_z + 2 * k3_z + k4_z)

    return [res_y, res_z]