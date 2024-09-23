import math
from math import sin, cos
import mpmath
from mpmath import sec, cosec
x = 0.3
result = 0.0
while x <= 0.9:
    if x < 0.5:
        result = cosec(cos(x ** 2))
        print("cosec(cos(x ** 2))")
        print("x = " + x)
        print("resut = " + result)
    elif x >= 0.5 & x < 0.7:
        result = cos(sin(x))
        print("cos(sin(x))")
        print("x = " + x)
        print("resut = " + result)
    else:
        result = sin(sec(x))
        print("cos(sin(x))")
        print("x = " + x)
        print("resut = " + result)
    x = x + 0.05
