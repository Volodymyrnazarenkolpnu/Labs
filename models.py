''''Models'''
#from services import garden_update_field, get_garden_from_db, tick         

class Properties():
    """
    Plant properties
    """
    def __init__(self, name, decay_age, maturation_age, points):
        self.__name = name
        self.__decay_age = decay_age
        self.__maturation_age = maturation_age
        self.__points = points
    def get_name(self):
        """
        Name getter
        """
        return self.__name
    def get_decay_age(self):
        """
        Decay age getter
        """
        return self.__decay_age
    def get_maturation_age(self):
        """
        Maturation age getter
        """
        return self.__maturation_age
    def get_points(self):
        """
        points getter
        """
        return self.__points

class Player():
    """
    contains player
    """
    def __init__(self, player_id, name, points, unlocked_plants, garden):
        self.__player_id = player_id
        self.__name = name
        self.__points = points
        self.__unlocked_plants = unlocked_plants
        self.__garden = garden
    # def plant(self, player_id, slot, plant_id):
    #     """
    #     plants something in the garden
    #     """
    #     garden = get_garden_from_db(player_id)
    #     garden_sizey = garden.get_sizey()
    #     garden_sizex = garden.get_sizex()
    #     garden_field = garden.get_field()
    #     y = math.ceil(slot / garden_sizey) - 1
    #     _x = slot % garden_sizex - 1
    #     if _x == -1:
    #         _x += garden_sizex
    #     x = _x
    #     garden_field[y][x] = plant_id
    #     garden_update_field(player_id, garden_field)
    # def check(self, user_id):
    #     """
    #     Check garden status as player
    #     """
    #     garden = Garden(user_id)
    #     garden_last_tick = self.get_garden_obj().get_last_tick()
    #     if (datetime.datetime.now() - garden_last_tick).total_seconds() > 3600:
    #         _amount = math.floor((datetime.datetime.now()-garden_last_tick).total_seconds()/3600)
    #         for _k in range(_amount):
    #             tick(garden)
    #     print(garden)
    def set_garden(self, garden):
        """
        garden setter
        """
        self.__garden = garden
    def get_player_id(self):
        """
        Id getter
        """
        return self.__player_id
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
    def __init__(self, field, sizex, sizey, last_tick):
        self.__field = field
        self.__sizex = sizex
        self.__sizey = sizey
        self.__last_tick = last_tick
    def show_garden(self):
        """shows garden"""
        current_y = 0
        current_x = 0
        plant_list = []
        for g in self.__field:
            for plt in g:
                if plt != "":
                    plant_list.append(plt.data())
                else:
                    plant_list.append("Empty")
                current_x += 1
            current_y += 1
            current_x = 0
        return plant_list
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
    def __init__(self, plant_id, decay_age, name, maturation_age, prop_id, age=0, status="Growing"):
        self.__plant_id = plant_id
        self.__decay_age = decay_age
        self.__name = name
        self.__maturation_age = maturation_age
        self.__prop_id = prop_id
        self.age = age
        self.status = status
        # self.__idnum = species
        # self.__decay_age = plants[species].decay_age
        # self.__name = plants[species].name
        # self.__maturation_age = plants[species].maturation_age
        # self.__idnum = species

    def data(self):
        """returns data about itself"""
        return (self.__plant_id, self.__name, self.age, self.status, self.__prop_id)

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
    def get_id(self):
        """
        id getter
        """
        return self.__plant_id
    def get_prop_id (self):
        """
        prop_id getter
        """
        return self.__prop_id
    def get_decay_age(self):
        """
        Decay age getter
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
    # def get_idnum(self):
    #     """
    #     idnum getter
    #     """
    #     return self.__idnum
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
class Mutations():
    """
    For mutations, trying to make them work as objects
    """
    def __init__(self, plantlist, plantquantity, chance, outcomeplant):
        self.__plantlist = plantlist
        self.__plantquantity = plantquantity
        self.__chance = chance
        self.__outcomeplant = outcomeplant
        #mutations.append(self)
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
