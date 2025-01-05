"""
main logic script
"""
import datetime
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from services import GameService, PlayerService, PlantPropsService
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
    player_and_status = PlayerService.get_player_or_create_db(user_id, user_fullname)
    exist_status = player_and_status[1]


    if exist_status is False:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Your account was created!"
        )
    else:
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!You already have an account!"
        )

class CurrentCheckUser:
    """player object for when few instances of /check is run"""
    def __init__(self, player_id, cursor_x, cursor_y, last_action_time):
        self.player_id = player_id
        self.cursor_x = cursor_x
        self.cursor_y = cursor_y
        self.last_action_time = last_action_time

async def check(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /check is issued."""

    user = update.effective_user
    user_id = user.id
    user_name = user.full_name
    cursor_x = 0
    cursor_y = 0
    last_action_time = datetime.datetime.now()
    user = CurrentCheckUser(user_id, cursor_x, cursor_y, last_action_time)
    current_userlist = list(filter(lambda user: user_id == user.player_id, current_check_users))
    if len(current_userlist) < 1:
        current_check_users.append(user)
    keyboard = [[InlineKeyboardButton("Plant", callback_data=f"Plant_{user_id}"),InlineKeyboardButton("Up", callback_data=f"Up_{user_id}"),InlineKeyboardButton("Upoot", callback_data=f"Uproot_{user_id}")],
    [InlineKeyboardButton("Left", callback_data=f"Left_{user_id}"),InlineKeyboardButton("Down", callback_data=f"Down_{user_id}"),InlineKeyboardButton("Right", callback_data=f"Right_{user_id}")]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    player = PlayerService.get_player_or_create_db(user_id, user_name)[0]
    garden = GameService.check(user_id, player)
    txt = garden.show_garden(0,0)
    await update.message.reply_text(txt,  reply_markup= reply_markup)
    sleep()

async def check_buttons(update : Update, _context: ContextTypes.DEFAULT_TYPE):
    """Process /check button inpust"""
    querry = update.callback_query
    querry_data = querry.data.split("_")
    querry_data[1] = int(querry_data[1])
    querry_user = querry.from_user.id
    print(current_check_users)
    print(querry_data[1])
    print(querry_user)
    current_userlist = list(filter(lambda user: querry_data[1] == user.player_id, current_check_users))
    cursor_x = current_userlist[0].cursor_x
    cursor_y = current_userlist[0].cursor_y
    user_id = querry_data[1]
    player = PlayerService.get_player_or_create_db(user_id, user_id)[0]
    garden = GameService.check(user_id, player)
    if querry_user != querry_data[1]:
        await querry.answer("Not yours!")
        return
    if querry_data[0] == "Up":
        if cursor_y > 0:
            cursor_y -= 1
            index = current_check_users.index(current_userlist[0])
            current_check_users[index].cursor_y = cursor_y
        else:
            await querry.answer("Error")
            return
    elif querry_data[0] == "Down":
        sizey = garden.get_sizey()
        if cursor_y < sizey - 1:
            cursor_y += 1
            index = current_check_users.index(current_userlist[0])
            current_check_users[index].cursor_y = cursor_y
        else:
            await querry.answer("Error")
            return
    elif querry_data[0] == "Left":
        if cursor_x > 0:
            cursor_x -= 1
            index = current_check_users.index(current_userlist[0])
            current_check_users[index].cursor_x = cursor_x
        else:
            await querry.answer("Error")
            return
    elif querry_data[0] == "Right":
        sizex = garden.get_sizex()
        if cursor_x < sizex - 1:
            cursor_x += 1
            index = current_check_users.index(current_userlist[0])
            current_check_users[index].cursor_x = cursor_x
        else:
            await querry.answer("Error")
            return
    elif querry_data[0] == "Plant":
        pass
    elif querry_data[0] == "Uproot":
        pass
    txt = garden.show_garden(cursor_x, cursor_y)
    keyboard = [
        [
            InlineKeyboardButton("Plant", callback_data=f"Plant_{user_id}"),
            InlineKeyboardButton("Up", callback_data=f"Up_{user_id}"),
            InlineKeyboardButton("Upoot", callback_data=f"Uproot_{user_id}")
        ],
        [
            InlineKeyboardButton("Left", callback_data=f"Left_{user_id}"),
            InlineKeyboardButton("Down", callback_data=f"Down_{user_id}"),
            InlineKeyboardButton("Right", callback_data=f"Right_{user_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await querry.edit_message_text(text=txt, reply_markup=reply_markup)
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
    user_name = user.full_name
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Not enough positional arguments given")
    else:
        slot = context.args[0]
        plant_id = context.args[1]
        status = GameService.plant(user_id, slot, plant_id, user_name)
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
                await update.message.reply_text(f"""{status[0]} in slot {context.args[0]}
                 collected successfully! Gained {status[2]} points""")
            else:
                await update.message.reply_text(f"""{status[0]} in slot {context.args[0]}
                 collected successfully!""")
    sleep()

# GameService.plant(player_id, 1, 1)
# GameService.plant(player_id, 4, 2)

application = Application.builder().token(KEY).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("check", check))
application.add_handler(CommandHandler("quit_game", quit_game))
application.add_handler(CommandHandler("plant", plant))
application.add_handler(CommandHandler("collect", collect))
application.add_handler(CallbackQueryHandler(check_buttons))
application.run_polling(allowed_updates=Update.MESSAGE)

# print(player.get_garden_obj())
# GameService.plant(player_id, 1, 1)
# GameService.plant(player_id, 4, 2)
# player.set_garden(GardenService.get_garden_from_db(player_id))
# print(player.get_garden_obj().get_last_tick())
# print(player.get_garden_obj())
