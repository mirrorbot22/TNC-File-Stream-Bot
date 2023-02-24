import jinja2
from Adarsh.vars import Var
from Adarsh.bot import StreamBot
from Adarsh.utils.human_readable import humanbytes
from Adarsh.utils.file_properties import get_file_ids
from Adarsh.server.exceptions import InvalidHash
import urllib.parse
import logging
import aiohttp
from urllib.parse import quote_plus

async def render_page(id, secure_hash, src=None):
    file_data = await get_file_ids(StreamBot, int(Var.BIN_CHANNEL), int(id))
    if file_data.unique_id[:6] != secure_hash:
        logging.debug(f'link hash: {secure_hash} - {file_data.unique_id[:6]}')
        logging.debug(f"Invalid hash for message with - ID {id}")
        raise InvalidHash
  

    src = urllib.parse.urljoin(Var.URL, f'{id}/{quote_plus(file_data.file_name)}?hash={secure_hash}')

    tag = file_data.mime_type.split('/')[0].strip()
    file_size = humanbytes(file_data.file_size)
    if tag == 'video':
        template_file = 'Adarsh/template/req.html'
        heading = f'Watch {file_data.file_name}'
    elif tag == 'audio':
        template_file = 'Adarsh/template/req.html'
        heading = f'Listen {file_data.file_name}'
    else:
        template_file = 'Adarsh/template/dl.html'
        heading = f'Download {file_data.file_name}'
        async with aiohttp.ClientSession() as s:
            async with s.get(src) as u:
                file_size = humanbytes(int(u.headers.get('Content-Length')))

    with open(template_file) as f:
        template = jinja2.Template(f.read())

    file_name = file_data.file_name.replace("_", " ")
    return template.render(
        heading=heading, 
        filename=file_name, 
        src=src, 
        file_size=file_size, 
        bot_usename=Var.BOT_USERNAME,
        ad1=Var.AD1, 
        ad2=Var.AD2, 
        ad3=Var.AD3, 
        ad4=Var.AD4,
        ad5=Var.AD5,
        video_ad=Var.VIDEO_AD,
        ad6=Var.AD6
        )