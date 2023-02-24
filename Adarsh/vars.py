# (c) adarsh-goel
import os
from os import getenv, environ
from dotenv import load_dotenv



load_dotenv()









class Var(object):
    MULTI_CLIENT = False
    API_ID = int(getenv('API_ID'))
    API_HASH = str(getenv('API_HASH'))
    BOT_TOKEN = str(getenv('BOT_TOKEN'))
    name = str(getenv('name', 'filetolinkbot'))
    SLEEP_THRESHOLD = int(getenv('SLEEP_THRESHOLD', '60'))
    WORKERS = int(getenv('WORKERS', '4'))
    BIN_CHANNEL = int(getenv('BIN_CHANNEL'))
    PORT = int(getenv('PORT', 8080))
    BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '0.0.0.0'))
    PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
    OWNER_ID = {int(x) for x in os.environ.get("OWNER_ID", "").split()}
    NO_PORT = bool(getenv('NO_PORT', False))
    APP_NAME = None
    OWNER_USERNAME = str(getenv('OWNER_USERNAME'))
    REPLIT_USERNAME = str(getenv('REPLIT_USERNAME'))
    ON_HEROKU = bool(APP_NAME := getenv('APP_NAME'))
    FQDN = (
        str(getenv('FQDN', BIND_ADRESS))
        if not ON_HEROKU or getenv('FQDN')
        else f'{APP_NAME}.{REPLIT_USERNAME}.repl.co'
    )
    HAS_SSL=bool(getenv('HAS_SSL',False))
    if ON_HEROKU:
        URL = f"https://{FQDN}/dl/"
    else:
        URL = f'http{"s" if HAS_SSL else ""}://{FQDN}{"" if NO_PORT else f":{PORT}"}/dl/'
    DATABASE_URL = str(getenv('DATABASE_URL'))
    UPDATES_CHANNEL = str(getenv('UPDATES_CHANNEL', None))
    BANNED_CHANNELS = list(
        {
            int(x)
            for x in str(getenv("BANNED_CHANNELS", "-1001362659779")).split()
        }
    )
    BOT_USERNAME = str(getenv('BOT_USERNAME'))
    AD1 = str(getenv('AD1', ""))
    AD2 = str(getenv('AD2', ""))
    AD3 = str(getenv('AD3', ""))
    AD4 = str(getenv('AD4', ""))
    AD5 = str(getenv('AD5', ""))
    AD6 = str(getenv('AD6', ""))
    USERS_CAN_USE = getenv('USERS_CAN_USE', False)
    ADMINS = (
        [int(i.strip()) for i in os.environ.get("ADMINS").split(",")]
        if os.environ.get("ADMINS")
        else []
    )
    IS_DISPLAY_DL_LINK = getenv('IS_DISPLAY_DL_LINK', False)
    VIDEO_AD = getenv('VIDEO_AD', "")