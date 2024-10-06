from random import randint as rint

NumList = [rint(0, 30) for i in range(30)]
max_res = 1
cur_res = 0
_current = 0
while (_current + 1) < len(NumList):
    cur_res =  NumList[_current] * NumList[(_current + 1)]
    if cur_res > max_res:
        max_res = cur_res
    _current += 1
print(f"Max result: {max_res}")