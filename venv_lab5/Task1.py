from enum import Enum
from math import sqrt
from random import randint as rint
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other): 
            return self.x == other.x and self.y == other.y

class Polygon(Point):
    def __init__(self, *args):
        self.points = []
        for pt in args:
            self.points.append(pt)
    
    def CalculateLongestDiagonal(self):
        _length = 0
        for pt in self.points:
            diag = 0
            for pt2 in self.points:
                diag = sqrt((pt2.x - pt.x) ** 2 + (pt2.y - pt.y) ** 2)
                if diag > _length:
                    _length = diag
        return _length
    
    def SortPointsByX(self):
        is_sorted = False
        while is_sorted == False:
            for i in range(0, len(self.points)):
                if i == len(self.points):
                    is_sorted = True
                if self.points[i].x > self.points[i + 1].x:
                    self.points[i], self.points[i + 1] = self.points[i + 1], self.points[i]
                    break
    
    def SortPointsByY(self):
        is_sorted = False
        while is_sorted == False:
            for i in range(0, len(self.points)):
                if i == len(self.points):
                    is_sorted = True
                if self.points[i].y > self.points[i + 1].y:
                    self.points[i], self.points[i + 1] = self.points[i + 1], self.points[i]
                    break
p1 = Point(1, 1)
p2 = Point(1, -1)
p3 = Point(-1, -1)
p4 = Point(-1, 1)
square = Polygon(p1, p2, p3, p4)
p5 = Point(2, 4)
p6 = Point(5, -8)
p7 = Point(-3, -1)
triangle = Polygon(p5, p6, p7)
triangle2 = Polygon(p1, p6, p7)
print(square.CalculateLongestDiagonal())

def drawgraph(*args):
    #initialising
    space = []
    for i in range(31):
        space.append([])
    for i in range(0, 30):
        for j in range(0, 30):
            space[i].insert(j, "  ")
    #drawing grahp axis
    for i in range(0, 30):
        space[i][15] = "- "
    for i in range(0, 30):
        space[15][i] = "| "
    space[15][15] = "+ "
    #drawing graph numbers
    for i in range(0, 30):
        space[0][i] = (str(-i + 15) + " " * (4 - len(str(-i + 15))))
    upper_numbers_sign_line = "    "
    for i in range(1, 30):
        if str(i - 15)[0] == "-":
            upper_numbers_sign_line += "- "
        else:
            upper_numbers_sign_line += "  "
    upper_numbers_first_line = "    "
    for i in range(1, 30):
        if str(i - 15)[0] == "-":
            upper_numbers_first_line += (str(i - 15)[1] + " ")
        else:
            upper_numbers_first_line += (str(i - 15)[0] + " ")
    upper_numbers_second_line = "    "
    for i in range(1, 30):
        if (str(i - 15))[0] == "-" and len(str(i - 15)) == 3:
            upper_numbers_second_line += (str(i - 15)[2] + " ")
        elif (str(i - 15))[0] != "-" and len(str(i - 15)) == 2:
            upper_numbers_second_line += (str(i - 15)[1] + " ")
        else:
            upper_numbers_second_line += "  "
    print(upper_numbers_sign_line)
    print(upper_numbers_first_line)
    print(upper_numbers_second_line)
    #drawing points
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    drawn_points = []
    statements = []
    for polyg in args:
        letter = alphabet[rint(0, 23)]
        alphabet.remove(letter)
        for pt in polyg.points:
            for drpt in drawn_points:
                if pt.__eq__(drpt):
                    statements.append(f"{pt.x}, {pt.y} is a part of {space[pt.x + 15][-pt.y + 15]} and {letter}")
            space[(pt.x + 15)][-(pt.y + 15)] = (letter + " ")
            drawn_points.append(pt)
    #printer
    for i in range(0, 30):
        line = ""
        for j in range(0, 30):
            line += f"{space[j][i]}"
        print(line)
    for statement in statements:
        print(statement)
drawgraph(square, triangle, triangle2)