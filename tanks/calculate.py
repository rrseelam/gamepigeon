import math as math


def calculate(x, y, wind):
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


print(str(calculate(406, -91, 1.1)) + " degrees")
