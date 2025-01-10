import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from helper.database import hyoshcoder
from config import Txt, Config

# AUTH_USERS = Config.AUTH_USERS

ON = [[InlineKeyboardButton('mᴇ́tᴀᴅᴏɴᴇᴇs ᴀᴄᴛɪᴠᴇ́ᴇs', callback_data='metadata_1'),
       InlineKeyboardButton('✅', callback_data='metadata_1')],
      [InlineKeyboardButton('Dᴇ́fɪɴɪʀ ᴅᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴘᴇʀsᴏɴɴᴀʟɪsᴇ́ᴇs', callback_data='custom_metadata')]]

OFF = [[InlineKeyboardButton('mᴇ́tᴀᴅᴏɴᴇᴇs ᴅᴇ́sᴀᴄᴛɪᴠᴇ́ᴇs', callback_data='metadata_0'),
        InlineKeyboardButton('❌', callback_data='metadata_0')],
       [InlineKeyboardButton('Dᴇ́fɪɴɪʀ ᴅᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴘᴇʀsᴏɴɴᴀʟɪsᴇ́ᴇs', callback_data='custom_metadata')]]


@Client.on_message(filters.private & filters.command("metadata"))
async def handle_metadata(bot: Client, message: Message):
    ms = await message.reply_text("**Vᴇᴜɪʟʟᴇᴢ ᴘᴀᴛɪᴇɴᴛᴇʀ...**", reply_to_message_id=message.id)
    bool_metadata = await hyoshcoder.get_metadata(message.from_user.id)
    user_metadata = await hyoshcoder.get_metadata_code(message.from_user.id)
    await ms.delete()
    
    if bool_metadata:
        await message.reply_text(
            f"<b>Vᴏᴛʀᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴀᴄᴛᴜᴇʟʟᴇs :</b>\n\n➜ {user_metadata} ",
            reply_markup=InlineKeyboardMarkup(ON),
        )
    else:
        await message.reply_text(
            f"<b>Vᴏᴛʀᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴀᴄᴛᴜᴇʟʟᴇs :</b>\n\n➜ {user_metadata} ",
            reply_markup=InlineKeyboardMarkup(OFF),
        )


@Client.on_callback_query(filters.regex(".*?(custom_metadata|metadata).*?"))
async def query_metadata(bot: Client, query: CallbackQuery):
    data = query.data

    if data.startswith("metadata_"):
        _bool = data.split("_")[1] == '1'
        user_metadata = await hyoshcoder.get_metadata_code(query.from_user.id)

        if _bool:
            await hyoshcoder.set_metadata(query.from_user.id, bool_meta=False)
            await query.message.edit(
                f"<b>Vᴏᴛʀᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴀᴄᴛᴜᴇʟʟᴇs :</b>\n\n➜ {user_metadata} ",
                reply_markup=InlineKeyboardMarkup(OFF),
            )
        else:
            await hyoshcoder.set_metadata(query.from_user.id, bool_meta=True)
            await query.message.edit(
                f"<b>Vᴏᴛʀᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴀᴄᴛᴜᴇʟʟᴇs :</b>\n\n➜ {user_metadata} ",
                reply_markup=InlineKeyboardMarkup(ON),
            )

    elif data == "custom_metadata":
        await query.message.delete()
        try:
            user_metadata = await hyoshcoder.get_metadata_code(query.from_user.id)
            metadata_message = f"""
<b>--Pᴀʀᴀᴍᴇᴛʀᴇs ᴅᴇs mᴇ́tᴀᴅᴏɴᴇᴇs:--</b>

➜ <b>mᴇ́tᴀᴅᴏɴᴇᴇs ᴀᴄᴛᴜᴇʟʟᴇs :</b> {user_metadata}

<b>Dᴇ́sᴄʀɪᴘᴛɪᴏɴ</b> : Lᴇs mᴇ́tᴀᴅᴏɴᴇᴇs vᴏɴᴛ mᴏdɪꜰɪᴇʀ ʟᴇs fɪʟᴇs vɪᴅᴇᴏ MKV, ʏ ɪɴclᴜᴇɴs tᴏᴜᴛs ʟᴇs tɪᴛʀᴇs ᴀᴜᴅɪᴏ, sᴛʀᴇᴀᴍs ᴇᴛ sᴜʙᴛɪᴛʀᴇs.

<b>➲ Eɴvᴏʏᴇᴢ ʟᴇ tɪᴛʀᴇ ᴅᴇs mᴇ́tᴀᴅᴏɴᴇᴇs. Dᴇ́ʟᴀɪ : 60 sᴇc</b>
"""

            metadata = await bot.ask(
                text=metadata_message,
                chat_id=query.from_user.id,
                filters=filters.text,
                timeout=60,
                disable_web_page_preview=True,
            )
        except asyncio.TimeoutError:
            await bot.send_message(
                chat_id=query.from_user.id,
                text="⚠️ Eʀʀᴇᴜʀ !!\n\n**Lᴀ dᴇᴍᴀɴᴅᴇ ᴀ ᴇxᴘɪʀᴇ́ᴇ.**\nRᴇ́dᴇᴍᴀʀʀᴇᴢ ᴇɴ ᴜtilisant /metadata",
            )
            return
        
        try:
            ms = await bot.send_message(
                chat_id=query.from_user.id,
                text="**Vᴇᴜɪʟʟᴇᴢ ᴘᴀᴛɪᴇɴᴛᴇʀ...**",
                reply_to_message_id=query.message.id,
            )
            await hyoshcoder.set_metadata_code(
                query.from_user.id, metadata_code=metadata.text
            )
            await ms.edit("**Vᴏᴛʀᴇ cᴏᴅᴇ ᴅᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴀ ᴇᴛᴇ ᴅᴇ́fɪɴɪ ᴀᴠᴇᴄ sᴜᴄᴄᴇ̀s ✅**")
        except Exception as e:
            await bot.send_message(
                chat_id=query.from_user.id,
                text=f"**Uɴᴇ ᴇʀʀᴇᴜʀ ᴇsᴛ sᴜʀᴠᴇᴜ :** {str(e)}",
            )
