
"""
main logic script
"""
import math
import datetime
players = []
decay_ages = {0: 6}
maturation_ages = {0: 3}
names = {0:"Blue Corn"}
class Player():
    """
    contains player
    """
    def __init__(self, name):
        self.name = name
        self.garden = Garden(2, 2)
        self.points = 0
        self.unlocked_plants = [0]
        players.append(self)
    def plant(self, slot, plant):
        """
        plants something in the garden
        """
        y = math.ceil(slot / self.garden.sizey) - 1
        _x = slot % self.garden.sizex - 1
        if _x == -1:
            _x += self.garden.sizex
        x = _x
        self.garden.field[y][x] = Plant(plant)

class Garden():
    """
    Garden of individual player
    """
    def __init__(self, sizex = 2, sizey = 2):
        self.field = []
        self.sizex = sizex
        self.sizey = sizey
        self.last_tick = datetime.datetime(2024, 12, 26, 18, 18, 12)
        for _i in range(0, sizey):
            self.field.append([])
        for _i in range(0, sizey):
            for _j in range(0, sizex):
                self.field[_i].append("")

class Plant():
    """
    Main plant class
    """
    age = 0
    status = "Growing"
    maturation_age = 1
    decay_age = 2
    name = "Plant"
    def __init__(self, species):
        self.decay_age = decay_ages.get(species)
        self.name = names.get(species)
        self.maturation_age = maturation_ages.get(species)

    def __str__(self):
        return f"{self.name}, {self.age}, {self.status}"

    def aging(self):
        """
        Maturation of plants
        """
        self.age += 1
        if self.age >= self.maturation_age:
            self.status = "Mature"
        if self.age >= self.decay_age:
            self.status = "Decayed"


def tick():
    """
    Tick
    """
    for _i in range(0, plr.garden.sizey):
        for _j in range(0, plr.garden.sizex):
            if plr.garden.field[_i][_j] != "":
                plr.garden.field[_i][_j].aging()
                if plr.garden.field[_i][_j].age >= plr.garden.field[_i][_j].decay_age:
                    plr.garden.field[_i][_j] = ""
    plr.garden.last_tick = datetime.datetime.now()

player = Player("a")
player.plant(1, 0)
print(player.garden.field[0][0])
print(player.garden.last_tick)
while True:
    inp = input()
    
    for plr in players:
        if (datetime.datetime.now() - plr.garden.last_tick).total_seconds() > 3600:
            _amount = math.floor((datetime.datetime.now() - plr.garden.last_tick).total_seconds() / 3600)
            for i in range(0, _amount):
                tick()
                plr.garden.last_tick += datetime.timedelta(hours=1)
        print(plr.garden.field[0][0])
    if inp == "exit":
        exit()
