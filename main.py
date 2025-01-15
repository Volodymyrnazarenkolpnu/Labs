"""
main logic script
"""
import datetime
import time
import io
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from services import GameService, PlayerService, PlantPropsService
from setting import BORDER_WIDTH, CELL_WIDTH
KEY = "7548885562:AAGyYJ87KaiZY7LAbm_uu9_u7NFLqnqRmXw"
current_check_users = []

# plants =[]
# mutations = []
# bluecorn = Mutations([0],[2], 10, 0)
# clockberry = Mutations([0],[2], 5, 1)
        #    GardenService.tick(player_id, player.get_garden_obj())
        #GameService.check(player_id, player)      
def sleep():
    """
    Delay between messages
    """
    time.sleep(1)
async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    user_id = user.id
    user_fullname = user.full_name
    group = update.effective_chat
    player_and_status = PlayerService.create_player(user_id, user_fullname, group=group)
    exist_status = player_and_status

    if exist_status is True:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Your account was created!"
        )
    else:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!You already have an account!"
        )

async def top(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    

async def check(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /check is issued."""
    mode = _context.args
    user = update.effective_user
    user_id = user.id
    player_and_status = PlayerService.get_player(user_id)
    if player_and_status[1] is False:
        update.message.reply_text("You need to register first")
    player = player_and_status[0]
    garden = GameService.check(user_id, player)
    garden_x = garden.get_sizex()
    garden_y = garden.get_sizey()
    check_image = GameService.image_gen(garden_x, garden_y)
    draw_check_image = check_image[0]
    if len(mode) > 0:
        if mode[0] == "info":
            garden_data = garden.show_garden()
            _index = 0
            for row in range(garden_x):
                for column in range(garden_y):
                    font = ImageFont.truetype("ArialMT.ttf", size=14)
                    # font = ImageFont.truetype("arial.ttf", size=14)
                    draw_check_image.text((BORDER_WIDTH + CELL_WIDTH * (column) + 7, BORDER_WIDTH + CELL_WIDTH * (row) + 7),
                    f"#{_index + 1}",
                    fill=(0,0,0), anchor="lt", font=font)
                    if garden_data[_index] != "Empty":
                        _prop = PlantPropsService.get_plant_props_by_id(garden_data[_index][4])
                        _decay_age = _prop.get_decay_age()

                        draw_check_image.text((BORDER_WIDTH + CELL_WIDTH * (column)+CELL_WIDTH/2, BORDER_WIDTH + CELL_WIDTH * (row) + CELL_WIDTH/2),
                        str(garden_data[_index][1]),
                        font=font, fill=(0,0,0), align="center", anchor="mm")
                        font = ImageFont.truetype("ArialMT.ttf", size=15)
                        # font = ImageFont.truetype("arial.ttf", size=15)

                        draw_check_image.text((BORDER_WIDTH + CELL_WIDTH * (column) + CELL_WIDTH - 7, BORDER_WIDTH + CELL_WIDTH * (row) + CELL_WIDTH - 7),
                        f"{str(garden_data[_index][2])}/{_decay_age}",
                        fill=(0,0,0), anchor="rb", font=font)

                        _col = (0,0,0)
                        status = garden_data[_index][3]
                        if status == "Growing":
                            _col = (0,120,10)
                        elif status == "Mature":
                            _col = (100, 100, 0)
                        status = status[0]
                        draw_check_image.text((BORDER_WIDTH + CELL_WIDTH * (column) + 7, BORDER_WIDTH + CELL_WIDTH * (row) + CELL_WIDTH - 7),
                        f"{status}",
                        fill=_col, anchor="lb", font=font)
                    else:
                        draw_check_image.text((BORDER_WIDTH + CELL_WIDTH * (column)+CELL_WIDTH/2, BORDER_WIDTH + CELL_WIDTH * (row) + CELL_WIDTH/2),
                        "Empty",
                        font=font, fill=(0,0,0), anchor="mm")
                    _index+=1

    check_image_bio = io.BytesIO()
    check_image_bio.name = "check_image.png"
    check_image[1].save(check_image_bio, "PNG")
    check_image_bio.seek(0)

    await update.message.reply_photo(photo=check_image_bio)
    sleep()

# |empty|empty
#  empty empty

async def quit_game(update : Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """remove a user with a command"""
    user= update.effective_user
    user_id = user.id
    status = PlayerService.remove_player_or_display_error(user_id)
    if status is True:
        await update.message.reply_html(f"""{user.mention_html()},
        your account was deleted succesfully!""")
    else:
        await update.message.reply_html(f"""{user.mention_html()},
        it doesn't look like you have an account""")

async def plant(update : Update, context: ContextTypes.DEFAULT_TYPE):
    """plants something in the garden of the user"""
    user = update.effective_user
    user_id = user.id
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Not enough positional arguments given")
    else:
        slot = context.args[0]
        plant_id = context.args[1]
        status = GameService.plant(user_id, slot, plant_id)
        if status is True:
            plant_name = PlantPropsService.get_plant_props_by_id(plant_id).get_name()
            await update.message.reply_text(f"Successfully planted {plant_name} in slot #{slot}")
        elif status == "occupied":
            await update.message.reply_text("Given slot is already occupied by another plant")
        elif status == "wrong_slot":
            await update.message.reply_text("Given slot is outside of your garden")
        elif status == "not_available":
            await update.message.reply_text("You don't yet have that plant")
        elif status == "not_int":
            await update.message.reply_text("Both slot number and plant id must be integer")
    sleep()

async def collect(update : Update, context: ContextTypes.DEFAULT_TYPE):
    """collect/uproot a plant in the garden of the user"""
    user = update.effective_user
    user_id = user.id
    if not context.args:
        await update.message.reply_text("Not enough positional arguments given")
    else:
        status = GameService.uproot(user_id, context.args[0])
        if status == "not_int":
            await update.message.reply_text("Slot number should be integer")
        elif status == "wrong_slot":
            await update.message.reply_text("Given slot is outside of your garden")
        elif status == "slot_empty":
            await update.message.reply_text("This slot doesn't have any plants")
        else:
            print(status[1])
            if status[1] == "Mature":
                _text = f"""{status[0]} in slot {context.args[0]} collected successfully! Gained {status[2]} points"""
                status = PlayerService.check_or_unlock_plant(user_id, status[3])
                if status != "no":
                    _text += status
                await update.message.reply_text(_text)
            else:
                await update.message.reply_text(f"""{status[0]} in slot {context.args[0]}
                collected successfully!""")
    sleep()

# GameService.plant(player_id, 1, 1)
# GameService.plant(player_id, 4, 2)

application = Application.builder().token(KEY).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("top", top))
application.add_handler(CommandHandler("check", check))
application.add_handler(CommandHandler("quit_game", quit_game))
application.add_handler(CommandHandler("plant", plant))
application.add_handler(CommandHandler("collect", collect))
application.run_polling(allowed_updates=Update.ALL_TYPES)

# print(player.get_garden_obj())
# GameService.plant(player_id, 1, 1)
# GameService.plant(player_id, 4, 2)
# player.set_garden(GardenService.get_garden_from_db(player_id))
# print(player.get_garden_obj().get_last_tick())
# print(player.get_garden_obj())
