from telebot import types,TeleBot
from db.primaryutils import BotDatabase
db = BotDatabase()
admincmds = ['/freeids','/broadcast']
admins = [1097600241]

def admin(message: types.Message,bot):
    if message.chat.id == 1097600241:
        bot.send_message(message.chat.id,"/broadcast {MESSAGE} to broadcast a message")
    
def handleadmincmd(message,bot:TeleBot):
    msg = message.text
    if msg.startswith("/broadcast"):
        broadcast = msg.partition(" ")[2]
        users = db.fetch_users()
        broadcastmsg = f"#Broadcast\n\n{broadcast}"
        sent = 0 
        fails = 0
        bmsg = bot.send_message(message.chat.id,f"Running Broadcast:\n\nStatistics:\nSent: {sent}\nFails:{fails}")
        for i in range(len(users)):
          try:
            bot.send_message(users[i][0],broadcastmsg)
            sent +=1
            bot.edit_message_text(f"Running Broadcast:\n\nStatistics:\nSent: {sent}\nFails:{fails}",chat_id=bmsg.chat.id,message_id=bmsg.id)
          except:
             fails+=1
             bot.edit_message_text(f"Running Broadcast:\n\nStatistics:\nSent: {sent}\nFails:{fails}",chat_id=bmsg.chat.id,message_id=bmsg.id)

    elif msg == "/freeids":
        bot.send_message(message.chat.id,"idk")


