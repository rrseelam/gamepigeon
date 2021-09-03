import cv2 as cv
import numpy as np
import math as math

# img = cv.imread(
#    r"C:\Users\olafd\Documents\Programming\gamepigeon\tanks\images\image.png")

#img = cv.resize(img, (750, 1334))


def get_wind_val(img):
    crop = crop_img(img)

    start = -1
    end = -1

    done = False
    for i in range(crop.shape[1]):
        if not done and crop[5, i, 0] > 200:
            start = i
            done = True
        elif done and crop[5, i, 0] < 125:
            end = i
            break

    mid = crop.shape[1] / 2
    start_val = (mid - start) / 12.5
    end_val = (end - mid) / 12.5
    if start_val > end_val:
        return -1 * start_val
    return end_val


def crop_img(img):

    resized_img = cv.resize(img, (750, 1334))

    dim1 = resized_img.shape[0]
    dim2 = resized_img.shape[1]

    crop_img = resized_img[int(dim1/1334 * 253): int(dim1/1334 * 254) +
                           10, int(dim2/750 * 264): int(dim2/750 * 485)]
    return crop_img


def find_red(img):
    c = 0
    x, y = 0, 0
    arr = np.array(img[500:1200, :, :])
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j, 2] < 50 and arr[i, j, 0] > 100 and arr[i, j, 1] > 100:
                c += 1
                y += i
                x += j

    return (x/c, y/c)


def find_blue(img):
    c = 0
    x, y = 0, 0
    arr = np.array(img[500:1200, :, :])
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if arr[i, j, 0] < 50 and arr[i, j, 1] > 50 and arr[i, j, 2] > 50:
                c += 1
                y += i
                x += j

    return (x/c, y/c)


def get_dist(img):
    rx, ry = find_red(img)
    bx, by = find_blue(img)
    you = 0
    if rx < bx:
        you = 'red'
    else:
        you = 'blue'

    x_dist = abs(rx - bx)

    if you == 'red':
        y_dist = ry - by
    else:
        y_dist = by - ry

    return you, x_dist, y_dist


def compute(x, y, wind):
    x = x * 406/619
    y = y * 91/144
    power = 80
    gravity = 0.07102
    velocity = 0.0714 * power
    velocity = velocity + 1.47
    wind_velocity = 0.0587 * wind

    min_diff = 1000
    angle = 0
    a = 60
    while a < 90:
        _a = math.radians(a)
        t = ((velocity * math.sin(_a)) +
             math.sqrt(math.pow(velocity * math.sin(_a), 2) - (2 * gravity * y))) / gravity
        _x = t * (velocity * math.cos(_a) + wind_velocity)
        diff = abs(_x - x)
        if diff < min_diff:
            min_diff = diff
            angle = a

        a += 1
    return angle


def set_power(wind):
    if 8 >= wind >= 6:
        power = 82
    elif wind > 8:
        power = 83
    elif 6 > wind > 1:
        power = 81
    elif wind <= -6:
        power = 78
    elif -6 <= wind <= -1:
        power = 79
    else:
        power = 80
    return power


# u, x, y = get_dist(img)
# wind = get_wind_val(img)
# result = compute(x, y, 8.7)
# power = set_power(wind)

#print(f"u:{u} x:{x} y:{y} wind:{wind} angle:{result} power:{power}")
