#(c) Adarsh-Goel
import os
import asyncio
from asyncio import TimeoutError
from Adarsh.bot import StreamBot
from Adarsh.utils.database import Database
from Adarsh.utils.human_readable import humanbytes
from Adarsh.vars import Var
# from urllib.parse import quote_plus
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from shortzy import Shortzy

from urllib.parse import quote as quote_plus

from Adarsh.utils.file_properties import get_name, get_hash, get_media_file_size
db = Database(Var.DATABASE_URL, Var.name)



@StreamBot.on_message((filters.private) & (filters.document | filters.video | filters.audio | filters.photo) , group=4)
async def private_receive_handler(c: Client, m: Message):

    if m.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return

    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id)
        await c.send_message(
            Var.BIN_CHANNEL,
            f"New User Joined! : \n\n Name : [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started Your Bot!!"
        )
    if Var.UPDATES_CHANNEL != "None":
        try:
            user = await c.get_chat_member(Var.UPDATES_CHANNEL, m.chat.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.chat.id,
                    text="You are banned!",
                    
                    disable_web_page_preview=True
                )
                return 
        except UserNotParticipant:
            await c.send_message(
                chat_id=m.chat.id,
                text="""<i>πΉπΎπΈπ½ UPDATES CHANNEL ππΎ πππ΄ πΌπ΄ π</i>""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jα΄ΙͺΙ΄ Ι΄α΄α΄‘ π", url=f"https://t.me/{Var.UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                
            )
            return
        except Exception as e:
            await m.reply_text(e)
            await c.send_message(
                chat_id=m.chat.id,
                text="**Sα΄α΄α΄α΄ΚΙͺΙ΄Ι’ α΄‘α΄Ι΄α΄ WΚα΄Ι΄Ι’. Cα΄Ι΄α΄α΄α΄α΄ α΄Κ Κα΄ss** [Adarsh Goel](https://github.com/adarsh-goel)",
                
                disable_web_page_preview=True)
            return
    try:
        user = await db.get_user(m.from_user.id)
        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        og_stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        stream_link = await short_link(og_stream_link, user)

        og_online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = await short_link(og_online_link, user) if Var.IS_DISPLAY_DL_LINK else stream_link

        msg_text ="""<i><u>π¬πΌππΏ ππΆπ»πΈ ππ²π»π²πΏπ?ππ²π± !</u></i>\n\n<b>π FΙͺΚα΄ Ι΄α΄α΄α΄ :</b> <i>{}</i>\n\n<b>π¦ FΙͺΚα΄ κ±Ιͺα΄’α΄ :</b> <i>{}</i>\n\n<b>π₯ Dα΄α΄‘Ι΄Κα΄α΄α΄ / π₯WATCH :</b> <i>{}</i>\n\n<b>πΈ Nα΄α΄α΄ : LINK WON'T EXPIRE TILL I DELETE</b>"""

        await log_msg.reply_text(text=f"**Rα΄Qα΄α΄κ±α΄α΄α΄ ΚΚ :** [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n**Uκ±α΄Κ Ιͺα΄ :** `{m.from_user.id}`\n**Stream ΚΙͺΙ΄α΄ :** {og_stream_link}", disable_web_page_preview=True,  quote=True)
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link),
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("π₯ Dα΄α΄‘Ι΄Κα΄α΄α΄ / STREAM π₯", url=stream_link)]]) #Download Link
        )
    except FloodWait as e:
        print(f"Sleeping for {str(e.x)}s")
        await asyncio.sleep(e.x)
        await c.send_message(chat_id=Var.BIN_CHANNEL, text=f"Gα΄α΄ FΚα΄α΄α΄Wα΄Ιͺα΄ α΄? {str(e.x)}s from [{m.from_user.first_name}](tg://user?id={m.from_user.id})\n\n**ππππ πΈπ³ :** `{str(m.from_user.id)}`", disable_web_page_preview=True)


@StreamBot.on_message(filters.channel & ~filters.group & (filters.document | filters.video | filters.photo)  & ~filters.forwarded, group=-1)
async def channel_receive_handler(bot, broadcast):

    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)

        return
    try:
        log_msg = await broadcast.forward(chat_id=Var.BIN_CHANNEL)
        og_stream_link = f"{Var.URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        stream_link = await short_link(og_stream_link)

        og_online_link = f"{Var.URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
        online_link = await short_link(og_online_link) if Var.IS_DISPLAY_DL_LINK else stream_link
        await log_msg.reply_text(
            text=f"**Channel Name:** `{broadcast.chat.title}`\n**CHANNEL ID:** `{broadcast.chat.id}`\n**Rα΄Η«α΄α΄sα΄ α΄ΚΚ:** {og_stream_link}",
            quote=True
        )
        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("π₯STREAM ", url=stream_link),
                     InlineKeyboardButton('Dα΄α΄‘Ι΄Κα΄α΄α΄π₯', url=online_link)] 
                ]
            )
        )
    except FloodWait as w:
        print(f"Sleeping for {str(w.x)}s")
        await asyncio.sleep(w.x)
        await bot.send_message(chat_id=Var.BIN_CHANNEL,
                             text=f"GOT FLOODWAIT OF {str(w.x)}s FROM {broadcast.chat.title}\n\n**CHANNEL ID:** `{str(broadcast.chat.id)}`",
                             disable_web_page_preview=True)
    except Exception as e:
        await bot.send_message(chat_id=Var.BIN_CHANNEL, text=f"**#ERROR_TRACKEBACK:** `{e}`", disable_web_page_preview=True)
        print(f"Cα΄Ι΄'α΄ Eα΄Ιͺα΄ BΚα΄α΄α΄α΄α΄sα΄ Mα΄ssα΄Ι’α΄!\nEΚΚα΄Κ:  **Give me edit permission in updates and bin Channel!{e}**")



async def short_link(link, user=None):
    if not user:
        return link

    # encoded_url = quote(link, safe='/:?=')
    api_key = user.get("shortener_api")
    base_site = user.get("base_site")

    if bool(api_key and base_site) and Var.USERS_CAN_USE:
        shortzy = Shortzy(api_key, base_site)
        link = await shortzy.convert(link)

    return link
