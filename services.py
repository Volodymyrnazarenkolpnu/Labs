'''
Services of project. We used it when we need to interact with db, or do massive logic
'''
import datetime
import json
import math
import io
from random import randint
from PIL import Image, ImageDraw
from db import (create_new_plant, add_points_to_player, remove_garden_by_id,
remove_player_by_id, create_player_and_their_garden,
delete_plant_by_id, get_garden_by_player_id, get_plant_by_id,
get_plant_props_by_id, get_player_by_id, get_all_mutations,
update_field, update_garden_last_tick, update_plant,
update_unlocked_plants)
from models import Garden, Mutations, Plant, Player, Properties
from setting import BORDER_WIDTH, CELL_WIDTH

class PlayerService:
    '''Player service'''
    @staticmethod
    def get_player(player_id):
        ''''Get or create new player from db. Also it updates name if user exists'''
        player = get_player_by_id(player_id)
        exist_status = True
        if player is None:
            exist_status = False
        name_from_player = player["username"]
        points = player["points"]
        unlocked_plants = json.loads(player["unlocked_plants"])
        garden = GardenService.get_garden_from_db(player_id)
        return [Player(player_id, name_from_player, points, unlocked_plants, garden), exist_status]
    @staticmethod
    def create_player(player_id, name, group):
        """creates a player"""
        player = get_player_by_id(player_id)
        if player is None:
            create_player_and_their_garden(player_id, group, name, 2, 2)
            exit_status = True
        else:
            exit_status = False
        return exit_status

    @staticmethod
    def remove_player_or_display_error(player_id):
        """removes a player if it exists"""
        player = get_player_by_id(player_id)
        if player is None:
            return False
        else:
            remove_player_by_id(player_id)
            remove_garden_by_id(player_id)
            return True
    @staticmethod
    def check_or_unlock_plant(player_id, prop_id):
        """updates unlocked plants list if necessary"""
        player = get_player_by_id(player_id)
        unlocked_plants = json.loads(player["unlocked_plants"])
        if not prop_id in unlocked_plants:
            update_unlocked_plants(player_id, prop_id)
            _prop = get_plant_props_by_id(prop_id)
            return f"Unlocked {_prop["name"]} seed!"
        else:
            return "no"
    @staticmethod
    def get_group_players(group):
        pass


class GardenService:
    '''Garden service'''
    @staticmethod
    def get_garden_from_db(player_id):
        '''Get garden from db. Raises eeror if that not found'''        
        garden = get_garden_by_player_id(player_id)
        if garden is not None:
            field = json.loads(garden["field"])[:]
            sizex = garden["sizex"]
            sizey = garden["sizey"]
            last_tick = datetime.datetime.strptime(garden["last_tick"], "%Y-%m-%d %H:%M:%S.%f")
            for _i in range(0, sizey): #init field (get real plants from db)
                for _j in range(0, sizex):
                    field[_i][_j] = PlantService.get_plant_by_id(field[_i][_j])
            return Garden(field, sizex, sizey, last_tick)
        raise ValueError("Garden that you tryied to get not exists")
    @staticmethod
    def tick(user_id, garden: Garden):
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
                        delete_plant_by_id(garden_field[_i][_j].get_id())
                        garden_field[_i][_j] = ""
                    else:
                        update_plant(garden_field[_i][_j].get_id(),
                                     garden_field[_i][_j].get_age(),
                                     garden_field[_i][_j].get_status())
        GardenService.mutate(garden)
        update_garden_last_tick(user_id, f"{garden.get_last_tick() + datetime.timedelta(hours=1)}")
        garden.set_last_tick(garden.get_last_tick() + datetime.timedelta(hours=1))
        update_field(user_id, garden.get_field(), garden.get_sizex(), garden.get_sizey())
    @staticmethod
    def mutate(garden):
        """
        Checks each slot in a garden and applies mutations
        """
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
                                newslot = garden_field[ny][nx]
                                if newslot != "" and newslot.get_status() == "Mature":
                                    _plant_idnum = newslot.get_prop_id()
                                    if not _plant_idnum in nearby_plants:
                                        nearby_plants.append(_plant_idnum)
                                        nearby_plants_amounts.append(1)
                                    else:
                                        _idx = nearby_plants.index(_plant_idnum)
                                        nearby_plants_amounts[_idx] += 1
                    for mutation in MutationsService.get_all_mutations_as_model_array():
                        satisfies = True
                        for mutation_plant in mutation.get_plant_list():
                            mutation_plantlist = mutation.get_plant_list()
                            mutation_plant_quantity = mutation.get_plant_quantity()
                            if mutation_plant in nearby_plants:
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
                        if _rand < mutation.get_chance():
                            garden_field[rownum][slotnum] = PlantService.create_plant(mutation.get_outcome_plant())
                slotnum += 1
            rownum += 1

class MutationsService:
    '''Mutation Service'''
    @staticmethod
    def get_all_mutations_as_model_array():
        '''Get all mutations from db and parse it to Mutations array'''
        raw_mutations = get_all_mutations()
        mutations = []
        for raw_mutation in raw_mutations:
            plantlist = json.loads(raw_mutation[0])
            plantquantity = json.loads(raw_mutation[1])
            chance = raw_mutation[2]
            outcomeplant_id = raw_mutation[3]
            mutations.append(Mutations(plantlist, plantquantity, chance, outcomeplant_id))
        return mutations

