import datetime
import json
import math
import sqlite3
import numpy


connection = sqlite3.connect('my_database.db')
#region INIT
def init():
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
    name TEXT
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

    connection.commit()
    cursor.close()
#endregion

#region PLAYERS
def create_player_and_their_garden(user_id, username, sizex = 2, sizey = 2):
    field = numpy.full((sizex, sizey), "")
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM PlantsProps')
    first_plant = cursor.fetchone()    
    cursor.execute('INSERT INTO Players (id, username, points, unlocked_plants) VALUES (?, ?, ?, ?)', (user_id, username, 0, json.dumps([first_plant[0]])))
    cursor.execute('INSERT INTO Gardens (id, field, sizex, sizey, last_tick) VALUES (?, ?, ?, ?, ?)', (
        user_id, 
        json.dumps(field.tolist()),
        sizex,
        sizey,
        datetime.datetime.now().__str__()
        ))
    connection.commit()
    cursor.close()
    
def update_player_name(player_id, name):
    cursor = connection.cursor()    
    cursor.execute('UPDATE Players SET username = ? WHERE id = ?', (name, player_id))
    connection.commit()
    cursor.close()
    
def find_player_by_id(user_id):    
    cursor = connection.cursor()    
    cursor.execute('SELECT username, points, unlocked_plants FROM Players WHERE id = ?', (user_id,))
    user = cursor.fetchone()     
    cursor.close()
    return user
#endregion

#region GARDEN
def find_garden_by_player_id(user_id):    
    cursor = connection.cursor()    
    cursor.execute('SELECT field, sizex, sizey, last_tick FROM Gardens WHERE id = ?', (user_id,))
    garden = cursor.fetchone()     
    cursor.close()
    return garden


def update_field(user_id, garden_field):
    cursor = connection.cursor()    
    cursor.execute('UPDATE Gardens SET field = ? WHERE id = ?', (json.dumps(garden_field), user_id))
    connection.commit()
    cursor.close()

#endregion
    
#region MUTATION
def get_all_mutations():    
    cursor = connection.cursor()    
    cursor.execute('SELECT plantlist, plantquantity, chance, outcomeplant_id FROM Mutations')
    raw_mutations = cursor.fetchall()     
    cursor.close()

    return raw_mutations
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


