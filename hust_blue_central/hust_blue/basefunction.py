PI = 3.14159265358979323846264338327950288419717
RAD_TO_DEG = 57.29577951308232
DEG_TO_RAD = 0.01745329251994329576923690768489

import math
import numpy as np


def matrix_multiply_3x3( a, b):
    c = np.zeros((3,3))
    c[0][0] = a[0][0] * b[0][0] + a[0][1] * b[1][0] + a[0][2] * b[2][0];
    c[0][1] = a[0][0] * b[0][1] + a[0][1] * b[1][1] + a[0][2] * b[2][1];
    c[0][2] = a[0][0] * b[0][2] + a[0][1] * b[1][2] + a[0][2] * b[2][2];
    c[1][0] = a[1][0] * b[0][0] + a[1][1] * b[1][0] + a[1][2] * b[2][0];
    c[1][1] = a[1][0] * b[0][1] + a[1][1] * b[1][1] + a[1][2] * b[2][1];
    c[1][2] = a[1][0] * b[0][2] + a[1][1] * b[1][2] + a[1][2] * b[2][2];
    c[2][0] = a[2][0] * b[0][0] + a[2][1] * b[1][0] + a[2][2] * b[2][0];
    c[2][1] = a[2][0] * b[0][1] + a[2][1] * b[1][1] + a[2][2] * b[2][1];
    c[2][2] = a[2][0] * b[0][2] + a[2][1] * b[1][2] + a[2][2] * b[2][2];
    return c

def matrix_multiply_3x1( a, b):
    c0 = a[0][0] * b[0] + a[0][1] * b[1] + a[0][2] * b[2]
    c1 = a[1][0] * b[0] + a[1][1] * b[1] + a[1][2] * b[2]
    c2 = a[2][0] * b[0] + a[2][1] * b[1] + a[2][2] * b[2]
    return c0,c1,c2


def transpose_matrix_3x3(ipt):
    opt = np.zeros((3,3))
    opt[0][0] = ipt[0][0]
    opt[0][1] = ipt[1][0]
    opt[0][2] = ipt[2][0]
    opt[1][0] = ipt[0][1]
    opt[1][1] = ipt[1][1]
    opt[1][2] = ipt[2][1]
    opt[2][0] = ipt[0][2]
    opt[2][1] = ipt[1][2]
    opt[2][2] = ipt[2][2]
    return opt

def rot( angle, axis):
    c_ang = np.cos(angle * DEG_TO_RAD)
    s_ang = np.sin(angle * DEG_TO_RAD)
    r = np.zeros((3,3))
    if axis == 1:
        r[0][0] = 1
        r[0][1] = 0
        r[0][2] = 0
        r[1][0] = 0
        r[2][0] = 0
        r[1][1] = c_ang
        r[2][2] = c_ang
        r[1][2] = s_ang
        r[2][1] = -s_ang
    elif axis == 2:
        r[0][1] = 0
        r[1][0] = 0
        r[1][1] = 1
        r[1][2] = 0
        r[2][1] = 0
        r[0][0] = c_ang
        r[2][2] = c_ang
        r[0][2] = -s_ang
        r[2][0] = s_ang
    elif axis == 3:
        r[2][0] = 0
        r[2][1] = 0
        r[2][2] = 1
        r[0][2] = 0
        r[1][2] = 0
        r[0][0] = c_ang
        r[1][1] = c_ang
        r[1][0] = -s_ang
        r[0][1] = s_ang

    return r


def rot3d( ref_lat, ref_lon):

    r1 = rot( 90 + ref_lon, 3)
    r2 = rot( 90 - ref_lat, 1)
    r = matrix_multiply_3x3(r2, r1)
    return r


def straight_distance(lon1, lat1, lon2, lat2):
    lon1 *= DEG_TO_RAD
    lat1 *= DEG_TO_RAD
    lon2 *= DEG_TO_RAD
    lat2 *= DEG_TO_RAD
    val_a = lat1 - lat2
    val_b = lon1 - lon2
    return 2 * np.arcsin(np.sqrt
                         (np.sin(val_a / 2) * np.sin(val_a / 2) + np.cos(lat1) * np.cos(lat2) * np.sin(
                             val_b / 2) * np.sin
                          (val_b / 2))) * 6378137


def straight_distance_alt(lon1, lat1, alt1, lon2, lat2, alt2):
    lon1 *= DEG_TO_RAD
    lat1 *= DEG_TO_RAD
    lon2 *= DEG_TO_RAD
    lat2 *= DEG_TO_RAD
    a = lat1 - lat2
    b = lon1 - lon2
    c = 6378137 + min(alt1, alt2)
    d = 2 * np.arcsin \
        (np.sqrt(np.sin(a / 2) * np.sin(a / 2) + np.cos(lat1) * np.cos(lat2) * np.sin(b / 2) * np.sin(b / 2))) * c
    return np.sqrt(abs(d * d - np.power(alt1 - alt2, 2)))


