import re
import os
from os import environ
from pyrogram import enums
from Script import script
import asyncio
import json
from collections import defaultdict
from pyrogram import Client

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

#main variables
API_ID = int(environ.get('API_ID', '26128908'))
API_HASH = environ.get('API_HASH', '6bf92ae138ac065939834600e14db146')
BOT_TOKEN = environ.get('BOT_TOKEN', '7559253315:AAEsbyOGfpXuO_9vfRwMIKyofv90kjUCssw')
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '1769132732 560951157').split()]
USERNAME = environ.get('USERNAME', 'https://telegram.me/Stevettan')
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002145049116'))
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002517992667').split()]
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://cmbot5db1:cmbot5db1@cluster0.xa7rvom.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI2 = environ.get('DATABASE_URI2', "mongodb+srv://cmbot5db2:cmbot5db2@cluster0.w5raldn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'TheSeatimebotsfives')
LOG_API_CHANNEL = int(environ.get('LOG_API_CHANNEL', '-1002145049116'))
QR_CODE = environ.get('QR_CODE', 'https://envs.sh/wam.jpg')
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '-1002508695057').split()]

#this vars is for when heroku or koyeb acc get banned, then change this vars as your file to link bot name
BIN_CHANNEL = int(environ.get('BIN_CHANNEL', '-1002145049116'))
URL = environ.get('URL', 'https://heroku.com/botbsbsbbshbs/')

# verify system vars
IS_VERIFY = is_enabled('IS_VERIFY', False)
LOG_VR_CHANNEL = int(environ.get('LOG_VR_CHANNEL', '-1002145049116'))
TUTORIAL = environ.get("TUTORIAL", "https://youtu.be/0c-i2Lol6LU")
TUTORIAL2 = environ.get("TUTORIAL2", "https://youtu.be/GdaUbzxDTKs")
TUTORIAL3 = environ.get("TUTORIAL3", "https://youtu.be/rddlpYLm0G0")
VERIFY_IMG = environ.get("VERIFY_IMG", "https://graph.org/file/45a270fc6a0a1c183c614.jpg")
SHORTENER_API = environ.get("SHORTENER_API", "8c09653e5c38f84d1b76ad3197c5a023e53b494d")
SHORTENER_WEBSITE = environ.get("SHORTENER_WEBSITE", "onepagelink.in")
SHORTENER_API2 = environ.get("SHORTENER_API2", "0c8ebd63bfe9f67f9970b8767498ff60316b9b03")
SHORTENER_WEBSITE2 = environ.get("SHORTENER_WEBSITE2", "tnshort.net")
SHORTENER_API3 = environ.get("SHORTENER_API3", "9c5a6c96077a1b499d8f953331221159383eb434")
SHORTENER_WEBSITE3 = environ.get("SHORTENER_WEBSITE3", "omegalinks.in")
TWO_VERIFY_GAP = int(environ.get('TWO_VERIFY_GAP', "3600"))
THREE_VERIFY_GAP = int(environ.get('THREE_VERIFY_GAP', "21600"))

# languages search
LANGUAGES = ["hindi", "english", "telugu", "tamil", "kannada", "malayalam"]

auth_channel = environ.get('AUTH_CHANNEL', '-1002564896363')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
SUPPORT_GROUP = int(environ.get('SUPPORT_GROUP', '-1002145049116'))

# Working groups for search restriction bot only works on this channels 
WORKING_GROUPS = environ.get('WORKING_GROUPS', "-1002345891582 -1002227429072 -1001992521975")  # Space-separated group IDs
ALLOWED_GROUP_IDS = [int(group_id) for group_id in WORKING_GROUPS.split()] if WORKING_GROUPS else []

# bot settings
AUTO_FILTER = is_enabled('AUTO_FILTER', True)
PORT = os.environ.get('PORT', '8080')
MAX_BTN = int(environ.get('MAX_BTN', '8'))
AUTO_DELETE = is_enabled('AUTO_DELETE', False)
DELETE_TIME = int(environ.get('DELETE_TIME', 600))
IMDB = is_enabled('IMDB', False)
FILE_CAPTION = environ.get('FILE_CAPTION', f'{script.FILE_CAPTION}')
IMDB_TEMPLATE = environ.get('IMDB_TEMPLATE', f'{script.IMDB_TEMPLATE_TXT}')
LONG_IMDB_DESCRIPTION = is_enabled('LONG_IMDB_DESCRIPTION', False)
PROTECT_CONTENT = is_enabled('PROTECT_CONTENT', False)
SPELL_CHECK = is_enabled('SPELL_CHECK', False)
LINK_MODE = is_enabled('LINK_MODE', False)
PM_SEARCH = is_enabled('PM_SEARCH', False)