class PlantService:
    '''Plant service'''
    @staticmethod
    def get_plant_by_id(plant_id):
        '''Need to find a PlantsProps by id'''          
        raw_plant = get_plant_by_id(plant_id)
        if raw_plant is not None:
            return Plant(raw_plant["id"], raw_plant["decay_age"], raw_plant["name"], raw_plant["maturation_age"], raw_plant["prop_id"], raw_plant["age"], raw_plant["status"])
        else:
            return ""
    @staticmethod
    def create_plant(propsid):
        '''Need to create a Plant by propid(foreignkey)'''          
        raw_plant = create_new_plant(propsid)
        if raw_plant is not None:
            return Plant(raw_plant["id"], raw_plant["decay_age"], raw_plant["name"], raw_plant["maturation_age"], raw_plant["prop_id"], raw_plant["age"], raw_plant["status"])
        else:
            return None



class PlantPropsService:
    '''Plant prop Service'''
    @staticmethod
    def get_plant_props_by_id(propsid):
        '''Need to find a Plants by id'''          
        raw_plant = get_plant_props_by_id(propsid)
        return Properties(raw_plant["name"], raw_plant["decay_age"], raw_plant["maturation_age"], raw_plant["points"])




class GameService:
    '''Game Service'''
    @staticmethod
    def plant(player_id, slot, prop_id):
        """
        plants something in the garden
        """
        player = PlayerService.get_player(player_id)[0]
        player_plantlist = player.get_unlocked_plants()
        garden = GardenService.get_garden_from_db(player_id)
        garden_field = garden.get_field()
        garden_sizey = garden.get_sizey()
        garden_sizex = garden.get_sizex()
        try:
            slot = int(slot)
            prop_id = int(prop_id)
        except ValueError:
            return "not_int"
        y = math.ceil(slot / garden_sizey) - 1
        _x = slot % garden_sizex - 1
        if _x == -1:
            _x += garden_sizex
        x = _x
        if x < 0 or x >= garden_sizex or  y < 0 or y >= garden_sizey:
            return "wrong_slot"
        if not prop_id in player_plantlist:
            return "not_available"
        if garden_field[y][x] == "":
            new_plant = PlantService.create_plant(prop_id)
            if new_plant is not None:
                garden_field[y][x] = new_plant
            update_field(player_id, garden_field, garden_sizex, garden_sizey)
            return True
        else:
            return "occupied"
        
    @staticmethod
    def check(user_id, player: Player ):
        """
        Check garden status as player
        """
        garden = player.get_garden_obj()
        garden_last_tick = player.get_garden_obj().get_last_tick()
        total_time = (datetime.datetime.now() - garden_last_tick).total_seconds()
        if total_time > 3600:
            _amount = math.floor((datetime.datetime.now() - garden_last_tick).total_seconds() / 3600)
            for _k in range(_amount):
                GardenService.tick(user_id, garden)
        return garden
    
    @staticmethod
    def image_gen(x, y):
        """generates a base image of a garden"""
        check_image = Image.new('RGB', ((BORDER_WIDTH*2 + x * CELL_WIDTH),(BORDER_WIDTH*2 + y * CELL_WIDTH)),(255,255,255))
        draw_check_image = ImageDraw.Draw(check_image)
        for slot in range(x):
            draw_check_image.line(((BORDER_WIDTH + slot * CELL_WIDTH),(BORDER_WIDTH),(BORDER_WIDTH + slot * CELL_WIDTH),(BORDER_WIDTH + y * CELL_WIDTH)), fill =(100, 10, 10), width=1)
        for slot in range(y):
            draw_check_image.line(((BORDER_WIDTH),(BORDER_WIDTH + slot * CELL_WIDTH),(BORDER_WIDTH + x * CELL_WIDTH),(BORDER_WIDTH  + slot * CELL_WIDTH)), fill =(100, 10, 10), width=1)
    
        draw_check_image.rectangle((0, 0, x * CELL_WIDTH + BORDER_WIDTH*2, y * CELL_WIDTH + BORDER_WIDTH*2),width=BORDER_WIDTH, outline=(10,100,10))
        
        return (draw_check_image, check_image)

    @staticmethod
    def uproot(player_id, slot):
        """collect/uproot a plant"""
        try:
            slot = int(slot)
        except ValueError:
            return "not_int"
        garden = GardenService.get_garden_from_db(player_id)
        garden_field = garden.get_field()
        garden_sizey = garden.get_sizey()
        garden_sizex = garden.get_sizex()
        y = math.ceil(slot / garden_sizey) - 1
        _x = slot % garden_sizex - 1
        if _x == -1:
            _x += garden_sizex
        x = _x
        if x < 0 or x >= garden_sizex or  y < 0 or y >= garden_sizey:
            return "wrong_slot"
        if garden_field[y][x] == "":
            return "slot_empty"
        else:
            plant_id = garden_field[y][x].get_id()
            prop_id = garden_field[y][x].get_prop_id()
            points = get_plant_props_by_id(prop_id)["points"]
            plant_status = garden_field[y][x].get_status()
            if plant_status == "Mature":
                add_points_to_player(player_id, points)
            plant_name= garden_field[y][x].get_name()
            delete_plant_by_id(plant_id)
            garden_field[y][x] = ""
            update_field(player_id, garden_field, garden_sizex, garden_sizey)
            return (plant_name, plant_status, points, prop_id)
