import math
x = 1.839
y = 3.821
z = 0.349
result = x ** (y + z) + math.sqrt(x + z ** y) - 161 * math.tan(x * z)
print(result)