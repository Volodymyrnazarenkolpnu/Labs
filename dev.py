"""DEV"""
from services import GardenService, PlayerService
def devloop():
    """DEVLOOP"""
    while True:
        inp = input()
        #GameService.check(player_id, player)
        if inp == "exit":
            exit()
        if inp == "tick":
            player_id = input()
            player = PlayerService.get_player_or_create_db(player_id, "")[0]
            garden = player.get_garden_obj()
            print(GardenService.tick(player_id, garden))
devloop()
