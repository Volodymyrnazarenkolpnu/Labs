"""
main logic script
"""
from services import GameService, GardenService, PlayerService


# plants =[]
# mutations = []
# bluecorn = Mutations([0],[2], 10, 0)
# clockberry = Mutations([0],[2], 5, 1)



player_id = "maximka"
player = PlayerService.get_player_or_create_db(player_id, "david")
print(player.get_garden_obj())
GameService.plant(player_id, 1, 1)
GameService.plant(player_id, 4, 2)
player.set_garden(GardenService.get_garden_from_db(player_id))
print(player.get_garden_obj().get_last_tick())
print(player.get_garden_obj())
while True:
    inp = input()
    GameService.check(player_id, player)
    if inp == "exit":
        exit()
    if inp == "tick":
        GardenService.tick(player_id, player.get_garden_obj())
