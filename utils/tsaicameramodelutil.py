import math
import numpy as np


class Coordinates(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z


def get_rotational_numpy(r_coords):
    r1 = math.cos(r_coords.get_y()) * math.cos(r_coords.get_z())
    r2 = math.cos(r_coords.get_z()) * math.sin(r_coords.get_x()) * math.sin(r_coords.get_y()) \
        - math.cos(r_coords.get_x()) * math.sin(r_coords.get_z())
    r3 = math.sin(r_coords.get_x()) * math.sin(r_coords.get_z()) \
        + math.cos(r_coords.get_x()) * math.cos(r_coords.get_z()) * math.sin(r_coords.get_y())
    r4 = math.cos(r_coords.get_y()) * math.sin(r_coords.get_z())
    r5 = math.sin(r_coords.get_x()) * math.sin(r_coords.get_y()) * math.sin(r_coords.get_z()) \
        + math.cos(r_coords.get_x()) * math.cos(r_coords.get_z())
    r6 = math.cos(r_coords.get_x()) * math.sin(r_coords.get_y()) * math.sin(r_coords.get_z()) \
        - math.cos(r_coords.get_z()) * math.sin(r_coords.get_x())
    r7 = -1 * math.sin(r_coords.get_y())
    r8 = math.cos(r_coords.get_y()) * math.sin(r_coords.get_x())
    r9 = math.cos(r_coords.get_x()) * math.cos(r_coords.get_y())

    return np.array([[r1, r2, r3], [r4, r5, r6], [r7, r8, r9]])


def get_coord_numpy(coords):
    return np.array([[coords.get_x()], [coords.get_y()], [coords.get_z()]])


def calc_image_coords_numpy(r_coords, w_coords, t_coords):
    r_mat = get_rotational_numpy(r_coords)
    t_mat = get_coord_numpy(t_coords)
    w_mat = get_coord_numpy(w_coords)
    r_w_mat = np.matmul(r_mat, w_mat)
    return np.add(r_w_mat, t_mat)


def calc_world_coords_numpy(i_coords, r_coords, t_coords):
    r_inv_mat = np.linalg.inv(get_rotational_numpy(r_coords))
    t_mat = get_coord_numpy(t_coords)
    i_mat = get_coord_numpy(i_coords)
    iminust_mat = np.subtract(i_mat, t_mat)
    return np.matmul(r_inv_mat, iminust_mat)


def calc_image_x_coord(xu, zi, f):
    xumulzi = xu * zi
    return xumulzi / f


def calc_image_y_coord(yu, zi, f):
    xumulzi = yu * zi
    return xumulzi / f


def calc_image_x_undistorted_from_top(xi, zi, f):
    return f*xi/zi


def calc_image_y_undistorted_from_top(yi, zi, f):
    return f*yi/zi


def calc_image_x_undistorted_from_bot(xd, yd, k):
    krsq = k * (math.pow(xd, 2) + math.pow(yd, 2))
    onepluskrsq = 1 + krsq
    return xd * onepluskrsq


def calc_image_y_undistorted_from_bot(xd, yd, k):
    krsq = k * (math.pow(xd, 2) + math.pow(yd, 2))
    onepluskrsq = 1 + krsq
    return yd * onepluskrsq


def calc_pix_x(sx, xd, dx, cx):
    sxxddivdx = sx*xd/dx
    return sxxddivdx + cx


def calc_pix_y(yd, dy, cy):
    yddivdy = yd/dy
    return yddivdy + cy


def calc_image_x_distorted(xf, sx, dx, cx):
    xfmincx = xf - cx
    xfmincxmuldx = xfmincx * dx
    return xfmincxmuldx / sx


def calc_image_y_distorted(yf, dy, cy):
    yfmincy = yf - cy
    return yfmincy * dy


class CameraParams(object):

    def __init__(self, xf, yf, zi, sx, cx, cy, k, f, rx, ry, rz, tx, ty, tz, dx, dy):
        self.xf = xf
        self.yf = yf
        self.zi = zi
        self.sx = sx
        self.cx = cx
        self.cy = cy
        self.k = k
        self.f = f
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.dx = dx
        self.dy = dy

    def get_xf(self):
        return self.xf

    def get_yf(self):
        return self.yf

    def get_zi(self):
        return self.zi

    def get_sx(self):
        return self.sx

    def get_cx(self):
        return self.cx

    def get_cy(self):
        return self.cy

    def get_k(self):
        return self.k

    def get_f(self):
        return self.f

    def get_rx(self):
        return self.rx

    def get_ry(self):
        return self.ry

    def get_rz(self):
        return self.rz

    def get_tx(self):
        return self.tx

    def get_ty(self):
        return self.ty

    def get_tz(self):
        return self.tz

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy


xf01 = 367.5
yf01 = 130.5
zi01 = 75 #height
sx0 = 1
cx0 = 1036.6183693
cy0 = 59.419916551
k0 = -0.0028341198763
f0 = 3.8421554336
rx0 = -1.8816423818
ry0 = -0.15377351681
rz0 = 0.030518220098
tx0 = 2183.2767031
ty0 = 3450.6736437
tz0 = 5273.9192961
dx0 = 0.00375
dy0 = 0.00375

cam0 = CameraParams(xf01, yf01, zi01, sx0, cx0, cy0, k0, f0, rx0, ry0, rz0, tx0, ty0, tz0, dx0, dy0)

xf11 = 183.5
yf11 = 125.5
zi11 = 155
sx1 = 1
cx1 = 904.14676533
cy1 = 591.71430888
k1 = -0.000420039049
f1 = 3.802407252
rx1 = 1.0797724727
ry1 = 0.63145609215
rz1 = 2.8245123028
tx1 = -616.45840896
ty1 = 93.628248549
tz1 = 4642.8884327
dx1 = 0.00375
dy1 = 0.00375

cam1 = CameraParams(xf11, yf11, zi11, sx1, cx1, cy1, k1, f1, rx1, ry1, rz1, tx1, ty1, tz1, dx1, dy1)

# Get world coordinate from cam 0
xd0 = calc_image_x_distorted(cam0.get_xf(), cam0.get_sx(), cam0.get_dx(), cam0.get_cx())
print('cam0 || xd0: ' + str(xd0))
yd0 = calc_image_y_distorted(cam0.get_yf(), cam0.get_dy(), cam0.get_cy())
print('cam0 || yd0: ' + str(yd0))
xu0 = calc_image_x_undistorted_from_bot(xd0, yd0, cam0.get_k())
print('cam0 || xu0: ' + str(xu0))
yu0 = calc_image_y_undistorted_from_bot(xd0, yd0, cam0.get_k())
print('cam0 || yu0: ' + str(yu0))
xi0 = calc_image_x_coord(xu0, cam0.get_zi(), cam0.get_f())
print('cam0 || xi0: ' + str(xi0))
yi0 = calc_image_y_coord(yu0, cam0.get_zi(), cam0.get_f())
print('cam0 || yi0: ' + str(yi0))
i_coords0 = Coordinates(xi0, yi0, cam0.get_zi())
r_coords0 = Coordinates(cam0.get_rx(), cam0.get_ry(), cam0.get_rz())
t_coords0 = Coordinates(cam0.get_tx(), cam0.get_ty(), cam0.get_tz())

world_coords_numpy = calc_world_coords_numpy(i_coords0, r_coords0, t_coords0)
print('world coords: ' + str(world_coords_numpy))
world_coords = Coordinates(world_coords_numpy[0, 0], world_coords_numpy[1, 0], world_coords_numpy[2, 0])


# Calc xu amd yu using cam0 world coord and cam1 params
r_coords1 = Coordinates(cam1.get_rx(), cam1.get_ry(), cam1.get_rz())
t_coords1 = Coordinates(cam1.get_tx(), cam1.get_ty(), cam1.get_tz())
image_coords_numpy1 = calc_image_coords_numpy(r_coords1, world_coords, t_coords1)
xu1_top = calc_image_x_undistorted_from_top(image_coords_numpy1[0, 0], image_coords_numpy1[2, 0], cam1.get_f())
print('cam1 top || xu1: ' + str(xu1_top))
yu1_top = calc_image_y_undistorted_from_top(image_coords_numpy1[1, 0], image_coords_numpy1[2, 0], cam1.get_f())
print('cam1 top || yu1: ' + str(yu1_top))

# Calc xu and yu using cam1 params
xd1 = calc_image_x_distorted(cam1.get_xf(), cam1.get_sx(), cam1.get_dx(), cam1.get_cx())
print('cam1 || xd1: ' + str(xd1))
yd1 = calc_image_y_distorted(cam1.get_yf(), cam1.get_dy(), cam1.get_cy())
print('cam1 || yd1: ' + str(yd1))
xu1_bot = calc_image_x_undistorted_from_bot(xd1, yd1, cam1.get_k())
print('cam1 bottom || xu1: ' + str(xu1_bot))
yu1_bot = calc_image_y_undistorted_from_bot(xd1, yd1, cam1.get_k())
print('cam1 bottom || yu1: ' + str(yu1_bot))

# Compare both xu calcs
print('cam1 xd match results: ' + str(xu1_top == xu1_bot))

print('cam1 yd match results: ' + str(yu1_top == yu1_bot))