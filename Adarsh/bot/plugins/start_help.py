# (c) adarsh-goel 
from Adarsh.bot import StreamBot
from Adarsh.vars import Var
import logging
logger = logging.getLogger(__name__)


from Adarsh.utils.database import Database
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

db = Database(Var.DATABASE_URL, Var.name)
from pyrogram.types import ReplyKeyboardMarkup


buttonz=ReplyKeyboardMarkup(
[
    ["startโก๏ธ","help๐"],
    ["ping๐ก","status๐"]
            
],
resize_keyboard=True
)


@StreamBot.on_message((filters.command("start") | filters.regex('startโก๏ธ')) & filters.private )
async def start(b, m):

    if m.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return
    
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await b.send_message(
            Var.BIN_CHANNEL,
            f"**Nแดแดก Usแดส Jแดษชษดแดแด:** \n\n__Mส Nแดแดก Fสษชแดษดแด__ [{m.from_user.first_name}](tg://user?id={m.from_user.id}) __Sแดแดสแดแดแด Yแดแดส Bแดแด !!__"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await b.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await b.send_message(
                    chat_id=m.chat.id,
                    text="__๐ข๐๐ก๐ก๐จ, ๐จ๐๐ค ๐๐ก๐ ๐๐ก๐ ๐๐๐๐๐๐ ๐๐ก๐๐ ๐ค๐ข๐๐๐ ๐๐. ๐แดษดแดแดแดแด แดสแด ๐แดแด แดสแดแดแดส__\n\n  **๐๐ ๐ฌ๐๐ก๐ก ๐๐๐ก๐ฅ ๐ฎ๐ค๐ช**",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
             await StreamBot.send_photo(
                chat_id=m.chat.id,
                photo="https://telegra.ph/file/9d94fc0af81234943e1a9.jpg",
                caption="<i>๐น๐พ๐ธ๐ฝ CHANNEL ๐๐พ ๐๐๐ด ๐ผ๐ด๐</i>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jแดษชษด ษดแดแดก ๐", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
             return
        except Exception:
            await b.send_message(
                chat_id=m.chat.id,
                text="<i>๐ข๐ธ๐ถ๐ฎ๐ฝ๐ฑ๐ฒ๐ท๐ฐ ๐๐ฎ๐ท๐ฝ ๐๐ป๐ธ๐ท๐ฐ</i> <b> <a href='https://github.com/adarsh-goel'>CLICK HERE FOR SUPPORT </a></b>",
                
                disable_web_page_preview=True)
            return
    await StreamBot.send_photo(
        chat_id=m.chat.id,
        photo ="https://telegra.ph/file/ca10e459bc6f48a4ad0f7.jpg",
        caption =f'Hi {m.from_user.mention(style="md")}!,\nI am Telegram File to Link Generator Bot with Channel support.\nSend me any file and get a direct download link and streamable link.!\n\nCommands\n/start\n/help\n/base_site\n/shortener_api\n/remove_base_site\n/remove_shortener_api',
        reply_markup=buttonz)


@StreamBot.on_message((filters.command("help") | filters.regex('help๐')) & filters.private )
async def help_handler(bot, message):
    if message.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return
    
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id)
        await bot.send_message(
            Var.BIN_CHANNEL,
            f"**Nแดแดก Usแดส Jแดษชษดแดแด **\n\n__Mส Nแดแดก Fสษชแดษดแด__ [{message.from_user.first_name}](tg://user?id={message.from_user.id}) __Started Your Bot !!__"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await bot.get_chat_member(Var.UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="<i>Sแดสสส Sษชส, Yแดแด แดสแด Bแดษดษดแดแด FROM USING แดแด. Cแดษดแดแดแดแด แดสแด Dแดแด แดสแดแดแดส</i>",
                    
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await StreamBot.send_photo(
                chat_id=message.chat.id,
                photo="https://telegra.ph/file/ca10e459bc6f48a4ad0f7.jpg",
                Caption="**๐น๐พ๐ธ๐ฝ ๐๐๐ฟ๐ฟ๐พ๐๐ ๐ถ๐๐พ๐๐ฟ ๐๐พ ๐๐๐ด แดสษชs Bแดแด!**\n\n__Dแดแด แดแด Oแด แดสสแดแดแด, Oษดสส Cสแดษดษดแดส Sแดสsแดสษชสแดสs แดแดษด แดsแด แดสแด Bแดแด!__",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("๐ค Jแดษชษด Uแดแดแดแดแดs Cสแดษดษดแดส", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
            return
        except Exception:
            await bot.send_message(
                chat_id=message.chat.id,
                text="__Sแดแดแดแดสษชษดษข แดกแดษดแด Wสแดษดษข. Cแดษดแดแดแดแด แดแด__ [ADARSH GOEL](https://github.com/adarsh-goel/-pro/issues).",
                disable_web_page_preview=True)
            return
    await message.reply_text(
        text="""<b> Send me any file or video i will give you streamable link and download link.</b>\n
<b> I also support Channels, add me to you Channel and send any media files and see miracleโจ also send /list to know all commands""",
        disable_web_page_preview=True,
    )

@StreamBot.on_message(filters.command("shortener_api") & filters.private)
async def shortener_api_handler(bot, m):
    user_id = m.from_user.id
    user = await db.get_user(user_id)
    api = user.get("shortener_api")
    cmd = m.command
    if len(cmd) == 1:
        s = f"`/shortener_api (shortener_api)`\n\nCurrent shortener api : {api}\n\nEX: `/shortener_api 1aab74171e9891abd0ba799e3fd568c`"
        return await m.reply(s)
    
    elif len(cmd) == 2:
        api = cmd[1].strip()
        await db.update_user_info(user_id, {"shortener_api": api})
        await m.reply(f"Shortener API updated successfully to {api}")


@StreamBot.on_message(filters.command("base_site") & filters.private)
async def base_site_handler(bot, m):
    user_id = m.from_user.id
    user = await db.get_user(user_id)
    cmd = m.command
    site = user.get("base_site")
    text = f"`/base_site (base_site)`\n\nCurrent base site: {site}\n\n EX: `/base_site shareus.in`"
    if len(cmd) == 1:
        return await m.reply(text=text, disable_web_page_preview=True)
    elif len(cmd) == 2:
        base_site = cmd[1].strip()
        await db.update_user_info(user_id, {"base_site": base_site})
        await m.reply("Base Site updated successfully")

@StreamBot.on_message(filters.command("remove_shortener_api") & filters.private)
async def remove_shortener(c, m):
    user_id = m.from_user.id
    user = await db.get_user(user_id)
    if user.get("shortener_api"):
        await db.update_user_info(user_id, {"shortener_api": None})
        await m.reply("Shortener API removed successfully")
    else:
        await m.reply("You don't have any shortener API")


@StreamBot.on_message(filters.command("remove_base_site") & filters.private)
async def remove_base_site(c, m):
    user_id = m.from_user.id
    user = await db.get_user(user_id)
    print(user)
    if user.get("base_site"):
        await db.update_user_info(user_id, {"base_site": None})
        await m.reply("Base Site removed successfully")
    else:
        await m.reply("You don't have any base site")