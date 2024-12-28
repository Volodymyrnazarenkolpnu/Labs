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
        self.__name = name
        self.__garden = Garden(2, 2)
        self.__points = 0
        self.__unlocked_plants = [0]
        players.append(self)
    def plant(self, slot, plant):
        """
        plants something in the garden
        """
        garden_sizey = self.get_garden_obj().get_sizey()
        garden_sizex = self.get_garden_obj().get_sizex()
        garden_field = self.get_garden_obj().get_field()
        y = math.ceil(slot / garden_sizey) - 1
        _x = slot % garden_sizex - 1
        if _x == -1:
            _x += garden_sizex
        x = _x
        garden_field[y][x] = Plant(plant)
    def check(self):
        """
        Check garden status as player
        """
        garden = self.get_garden_obj()
        garden_last_tick = self.get_garden_obj().get_last_tick()
        if (datetime.datetime.now() - garden_last_tick).total_seconds() > 3600:
            _amount = math.floor((datetime.datetime.now() - garden_last_tick).total_seconds() / 3600)
            for _k in range(_amount):
                tick(garden)
        print(garden)
    def get_name(self):
        """
        Name getter
        """
        return self.__name
    def get_garden_obj(self):
        """
        Garden object getter
        """
        return self.__garden
    def get_points(self):
        """
        Points getter
        """
        return self.__points
    def get_unlocked_plants(self):
        """
        Unlocked plants list getter
        """
        return self.__unlocked_plants


class Garden():
    """
    Garden of individual player
    """
    def __init__(self, sizex = 2, sizey = 2):
        self.__field = []
        self.__sizex = sizex
        self.__sizey = sizey
        self.__last_tick = datetime.datetime(2024, 12, 28, 19, 18, 12)
        for _i in range(0, sizey):
            self.__field.append([])
        for _i in range(0, sizey):
            for _j in range(0, sizex):
                self.__field[_i].append("")
    def __str__(self):
        for g in self.__field:
            line = "|"
            for plt in g:
                if plt != "":
                    part = plt.__str__()
                else:
                    part = "Empty"
                line += f"{part}|"
            print(line)
        return ""
    def get_field(self):
        """
        Field matrix getter
        """
        return self.__field
    def get_sizex(self):
        """
        Horizontal size getter
        """
        return self.__sizex
    def get_sizey(self):
        """
        Vertical size getter
        """
        return self.__sizey
    def get_last_tick(self):
        """
        Last tick getter
        """
        return self.__last_tick
    def set_last_tick(self, last_tick):
        """
        Last tick setter
        """
        self.__last_tick = last_tick

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
        self.__decay_age = decay_ages.get(species)
        self.__name = names.get(species)
        self.__maturation_age = maturation_ages.get(species)
        self.__idnum = species

    def __str__(self):
        return f"{self.name}, {self.age}, {self.status}"

    def aging(self):
        """
        Maturation of plants
        """
        self_age = self.get_age()
        self_maturation_age = self.get_maturation_age()
        self_decay_age = self.get_decay_age()
        self.set_age(self_age + 1)
        self_age = self.get_age()

        if self_age >= self_maturation_age:
            self.set_status("Mature")
        if self_age >= self_decay_age:
            self.set_status("Decayed")

    def get_decay_age(self):
        """
        Decay agegetter
        """
        return self.__decay_age
    def get_name(self):
        """
        Plant name getter
        """
        return self.__name
    def get_maturation_age(self):
        """
        Maturaton age getter
        """
        return self.__maturation_age
    def get_idnum(self):
        """
        idnum getter
        """
        return self.__idnum
    def get_age(self):
        """
        Plant age getter
        """
        return self.age
    def get_status(self):
        """
        Status getter
        """
        return self.status
    def set_age(self, age):
        """
        Age setter
        """
        self.age = age
    def set_status(self, status):
        """
        Status getter
        """
        self.status = status

def tick(garden):

    """
    Tick
    """
    garden_sizey = garden.get_sizey()
    garden_sizex = garden.get_sizex()
    garden_field = garden.get_field()
    for _i in range(0, garden_sizey):
        for _j in range(0, garden_sizex):
            if garden_field[_i][_j] != "":
                garden_field[_i][_j].aging()
                if garden_field[_i][_j].get_age() >= garden_field[_i][_j].get_decay_age():
                    garden_field[_i][_j] = ""
    garden.set_last_tick(garden.get_last_tick() + datetime.timedelta(hours=1))
    mutate(garden)

def mutate(garden):
    """
    Checks each slot in a garden and applies mutations
    """
    #todo: find every one
    garden_field = garden.get_field()
    possible_mutations = []
    rownum = 0
    for yrow in garden_field:
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
                        if ny != -1 and nx != -1 and ny < len(garden_field) and nx < len(yrow):
                            if garden_field[ny][nx] != "" and garden_field[ny][nx].get_status() == "Mature":
                                _plant_idnum = garden_field[ny][nx].get_idnum()
                                if not nearby_plants.__contains__(_plant_idnum):
                                    nearby_plants.append(_plant_idnum)
                                    nearby_plants_amounts.append(1)
                                else:
                                    _idx = nearby_plants.index(_plant_idnum)
                                    nearby_plants_amounts[_idx] += 1
                for mutation in mutations:
                    satisfies = True
                    for mutation_plant in mutation.get_plant_list():
                        mutation_plantlist = mutation.get_plant_list()
                        mutation_plant_quantity = mutation.get_plant_quantity()
                        if nearby_plants.__contains__(mutation_plant):
                            _index_mutation = mutation_plantlist.index(mutation_plant)
                            _index_nearby = nearby_plants.index(mutation_plant)
                            if nearby_plants_amounts[_index_nearby] >= mutation_plant_quantity[_index_mutation]:
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
                        garden_field[rownum][slotnum] = Plant(mutation.get_outcome_plant())
            slotnum += 1
        rownum += 1

class Mutations():
    """
    For mutations, trying to make them work as objects
    """
    def __init__(self, plantlist, plantquantity, chance, outcomeplant):
        self.__plantlist = plantlist
        self.__plantquantity = plantquantity
        self.__chance = chance
        self.__outcomeplant = outcomeplant
        mutations.append(self)
    def get_plant_list(self):
        """
        List of plants needed for mutation getter
        """
        return self.__plantlist
    def get_plant_quantity(self):
        """
        Quantity of plants needed for mutation getter
        """
        return self.__plantquantity
    def get_chance(self):
        """
        Probability of mutation getter
        """
        return self.__chance
    def get_outcome_plant(self):
        """
        Outcome plant getter
        """
        return self.__outcomeplant

bluecorn = Mutations([0],[2], 10, 0)
clockberry = Mutations([0],[2], 5, 1)
player = Player("a")
player.plant(1, 0)
player.plant(4, 1)
print(player.get_garden_obj().get_last_tick())
print(player.get_garden_obj())
while True:
    inp = input()
    player.check()
    if inp == "exit":
        exit()
    if inp == "tick":
        tick(player.get_garden_obj())