def xyz_to_lla(xyz):
    lla = np.zeros(3)
    flattening = 1.0 / 298.257223563
    nva_e2 = (2.0 - flattening) * flattening
    if (xyz[0] == 0.0) & (xyz[1] == 0.0):
        lla[1] = 0.0
    else:
        lla[1] = np.arctan2(xyz[1], xyz[0]) * RAD_TO_DEG

    if (xyz[0] == 0.0) & (xyz[1] == 0.0) & (xyz[2] == 0.0):
        return []
    else :
        rho_sqrt = xyz[0] * xyz[0] + xyz[1] * xyz[1]
        rho = np.sqrt(rho_sqrt)
        temp_lat = np.arctan2(xyz[2], rho)
        temp_alt = np.sqrt(rho_sqrt + xyz[2] * xyz[2]) - 6378137.0
        rho_error = 1000.0
        z_error = 1000.0
        temp_iter = 0
        while (abs(rho_error) > 1e-6) | (abs(z_error) > 1e-6):
            s_lat = np.sin(temp_lat)
            c_lat = np.cos(temp_lat)
            q = 1.0 - nva_e2 * s_lat*s_lat
            r_n = 6378137.0 / np.sqrt(q)
            dr_dl = r_n * nva_e2 * s_lat * c_lat / q
            rho_error = (r_n + temp_alt) * c_lat - rho
            z_error = (r_n * (1.0 - nva_e2) + temp_alt) * s_lat - xyz[2]
            aa = dr_dl * c_lat - (r_n + temp_alt) * s_lat
            bb = c_lat
            cc = (1.0 - nva_e2)*(dr_dl * s_lat + r_n * c_lat)
            dd = s_lat
            inv_det = 1.0 / (aa * dd - bb * cc)
            temp_lat = temp_lat - inv_det * (+dd * rho_error - bb * z_error)
            temp_alt = temp_alt - inv_det * (-cc * rho_error + aa * z_error)
            temp_iter += 1
            if temp_iter > 20:
                return []

        lla[0] = temp_lat * RAD_TO_DEG
        lla[2] = temp_alt
    return lla

def lla_to_xyz(lla):
    xyz = np.zeros(3)
    if (lla[0] < -90.0) or (lla[0] > +90.0) or (lla[1] < -180.0) or (lla[1] > +360.0) :
        return []
    A_EARTH = 6378137.0
    flattening = 1.0 / 298.257223563
    NAV_E2 = (2.0 - flattening) * flattening
    deg2rad = np.pi / 180.0

    slat = np.sin(lla[0] * deg2rad)

    clat = np.cos(lla[0] * deg2rad)

    r_n = A_EARTH / np.sqrt(1.0 - NAV_E2 * slat * slat)
    xyz[0] = (r_n + lla[2]) * clat * np.cos(lla[1] * deg2rad)
    xyz[1] = (r_n + lla[2]) * clat * np.sin(lla[1] * deg2rad)
    xyz[2] = (r_n * (1.0 - NAV_E2) + lla[2]) * slat
    return xyz

def xyz_to_enu(xyz, ref_lla):
    diff_xyz = [0, 0,  0]
    ref_xyz = lla_to_xyz(ref_lla)
    if len(xyz) == 0:
        return []
    diff_xyz[0] = xyz[0] - ref_xyz[0]
    diff_xyz[1] = xyz[1] - ref_xyz[1]
    diff_xyz[2] = xyz[2] - ref_xyz[2]
    r = rot3d(ref_lla[0], ref_lla[1])
    enu = matrix_multiply_3x1(r, diff_xyz)

    return enu


def lla_to_enu(ref_lla, lla):
    xyz = lla_to_xyz(lla)
    if len(xyz) == 0:
        return []
    enu =xyz_to_enu(xyz, ref_lla)
    if len(enu) == 0:
        return []

    return enu


def lla_to_ned(r_lon, r_lat, r_alt, lon, lat, alt):
    lla = [lat, lon, alt]
    ref_lla = [r_lat, r_lon, r_alt]
    enu = lla_to_enu(ref_lla, lla)
    e = enu[0]
    n = enu[1]
    d = -enu[2]
    return n,e,d


def enu_to_lla(ref_lla, enu):
    xyz = np.zeros(3)
    ref_xyz = lla_to_xyz(ref_lla)
    if len(ref_xyz) == 0:
        print("reflla", ref_lla[0],ref_lla[1],ref_lla[2])
        print("enu",enu[0],enu[1],enu[2])
        print("xyz 0 ")
        return []
    r = rot3d(ref_lla[0], ref_lla[1])

    rt = transpose_matrix_3x3(r)
    diff_xyz = matrix_multiply_3x1(rt, enu)
    xyz[0] = diff_xyz[0] + ref_xyz[0]
    xyz[1] = diff_xyz[1] + ref_xyz[1]
    xyz[2] = diff_xyz[2] + ref_xyz[2]
    lla = xyz_to_lla(xyz)
    if len(lla) == 0:
        print("lla0")
        return []
    return lla


def ned_to_lla(r_lon, r_lat, r_alt, n, e, d):
    ref_lla = [r_lat, r_lon, r_alt]
    enu = [e, n, d * -1]
    lat, lon, alt = enu_to_lla(ref_lla, enu)
    return lon, lat, alt