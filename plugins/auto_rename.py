from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper.database import hyoshcoder

@Client.on_message(filters.private & filters.command("autorename"))
async def auto_rename_command(client, message):
    user_id = message.from_user.id

    command_parts = message.text.split("/autorename", 1)
    if len(command_parts) < 2 or not command_parts[1].strip():
        await message.reply_text(
            "**Vᴇᴜɪʟʟᴇᴢ ᴘʀᴏᴠɪᴅᴇʀ ᴜɴ ɴᴏᴜᴠᴇᴀᴜ ɴᴏᴍ ᴀᴘʀès ʟᴀ ᴄᴏᴍᴍᴀɴᴅᴇ /ᴀᴜᴛᴏʀᴇɴᴀᴍᴇ**\n\n"
            "Pour ᴄᴏᴍᴍᴇɴᴄᴇʀ ʟ'ᴜᴛɪʟɪsᴀᴛɪᴏɴ :\n"
            "**Fᴏʀᴍᴀᴛ ᴅ'ᴇxᴀᴍᴘʟᴇ :** `ᴍᴏɴSᴜᴘᴇʀVɪᴅᴇᴏ [episode] [quality]`"
        )
        return

    format_template = command_parts[1].strip()

    await hyoshcoder.set_format_template(user_id, format_template)

    await message.reply_text(
        f"**🌟 Fᴀɴᴛᴀsᴛɪqᴜᴇ! Vᴏᴜs êᴛᴇs ᴘʀêᴛ ᴀ ʀᴇɴᴏᴍᴍᴇʀ ᴀᴜᴛᴏᴍᴀᴛɪqᴜᴇᴍᴇɴᴛ vᴏᴛʀᴇs ꜰɪʟᴇs.**\n\n"
        "📩 Iʟ vᴏᴜs sᴜꜰꜰɪᴛ d'ᴇɴᴠᴏʏᴇʀ ʟᴇs ꜰɪʟᴇs qᴜᴇ vᴏᴜs sᴏᴜʜᴀɪᴛᴇᴢ ʀᴇɴᴏᴍᴍᴇʀ.\n\n"
        f"**Vᴏᴛʀᴇ mᴏᴅèʟᴇ ᴇɴʀᴇɢɪsᴛʀé :** `{format_template}`\n\n"
        "Rappelez-vous, je vais peut-être renommer vos fichiers lentement mais je les rendrai sûrement parfaits!✨"
    )

@Client.on_message(filters.private & filters.command("setmedia"))
async def set_media_command(client, message):
    user_id = message.from_user.id
    
    # Définir les boutons du clavier en ligne
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📁 ᴅᴏᴄᴜᴍᴇɴᴛ", callback_data="setmedia_document")],
        [InlineKeyboardButton("🎥 ᴠɪᴅᴇᴏ", callback_data="setmedia_video")]
    ])
    
    # Envoyer un message avec des boutons en ligne
    await message.reply_text(
        "**Vᴇᴜɪʟʟᴇᴢ sᴇʟᴇᴄᴛɪᴏɴɴᴇʀ ʟᴇ ᴛʏᴘᴇ ᴅᴇ ᴍéᴅɪᴀ qᴜᴇ vᴏᴜs sᴏᴜʜᴀɪᴛᴇᴢ ᴅéғɪɴɪʀ :**",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("^setmedia_"))
async def handle_media_selection(client, callback_query):
    user_id = callback_query.from_user.id
    media_type = callback_query.data.split("_", 1)[1]
    
    # Enregistrer le type de média préféré dans la base de données
    await hyoshcoder.set_media_preference(user_id, media_type)
    
    # Accuser réception du rappel et répondre avec une confirmation
    await callback_query.answer(f"**Pʀéғéʀᴇɴᴄᴇ ᴅᴇ ᴍéᴅɪᴀ déғɪɴɪᴇ sᴜʀ :** {media_type} ✅")
    await callback_query.message.edit_text(f"**Pʀéғéʀᴇɴᴄᴇ ᴅᴇ ᴍéᴅɪᴀ déғɪɴɪᴇ sᴜʀ :** {media_type} ✅")
