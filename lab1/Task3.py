import math
from math import tan 
from math import trunc
x = 1.839
y = 3.821
z = 0.349
result = x ** (y + z) + math.sqrt(x + z ** y) - 161 * tan(x * z)
print(result)
print(result.__round__(5))