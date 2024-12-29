"""
main logic script
"""
from db import find_player_by_id, find_garden_by_player_id, create_player_and_their_garden, update_field
from random import randint

from services import get_player_or_create_db, tick


# plants =[]
# mutations = []
# bluecorn = Mutations([0],[2], 10, 0)
# clockberry = Mutations([0],[2], 5, 1)

player_id = "maximka"
player = get_player_or_create_db(player_id, "david")
print(player.get_garden_obj())

# player.plant(player_id, 1, 1)
# player.plant(player_id, 4, 2)
print(player.get_garden_obj().get_last_tick())
print(player.get_garden_obj())
while True:
    inp = input()
    #player.check(player_id)
    if inp == "exit":
        exit()
    # if inp == "tick":
        # tick(player.get_garden_obj())
