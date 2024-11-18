"""Task 2, lab7, variant 2"""
from random import randint as rint
requests = ["Task1", "Task2", "Task3"]
id_last = 3
def process(task):
    """processes task"""
    print(f"{task} is processed")

while len(requests) > 0:
    process(requests[0])
    requests.pop(0)
    _i = rint(1, 3)
    if _i == 3:
        requests.append(f"Task{id_last + 1}")
        id_last += 1
