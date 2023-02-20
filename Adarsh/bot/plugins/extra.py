from Adarsh.bot import StreamBot
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import shutil, psutil
from Adarsh.vars import Var
from utils_bot import *
from Adarsh import StartTime


START_TEXT = """ Your Telegram DC Is : `{}`  """


         


@StreamBot.on_message(filters.regex("DC"))
async def start(bot, update):
    if update.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return
    
    text = START_TEXT.format(update.from_user.dc_id)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        quote=True
    )

    
    
@StreamBot.on_message(filters.command("list"))
async def list(l, m):
    if m.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return

    LIST_MSG = "Hi! {} Here is a list of all my commands \n \n1 . `start⚡️` \n2. `help📚` \n3. `status📊`\n4. `ping` "
    await l.send_message(chat_id = m.chat.id,
        text = LIST_MSG.format(m.from_user.mention(style="md"))
        
    )
    
    
@StreamBot.on_message(filters.regex("ping📡"))
async def ping(b, m):
    if m.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return
    start_t = time.time()
    ag = await m.reply_text("....")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await ag.edit(f"Pong!\n{time_taken_s:.3f} ms")
    
    
    
    
@StreamBot.on_message(filters.private & filters.regex("status📊"))
async def stats(bot, update):
    if update.from_user.id not in Var.ADMINS and not Var.USERS_CAN_USE:
        return
    
    currentTime = readable_time((time.time() - StartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    botstats = f'<b>Bot Uptime:</b> {currentTime}\n' \
                f'<b>Total disk space:</b> {total}\n' \
                f'<b>Used:</b> {used}  ' \
                f'<b>Free:</b> {free}\n\n' \
                f'📊Data Usage📊\n<b>Upload:</b> {sent}\n' \
                f'<b>Down:</b> {recv}\n\n' \
                f'<b>CPU:</b> {cpuUsage}% ' \
                f'<b>RAM:</b> {memory}% ' \
                f'<b>Disk:</b> {disk}%'
    await update.reply_text(botstats)
