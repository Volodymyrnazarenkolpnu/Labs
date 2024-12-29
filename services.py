import datetime
import json
import math
from random import randint
from db import create_player_and_their_garden, find_garden_by_player_id, find_player_by_id, get_all_mutations, update_field, update_player_name
from models import Garden, Mutations, Plant, Player

#region Player
def get_player_or_create_db(player_id, name):
    player = find_player_by_id(player_id)
    if player is None:    
        create_player_and_their_garden(player_id, name, 2, 2)
        player = find_player_by_id(player_id)           
    name_from_player = player[0]            
    points = player[1]
    unlocked_plants = json.loads(player[2])
    garden = get_garden_from_db(player_id)
    if name is not name_from_player:
        update_player_name(player_id, name)            
    return Player(name_from_player, points, unlocked_plants, garden)
    
 #endregion

#region Garden
def get_garden_from_db(player_id):
    garden = find_garden_by_player_id(player_id)
    if garden is not None:
        field = json.loads(garden[0])
        sizex = garden[1]
        sizey = garden[2]
        last_tick = datetime.datetime.strptime(garden[3], "%Y-%m-%d %H:%M:%S.%f")
        return Garden(field, sizex, sizey, last_tick)
    else: 
        print("Garden not found!")
        return None    
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
    update_field(garden.get_field())  
                
def garden_update_field(field):
    update_field(field)  
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
                            if garden_field[ny][nx] != "" and garden_field[ny][nx].get_status() == "Mature":
                                _plant_idnum = garden_field[ny][nx].get_idnum()
                                if not nearby_plants.__contains__(_plant_idnum):
                                    nearby_plants.append(_plant_idnum)
                                    nearby_plants_amounts.append(1)
                                else:
                                    _idx = nearby_plants.index(_plant_idnum)
                                    nearby_plants_amounts[_idx] += 1
                for mutation in MutationsMethods.get_all_mutations_as_model_array():
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

#endregion

#region mutations
def get_all_mutations_as_model_array():            
    raw_mutations = get_all_mutations()        
    mutations = []
  
    for raw_mutation in raw_mutations:
        plantlist = json.loads(raw_mutation[0])
        plantquantity = json.loads(raw_mutation[1])
        chance = raw_mutation[2]
        outcomeplant_id = raw_mutation[3]    
        mutations.append(Mutations(plantlist, plantquantity, chance, outcomeplant_id))
    return mutations
#endregion