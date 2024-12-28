import telebot
import flask,json


bot = telebot.TeleBot('8072433858:AAEnZOGA0VAQp7BuaTUbzvahSk75Y4uhqrU')
app = flask.Flask(__name__)

with open("config.json") as config_file:
    config = json.load(config_file)


BOT_TOKEN = config["bot_token"]
WEBHOOK_URL = config["webhook_url"]
ALLOWED_UPDATES = config.get("allowed_updates", None)
LOG_LEVEL = config.get("log_level", "INFO")

@app.route("/webhook", methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


from commands.start import startcmd
from commands.talklogic import find,stop,chatting
from commands.adminpanel import admin

bot.register_message_handler(commands=["start"],callback=startcmd,pass_bot=True)
bot.register_message_handler(commands=["find"],callback=find,pass_bot=True)
bot.register_message_handler(commands=['stop'],pass_bot=True,callback=stop)
bot.register_message_handler(commands=['admin'],pass_bot=True,callback=admin)
bot.register_message_handler(content_types=['animation', 'audio', 'contact', 'dice', 'document', 'location', 'photo', 'poll', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'],callback=chatting,pass_bot=True)

bot.remove_webhook()
webhookurl = "https://"+WEBHOOK_URL+"/webhook"
bot.set_webhook(url=webhookurl)