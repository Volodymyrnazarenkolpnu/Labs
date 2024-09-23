n = 1
result_fin = 0.0
result_cur = 0.0
x = 1.0
deviation = 0.00001

while x.__round__(2) < 1.5:
    result_cur = -1 ** (n + 1) * ((x - 1) ** n / n)
    result_fin += result_cur
    while result_cur.__abs__() > deviation:
        result_cur = -1 ** (n + 1) * ((x - 1) ** n / n)
        result_fin += result_cur        
        n += 1
    
    print(
        "x = " + x.__round__(5).__str__() 
        + " result = " + result_fin.__str__()
        )
    result_cur = 0.0
    result_fin = 0.0
    x += 0.05
    x = x.__round__(2)
    n = 1