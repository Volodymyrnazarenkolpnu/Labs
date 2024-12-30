'''File for work with sqlite database directly'''
import copy
import datetime
import json
import os
import sqlite3
import numpy


#region INIT
def init():
    '''INIT DB FOR FIRST LAUNCH'''
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Players (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    points INTEGER INT,
    unlocked_plants TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gardens (
    id TEXT PRIMARY KEY,
    field TEXT,
    sizex INTEGER INT,
    sizey INTEGER INT,
    last_tick TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PlantsProps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,    
    decay_age INTEGER INT,    
    maturation_age INTEGER INT,   
    name TEXT,
    points INTEGER INT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Plants(
    id INTEGER PRIMARY KEY AUTOINCREMENT,    
    age INTEGER INT,    
    status TEXT NOT NULL,
    plant_props_id INTEGER INT,
    FOREIGN KEY(plant_props_id) REFERENCES PlantsProps(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mutations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,    
    plantlist TEXT NOT NULL,
    plantquantity TEXT NOT NULL,
    chance INTEGER INT NOT NULL,
    outcomeplant_id INTEGER INT,
    FOREIGN KEY(outcomeplant_id) REFERENCES PlantsProps(id)
    )
    ''')
    cursor.execute('INSERT INTO PlantsProps (name, decay_age, maturation_age) VALUES ("Blue Corn", 6, 3)')
    cursor.execute('INSERT INTO PlantsProps (name, decay_age, maturation_age) VALUES ("Clockberry", 10, 7)')
    cursor.execute('INSERT INTO Mutations (plantlist, plantquantity, chance, outcomeplant_id) VALUES (?, ?, 10, 1)', (json.dumps([1]),json.dumps([2])))
    cursor.execute('INSERT INTO Mutations (plantlist, plantquantity, chance, outcomeplant_id) VALUES (?, ?, 5, 2)', (json.dumps([1]),json.dumps([2])))

    connection.commit()
    cursor.close()
    connection.close()
#endregion
DB_FILE = 'my_database.db'
if not os.path.exists(DB_FILE):
    print("Database file not found. Initializing...")
    init()
connection = sqlite3.connect(DB_FILE)

#region PLAYERS
def create_player_and_their_garden(user_id, username, sizex = 2, sizey = 2):
    '''Create player and garden for them'''
    field = numpy.full((sizex, sizey), "")
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM PlantsProps')
    first_plant = cursor.fetchone()    
    cursor.execute('INSERT INTO Players (id, username, points, unlocked_plants) VALUES (?, ?, ?, ?)'
                   , (user_id, username, 0, json.dumps([first_plant[0]])))
    cursor.execute('INSERT INTO Gardens (id, field, sizex, sizey, last_tick) VALUES (?, ?, ?, ?, ?)'
                   , (user_id, json.dumps(field.tolist()), sizex, sizey, f"{datetime.datetime.now()}"))
    connection.commit()
    cursor.close()
def update_player_name(player_id, name):
    '''Update player name'''
    cursor = connection.cursor()
    cursor.execute('UPDATE Players SET username = ? WHERE id = ?', (name, player_id))
    connection.commit()
    cursor.close()
def get_player_by_id(user_id):
    '''Need to find a player by player_id'''
    cursor = connection.cursor()
    cursor.execute('SELECT username, points, unlocked_plants FROM Players WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if(user is not None):
        return {"username": user[0], "points": user[1], "unlocked_plants": user[2]}
    return None
def remove_player_by_id(user_id):
    """removes a player from db"""
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Players WHERE id = ?", (user_id,))
    connection.commit()
    cursor.close()
    return True
def remove_garden_by_id(garden_id):
    """removes a garden from db"""
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Gardens WHERE id = ?", (garden_id,))
    connection.commit()
    cursor.close()
    return True
#endregion

#region GARDEN
def update_garden_last_tick(garden_id, last_tick):
    '''Update lasttick'''
    cursor = connection.cursor()
    cursor.execute('UPDATE Gardens SET last_tick = ? WHERE id = ?', (last_tick, garden_id,))
    connection.commit()
    cursor.close()

def get_garden_by_player_id(user_id):
    '''Need to find a garden of player by player_id'''
    cursor = connection.cursor()
    cursor.execute('SELECT field, sizex, sizey, last_tick FROM Gardens WHERE id = ?', (user_id,))
    garden = cursor.fetchone()
    cursor.close()
    return {"field": garden[0], "sizex": garden[1], "sizey": garden[2], "last_tick": garden[3]}


def update_field(user_id, garden_field, sizex, sizey):
    '''Update a field in the garden'''
    cursor = connection.cursor()
    field_for_ser = copy.deepcopy(garden_field)
    for _i in range(0, sizey):
        for _j in range(0, sizex):
            if garden_field[_i][_j] != '':
                field_for_ser[_i][_j] = garden_field[_i][_j].get_id()
     
    cursor.execute('UPDATE Gardens SET field = ? WHERE id = ?', (json.dumps(field_for_ser), user_id))
    connection.commit()
    cursor.close()

#endregion
#region MUTATION
def get_all_mutations():
    '''Get all mutations'''
    cursor = connection.cursor()
    cursor.execute('SELECT plantlist, plantquantity, chance, outcomeplant_id FROM Mutations')
    raw_mutations = cursor.fetchall()
    cursor.close()

    return raw_mutations
#endregion
#region Plants Props
def get_plant_by_id(plantid):
    '''Need to find a plant by id'''
    cursor = connection.cursor()
    cursor.execute("SELECT Plants.id, age, status, name, decay_age, maturation_age, PlantsProps.id as prop_id FROM Plants INNER JOIN PlantsProps ON PlantsProps.id = Plants.plant_props_id WHERE Plants.id = ?",(plantid,))
    plant = cursor.fetchone()
    cursor.close()
    if plant is not None:
        return {"id": plant[0], "age": plant[1], "status": plant[2], "name": plant[3], "decay_age": plant[4], "maturation_age": plant[5], "prop_id": plant[6]}
    return None
    #raise ValueError("Plant not found")

def create_new_plant(propid):
    '''Need to create a plant by propid(foreign key)'''
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Plants (age, status, plant_props_id) VALUES (0, ?, ?)', ("Growing", propid))
    connection.commit()
    plant_id = cursor.lastrowid
    cursor.close()
    return get_plant_by_id(plant_id)
def update_plant(plantid, age, status):
    '''Update a plant'''
    cursor = connection.cursor()
    cursor.execute('UPDATE Plants SET age=?, status=? WHERE id=?', (age, status, plantid))
    connection.commit()
    
def delete_plant_by_id(plantid):
    '''Update a plant'''
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Plants WHERE id=?', (plantid,))
    connection.commit()

#endregion
#region Plants Props
def get_plant_props_by_id(propsid):
    '''Need to find a PlantsProps by id'''
    cursor = connection.cursor()
    cursor.execute('SELECT name, decay_age, maturation_age FROM PlantsProps WHERE id = ?', (propsid,))
    plant = cursor.fetchone()
    cursor.close()
    return {"name": plant[0], "decay_age": plant[1], "maturation_age": plant[2]}
#endregion


#def fill_ids_to_plants(user_id):
# cursor = connection.cursor()
# cursor.execute('DELETE FROM Gardens WHERE id = ?', ("maximka1",))
# cursor.execute('DELETE FROM Players WHERE id = ?', ("maximka1",))
# connection.commit()
#init()
#create_player_and_their_garden("maximka", "david")
# print(find_player_by_id("maximka") == None)
#connection.close()
