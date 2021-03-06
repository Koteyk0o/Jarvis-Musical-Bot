import telebot
import json
from spotify_Module import bot_Spotify_Module
from spotify_Module import bot_Inline_Handler
from spotify_Module import bot_Callback_Handler

with open("bot_Keys.json") as json_File:
    bot_Keys_File = json.load(json_File)

spotify_Bot = telebot.TeleBot(bot_Keys_File["telegram"]["telegram_Key"])



@spotify_Bot.callback_query_handler(func=lambda call: True) #Callback buttons handler
def get_Callback_Data(call):
    bot_Callback_Handler.process_Callback_Data(call)

@spotify_Bot.inline_handler(func=lambda query: len(query.query) > 0) #Inline mode handler
def get_Inline_Data(query):
    bot_Inline_Handler.process_Inline_Data(query)

@spotify_Bot.message_handler(commands=["logout"]) #Logout command handler
def logout_Command_Handler(message):
    bot_Spotify_Module.logout_Command(message)

@spotify_Bot.message_handler(commands=["menu"]) #Menu command handler
def menu_Command_Handler(message):
    bot_Spotify_Module.menu_Command(message)

@spotify_Bot.message_handler(commands=["language"]) #Language command handler
def language_Command_Handler(message):
    bot_Spotify_Module.language_Command(message)

@spotify_Bot.message_handler(commands=["contacts"]) #Contacts command handler
def contacts_Command_Handler(message):
    bot_Spotify_Module.contacts_Command(message)

@spotify_Bot.message_handler(content_types=["text", "photo"]) #Messages handler
def get_Text_Message(message):
    bot_Spotify_Module.chat_Messages_Handler(message)



print("Mothership launched!")



def proceed_Updates(json_Updates):
    update = telebot.types.Update.de_json(json_Updates)
    spotify_Bot.process_new_updates([update])