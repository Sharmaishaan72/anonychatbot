from telebot import types
from db.primaryutils import BotDatabase

db = BotDatabase()

def startcmd(message: types.Message,bot):
    check = db.return_user_data(message.chat.id)
    if check and not check[2] == "T":
        bot.send_message(message.chat.id, 'Just use /find command!')
    elif not check:
        db.add_user(message.chat.id)
        bot.send_message(message.chat.id,"Welcome to the bot!")
    elif check[2] == "T":
        bot.send_message(message.chat.id,"You are banned from the bot!")
