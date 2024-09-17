import math
n = 1.0
result = 1.0
x = 1.0
while x < 1.50001:
    result = -1 ** (n + 1) * ((x - 1) ** n / n)
    print("n = " + n.__round__(5).__str__() + " x = " + x.__round__(5).__str__() + " result = " + result.__round__(5).__str__())
    x += 0.05
    n += 1