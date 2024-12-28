from telebot import types,TeleBot
from db.primaryutils import BotDatabase
from .adminpanel import admincmds,admins,handleadmincmd
db = BotDatabase()

users_in_bot = db.fetch_users()
users = {}
print(users)
freeid = None

def find(message: types.Message,bot):
    global freeid

    if message.chat.id not in users:
        bot.send_message(message.chat.id, 'Finding...')

        if freeid is None and freeid != message.chat.id:
            freeid = message.chat.id
        else:
            # Question:
            # Is there any way to simplify this like `bot.send_message([message.chat.id, freeid], 'Founded!')`?
            bot.send_message(message.chat.id, f'Found a partner!')
            bot.send_message(message.chat.id, f'You are talking with - {bot.get_chat(freeid).first_name}\n\nuse /stop to stop chat')
            bot.send_message(freeid, f'Found a partner!')
            bot.send_message(freeid,f"You are talking with - {message.chat.first_name}\n\nuse /stop to stop chat")

            users[freeid] = message.chat.id
            users[message.chat.id] = freeid
            freeid = None

        #print(users, freeid) # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'You are already in a chat!')



def stop(message: types.Message,bot):
    global freeid

    if message.chat.id in users:
        bot.send_message(message.chat.id, 'You have left the chat\n\n/find - to find a new partner')
        bot.send_message(users[message.chat.id], 'Your partner has left the chat\n\n/find - to find a new partner')

        del users[users[message.chat.id]]
        del users[message.chat.id]
        
        #print(users, freeid) # Debug purpose, you can remove that line
    elif message.chat.id == freeid:
        bot.send_message(message.chat.id, 'Stopped successfully')
        freeid = None
        

        #print(users, freeid) # Debug purpose, you can remove that line
    else:
        bot.send_message(message.chat.id, 'You are not in search!')




def chatting(message: types.Message,bot:TeleBot):
    if message.chat.id in users and message.text not in admincmds:
        bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)
    elif message.chat.id in admins and message.text.startswith(tuple(admincmds)) :
        print("admin")
        handleadmincmd(message,bot)
    elif message.text in admincmds and message.chat.id not in admins:
        bot.copy_message(users[message.chat.id], users[users[message.chat.id]], message.id)
    else:
        bot.send_message(message.chat.id, 'No one can hear you...')