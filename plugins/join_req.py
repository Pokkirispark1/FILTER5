from utils import temp
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
from database.fsubdb import fsub_db
from Script import script
from info import *
from database.ia_filterdb import get_file_details
from utils import get_settings, get_size
import asyncio

@Client.on_chat_join_request()
async def join_reqs(client, join_req):
    user_id = join_req.from_user.id
    channel_id = await fsub_db.get_rfsub_id()  
    if join_req.chat.id != int(channel_id):
        return
        
    join_count = await fsub_db.add_join_req(user_id)
    if await fsub_db.check_rfsub_limit():
        join_count = await fsub_db.get_join_count()
        limit = await fsub_db.get_rfsub_limit()
        limit_text = f"{join_count} of members" if limit else ""
        await client.send_message(RFSUB_NOTIFICATION, f"<b>Fsᴜʙ Wᴏʀᴋ Cᴏᴍᴘʟᴇᴛᴇᴅ ✅</b>\n<b>Rᴇǫᴜᴇsᴛs ᴀᴅᴅᴇᴅ ➡️</b>{limit_text}\n<b>Cʜᴀɴɴᴇʟ ➡️</b> : <code>{channel_id}</code>\n\n<b>Fsᴜʙ sʜɪғᴛᴇᴅ ᴛᴏ ᴅᴇғᴀᴜʟᴛ ᴄʜᴀɴɴᴇʟ</b>") 
        await client.send_sticker(RFSUB_NOTIFICATION, "CAACAgUAAxkBAAEO3WdoagEzQBPp9KB5TiIV9-rt-7qF_QACcQoAAmBffQVBn0D_9WK7hTYE")
        try:
            await client.send_message(channel_id, f"Fsᴜʙ Wᴏʀᴋ Cᴏᴍᴘʟᴇᴛᴇᴅ ✅</b>\n<b>Rᴇǫᴜᴇsᴛs ᴀᴅᴅᴇᴅ ➡️</b>{limit_text}\n<b>Cʜᴀɴɴᴇʟ ➡️</b> : <code>{channel_id}</code>\n\n<b>Fsᴜʙ sʜɪғᴛᴇᴅ ᴛᴏ ᴅᴇғᴀᴜʟᴛ ᴄʜᴀɴɴᴇʟ</b>")
        except Exception as e:
            await client.send_message(LOG_CHANNEL, f"Failed to notify fsub channel {channel_id}: {e}")
    
    if str(user_id) in temp.AUTO_ACCEPT:
        file_id = temp.AUTO_ACCEPT[str(user_id)]['file_id']
        grp_id = temp.AUTO_ACCEPT[str(user_id)]['grp_id']
        mode = temp.AUTO_ACCEPT[str(user_id)]['mode']
        try:
            files_ = await get_file_details(file_id)
            if not files_:
                await client.send_message(user_id, '<b>⚠️ ꜰɪʟᴇ ɴᴏᴛ ꜰᴏᴜɴᴅ ⚠️</b>')
                return
            files = files_[0]
            settings = await get_settings(int(grp_id))
            CAPTION = settings.get('caption', '')
            f_caption = CAPTION.format(
                file_name=files.file_name,
                file_size=get_size(files.file_size),
                file_caption=files.caption or ""
            )
            msg = await client.send_cached_media(
                chat_id=user_id,
                file_id=file_id,
                caption=f_caption,
                protect_content=settings.get('file_secure', False),
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🍿", url="https://t.me/+yRGybUMudhwzNGZk"),
                        InlineKeyboardButton("📺", url="https://t.me/+LsV_DaUHn0swNTVl"),
                        InlineKeyboardButton("🎭", url="https://t.me/+wPZhy7fVG5BlODU1"),
                        InlineKeyboardButton("🔞", url="https://t.me/+IsOm9la9LpMzOTM1")
                    ],[
                        InlineKeyboardButton("Gʀᴏᴜᴘ 🥇", url="https://t.me/+Vw364TMZTkpjNWVl"),
                        InlineKeyboardButton("Gʀᴏᴜᴘ 🥈", url="https://t.me/+NYDsPNzuu_thZGRl")
                    ]
                ])
            )
            # Clean up
            del temp.AUTO_ACCEPT[str(user_id)]
        except Exception as e:
            await client.send_message(user_id, f"Error sending file: {e}")

@Client.on_message(filters.command("delete_requests") & filters.private & filters.user(ADMINS))
async def delete_requests(client, message):
    await fsub_db.del_join_req()
    await message.reply("<b>⚙ Successfully deleted all channel join requests</b>")
