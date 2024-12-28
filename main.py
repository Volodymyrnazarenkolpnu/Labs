"""
main logic script
"""
import math
import datetime
from random import randint
players = []
decay_ages = {0: 6, 1: 10}
maturation_ages = {0: 3, 1:7}
names = {0:"Blue Corn", 1:"Clockberry"}
mutations = []
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
    def check(self):
        """
        Check garden status as player
        """
        if (datetime.datetime.now() - self.garden.last_tick).total_seconds() > 3600:
            _amount = math.floor((datetime.datetime.now() - self.garden.last_tick).total_seconds() / 3600)
            for _k in range(_amount):
                tick(self)
        print(self.garden)


class Garden():
    """
    Garden of individual player
    """
    def __init__(self, sizex = 2, sizey = 2):
        self.field = []
        self.sizex = sizex
        self.sizey = sizey
        self.last_tick = datetime.datetime(2024, 12, 28, 14, 18, 12)
        for _i in range(0, sizey):
            self.field.append([])
        for _i in range(0, sizey):
            for _j in range(0, sizex):
                self.field[_i].append("")
    def __str__(self):
        for g in self.field:
            line = "|"
            for plt in g:
                if plt != "":
                    part = plt.__str__()
                else:
                    part = "Empty"
                line += f"{part}|"
            print(line)
        return ""

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
        self.idnum = species

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


def tick(plr):
    """
    Tick
    """
    for _i in range(0, plr.garden.sizey):
        for _j in range(0, plr.garden.sizex):
            if plr.garden.field[_i][_j] != "":
                plr.garden.field[_i][_j].aging()
                if plr.garden.field[_i][_j].age >= plr.garden.field[_i][_j].decay_age:
                    plr.garden.field[_i][_j] = ""
    plr.garden.last_tick += datetime.timedelta(hours=1)
    mutate(plr.garden)

def mutate(garden):
    """
    Checks each slot in a garden and applies mutations
    """
    possible_mutations = []
    rownum = 0
    for yrow in garden.field:
        slotnum = 0
        for slot in yrow:
            if slot == "":
                nearby_plants = []
                nearby_plants_amounts = []
                for sltlocal in range(1, 9):
                    if sltlocal != 5:
                        y = math.ceil(sltlocal / 3) - 2
                        _x = sltlocal % 3 - 2
                        if _x == -2:
                            _x += 3
                        x = _x
                        oy = rownum
                        ox = slotnum
                        ny = oy + y
                        nx = ox + x
                        if ny != -1 and nx != -1 and ny < len(garden.field) and nx < len(yrow):
                            if garden.field[ny][nx] != "" and garden.field[ny][nx].status == "Mature":
                                if not nearby_plants.__contains__(garden.field[ny][nx].idnum):
                                    nearby_plants.append(garden.field[ny][nx].idnum)
                                    nearby_plants_amounts.append(1)
                                else:
                                    _idx = nearby_plants.index(garden.field[ny][nx].idnum)
                                    nearby_plants_amounts[_idx] += 1
                for mutation in mutations:
                    satisfies = True
                    for mutation_plant in mutation.plantlist:
                        if nearby_plants.__contains__(mutation_plant):
                            _index_mutation = mutation.plantlist.index(mutation_plant)
                            _index_nearby = nearby_plants.index(mutation_plant)
                            if mutation.plantquantity[_index_mutation] >= nearby_plants_amounts[_index_nearby]:
                                pass
                            else:
                                satisfies = False
                        else:
                            satisfies = False
                    if satisfies is True:
                        possible_mutations.append(mutation)
                for mutation in possible_mutations:
                    _rand = randint(0, 100)
                    if _rand < mutation.chance:
                        garden.field[rownum][slotnum] = Plant(mutation.outcomeplant)
            slotnum += 1
        rownum += 1

class Mutations():
    """
    For mutations, trying to make them work as objects
    """
    def __init__(self, plantlist, plantquantity, chance, outcomeplant):
        self.plantlist = plantlist
        self.plantquantity = plantquantity
        self.chance = chance
        self.outcomeplant = outcomeplant
        mutations.append(self)

bluecorn = Mutations([0],[2], 10, 0)
clockberry = Mutations([0],[2], 5, 1)
player = Player("a")
player.plant(1, 0)
player.plant(4, 0)
print(player.garden.last_tick)
print(player.garden)
while True:
    inp = input()
    player.check()
    if inp == "exit":
        exit()
    if inp == "tick":
        tick(player)
