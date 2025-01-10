from pyrogram import Client, filters 
from helper.database import hyoshcoder

@Client.on_message(filters.private & filters.command('set_caption'))
async def add_caption(client, message):
    if len(message.command) == 1:
       return await message.reply_text("**Dᴏɴɴᴇᴢ ʟᴀ ʟᴇ́ɢᴇɴᴅᴇ\n\nE𝓍ᴀᴍᴘʟᴇ : `/set_caption 📕Nᴏᴍ ➠ : {filename} \n\n🔗 Tᴀɪʟʟᴇ ➠ : {filesize} \n\n⏰ Dᴜʀᴇ́ᴇ ➠ : {duration}`**")
    caption = message.text.split(" ", 1)[1]
    await hyoshcoder.set_caption(message.from_user.id, caption=caption)
    await message.reply_text("**Vᴏᴛʀᴇ ʟᴇ́ɢᴇɴᴅᴇ ᴀ ᴇᴛᴇ ᴇnregistrᴇr ᴀᴠᴇᴄ sᴜᴄᴄᴇ̀s ✅**")

@Client.on_message(filters.private & filters.command('del_caption'))
async def delete_caption(client, message):
    caption = await hyoshcoder.get_caption(message.from_user.id)  
    if not caption:
       return await message.reply_text("**Vᴏᴜs n'ᴀᴠᴇᴢ ᴀᴜᴄᴜᴍᴇ ʟᴇ́ɢᴇɴᴅᴇ ❌**")
    await hyoshcoder.set_caption(message.from_user.id, caption=None)
    await message.reply_text("**Vᴏᴛʀᴇ ʟᴇ́ɢᴇɴᴅᴇ ᴀ ᴇᴛᴇ sᴜᴘᴘʀɪᴍᴇ́ᴇ ᴀᴠᴇᴄ sᴜᴄᴄᴇ̀s 🗑️**")

@Client.on_message(filters.private & filters.command(['see_caption', 'view_caption']))
async def see_caption(client, message):
    caption = await hyoshcoder.get_caption(message.from_user.id)  
    if caption:
       await message.reply_text(f"**Vᴏᴛʀᴇ ʟᴇ́ɢᴇɴᴅᴇ :**\n\n`{caption}`")
    else:
       await message.reply_text("**Vᴏᴜs n'ᴀᴠᴇᴢ ᴀᴜᴄᴜᴍᴇ ʟᴇ́ɢᴇɴᴅᴇ ❌**")

@Client.on_message(filters.private & filters.command(['view_thumb', 'viewthumb']))
async def viewthumb(client, message):    
    thumb = await hyoshcoder.get_thumbnail(message.from_user.id)
    if thumb:
       await client.send_photo(chat_id=message.chat.id, photo=thumb)
    else:
        await message.reply_text("**Vᴏᴜs n'ᴀᴠᴇᴢ ᴀᴜᴄᴜᴍᴇ ᴍɪɴɪᴀᴛᴜʀᴇ ❌**") 

@Client.on_message(filters.private & filters.command(['del_thumb', 'delthumb']))
async def removethumb(client, message):
    await hyoshcoder.set_thumbnail(message.from_user.id, file_id=None)
    await message.reply_text("**ᴍɪɴɪᴀᴛᴜʀᴇ sᴜᴘᴘʀɪᴍᴇ́ᴇ ᴀᴠᴇᴄ sᴜᴄᴄᴇ̀s 🗑️**")

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    mkn = await message.reply_text("Vᴇᴜɪʟʟᴇᴢ ᴘᴀᴛɪᴇɴᴛᴇʀ ...")
    await hyoshcoder.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await mkn.edit("**ᴍɪɴɪᴀᴛᴜʀᴇ ᴇɴʀᴇɢɪsᴛʀᴇ́ᴇ ᴀᴠᴇᴄ sᴜᴄᴄᴇ̀s ✅️**")
