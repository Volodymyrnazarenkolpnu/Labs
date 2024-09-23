n = 1
result = 1.0
x = 1.0
while x < 1.50001:
    while result.__abs__() > 0.00001:
        result = -1 ** (n + 1) * ((x - 1) ** n / n)
        print("n = " + n.__str__() + " x = " + x.__round__(5).__str__() + " result = " + result.__str__())
        n += 1
    result = 1.0
    x += 0.05
    n = 1