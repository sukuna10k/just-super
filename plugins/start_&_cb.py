import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from helper.database import hyoshcoder
from config import *
from config import Config

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message: Message):
    user = message.from_user
    await hyoshcoder.add_user(client, message)

    m = await message.reply_text("ᴏɴᴇᴇ-ᴄʜᴀɴ ! ᴄᴏᴍᴍᴇɴᴛ ᴠᴀs-ᴛᴜ ? \nᴀᴛᴛᴇɴᴅs ᴜɴ ɪɴsᴛᴀɴᴛ...")
    await asyncio.sleep(0.9)
    await m.edit_text("👀")
    await asyncio.sleep(0.5)
    await m.edit_text("⚡")
    await asyncio.sleep(0.5)
    await m.edit_text("Bʏᴀᴋᴜɢᴀɴ...")
    await asyncio.sleep(0.4)
    await m.delete()

    m =await  message.reply_sticker("CAACAgIAAxkBAALmzGXSSt3ppnOsSl_spnAP8wHC26jpAAJEGQACCOHZSVKp6_XqghKoHgQ")
    await asyncio.sleep(0.4)
    await m.delete()

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("• ᴍᴇs ᴄᴏᴍᴍᴀɴᴅᴇs •", callback_data='help')
        ],
        [
            InlineKeyboardButton('• ᴍɪsᴇs à ᴊᴏᴜʀ', url='https://t.me/hyoshassistantbot'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/tout_manga_confondu')
        ],
        [
            InlineKeyboardButton('• ᴀ ᴘʀᴏᴘᴏs', callback_data='about'),
            InlineKeyboardButton('sᴏᴜʀᴄᴇ •', callback_data='source')
        ]
    ])


    # Send start message with or without picture
    if Config.START_PIC:
        await message.reply_photo(
            Config.START_PIC,
            caption=Txt.START_TXT.format(user.mention),
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=Txt.START_TXT.format(user.mention),
            reply_markup=buttons,
            disable_web_page_preview=True
        )


# Callback Query Handler
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    print(f"Callback data received: {data}")  # Debugging line

    if data == "home":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("•  ᴍᴇs ᴄᴏᴍᴍᴀɴᴅᴇs  •", callback_data='help')],
                [InlineKeyboardButton('• ᴍɪsᴇs à ᴊᴏᴜʀ', url='https://t.me/hyoshassistantbot'), InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url='https://t.me/tout_manga_confondu')],
                [InlineKeyboardButton('• ᴀ ᴘʀᴏᴘᴏs', callback_data='about'), InlineKeyboardButton('sᴏᴜʀᴄᴇ •', callback_data='source')]
            ])
        )
    elif data == "caption":
        await query.message.edit_text(
            text=Txt.CAPTION_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ", url='https://t.me/tout_manga_confondu'), InlineKeyboardButton("ʀᴇᴛᴏᴜʀ •", callback_data="help")]
            ])
        )

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("• ғᴏʀᴍᴀᴛ ᴅᴇ ʀᴇɴᴏᴍᴍᴀɢᴇ ᴀᴜᴛᴏᴍᴀᴛɪǫᴜᴇ •", callback_data='file_names')],
                            [InlineKeyboardButton('• ᴠɪɢɴᴇᴛᴛᴇ', callback_data='thumbnail'), InlineKeyboardButton('ʟᴇ́ɢᴇɴᴅᴇ •', callback_data='caption')],
                            [InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴏɴɴᴇ́ᴇs', callback_data='meta'), InlineKeyboardButton('ғᴀɪʀᴇ ᴜɴ ᴅᴏɴ •', callback_data='donate')],
                            [InlineKeyboardButton('• ᴀᴄᴄᴜᴇɪʟ', callback_data='home')]
                        ])

        )

    elif data == "meta":
        await query.message.edit_text(  # Change edit_caption to edit_text
            text=Txt.SEND_METADATA,  # Changed from caption to text
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ғᴇʀᴍᴇʀ", callback_data="close"), InlineKeyboardButton("ʀᴇᴛᴏᴜʀ •", callback_data="help")]
            ])
        )
    elif data == "donate":
        await query.message.edit_text(
            text=Txt.DONATE_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ʀᴇᴛᴏᴜʀ", callback_data="help"), InlineKeyboardButton("ᴘʀᴏᴘʀɪᴇᴛᴀɪʀᴇ •", url='https://t.me/hyoshassistantBot')]
            ])
        )
    elif data == "file_names":
        format_template = await hyoshcoder.get_format_template(user_id)
        await query.message.edit_text(
            text=Txt.FILE_NAME_TXT.format(format_template=format_template),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ғᴇʀᴍᴇʀ", callback_data="close"), InlineKeyboardButton("ʀᴇᴛᴏᴜʀ •", callback_data="help")]
            ])
        )
    elif data == "thumbnail":
        await query.message.edit_caption(
            caption=Txt.THUMBNAIL_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ғᴇʀᴍᴇʀ", callback_data="close"), InlineKeyboardButton("ʀᴇᴛᴏᴜʀ •", callback_data="help")]
            ])
        )
    elif data == "metadatax":
        await query.message.edit_caption(
            caption=Txt.SEND_METADATA,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ғᴇʀᴍᴇʀ", callback_data="close"), InlineKeyboardButton("ʀᴇᴛᴏᴜʀ •", callback_data="help")]
            ])
        )
    elif data == "source":
        await query.message.edit_caption(
            caption=Txt.SOURCE_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ғᴇʀᴍᴇʀ", callback_data="close"), InlineKeyboardButton("ʀᴇᴛᴏᴜʀ •", callback_data="home")]
            ])
        )
    elif data == "premiumx":
        await query.message.edit_caption(
            caption=Txt.PREMIUM_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ʀᴇᴛᴏᴜʀ", callback_data="help"), InlineKeyboardButton("ᴀᴄʜᴇᴛᴇʀ ᴘʀᴇᴍɪᴜᴍ •", url='https://t.me/hyoshassistantBot')]
            ])
        )
    elif data == "plans":
        await query.message.edit_caption(
            caption=Txt.PREPLANS_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• ғᴇʀᴍᴇʀ", callback_data="close"), InlineKeyboardButton("ᴀᴄʜᴇᴛᴇʀ ᴘʀᴇᴍɪᴜᴍ •", url='https://t.me/hyoshassistantBot')]
            ])
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ", url='https://t.me/tout_manga_confondu'), InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅᴇs •", callback_data="help")],
                [InlineKeyboardButton("• ᴅᴇᴠᴇʟᴏᴘᴇʀ", url='https://t.me/hyoshassistantbot'), InlineKeyboardButton("ɴᴇᴛᴡᴏʀᴋ •", url='https://t.me/tout_manga_confondu')],
                [InlineKeyboardButton("• ʀᴇᴛᴏᴜʀ •", callback_data="home")]
            ])
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()

# Donation Command Handler
@Client.on_message(filters.command("donate"))
async def donation(client, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="ʀᴇᴛᴏᴜʀ", callback_data="help"), InlineKeyboardButton(text="ᴘʀᴏᴘʀɪᴇᴛᴀɪʀᴇ", url='https://t.me/hyoshassistantBot')]
    ])
    yt = await message.reply_photo(photo='img/2.jpg', caption=Txt.DONATE_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Premium Command Handler
@Client.on_message(filters.command("premium"))
async def getpremium(bot, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴘʀᴏᴘʀɪᴇᴛᴀɪʀᴇ", url="https://t.me/hyoshassistantBot"), InlineKeyboardButton("ғᴇʀᴍᴇʀ", callback_data="close")]
    ])
    yt = await message.reply_photo(photo='img/1.jpg', caption=Txt.PREMIUM_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Plan Command Handler
@Client.on_message(filters.command("plan"))
async def premium(bot, message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("ᴘᴀʏᴇʀ ᴠᴏᴛʀᴇ ᴀʙᴏɴɴᴇᴍᴇɴᴛ", url="https://t.me/hyoshassistantBot"), InlineKeyboardButton("ғᴇʀᴍᴇʀ", callback_data="close")]
    ])
    yt = await message.reply_photo(photo='img/2.jpg', caption=Txt.PREPLANS_TXT, reply_markup=buttons)
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()

# Bought Command Handler
@Client.on_message(filters.command("bought") & filters.private)
async def bought(client, message):
    msg = await message.reply('ᴀᴛᴛᴇɴᴅ, ᴊᴇ ᴠᴇʀɪғɪᴇ...')
    replied = message.reply_to_message

    if not replied:
        await msg.edit("<b>ᴠᴇᴜɪʟʟᴇᴢ ʀᴇᴘᴏɴᴅʀᴇ ᴀᴠᴇᴄ ʟᴀ ᴄᴀᴘᴛᴜʀᴇ ᴅ'ᴇ́cran ᴅᴇ ᴠᴏᴛʀᴇ ᴘᴀʏᴇᴍᴇɴᴛ ᴘᴏᴜʀ ʟ'ᴀᴄʜᴀᴛ ᴘʀᴇᴍɪᴜᴍ ᴘᴏᴜʀ ᴄᴏɴᴛɪɴᴜᴇʀ.\n\nᴘᴀʀ ᴇxᴀᴍᴘʟᴇ, ᴛᴇ́ʟᴇᴄʜᴀʀɢᴇᴢ ᴅ'ᴀʙᴏʀᴅ ᴠᴏᴛʀᴇ ᴄᴀᴘᴛᴜʀᴇ ᴅ'ᴇ́cran, ᴘᴜɪs ʀᴇᴘᴏɴᴅʀᴇ ᴀᴠᴇᴄ ʟᴀ ᴄᴏᴍᴍᴀɴᴅᴇ '/bought</b>")
    elif replied.photo:
        await client.send_photo(
            chat_id=Config.LOG_CHANNEL,
            photo=replied.photo.file_id,
            caption=f'<b>ᴜᴛɪʟɪsᴀᴛᴇᴜʀ - {message.from_user.mention}\nɪᴅ ᴜᴛɪʟɪsᴀᴛᴇᴜʀ - <code>{message.from_user.id}</code>\nɴᴏᴍ ᴜᴛɪʟɪsᴀᴛᴇᴜʀ - <code>{message.from_user.username}</code>\nᴘʀᴇɴᴏᴍ - <code>{message.from_user.first_name}</code></b>',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Close", callback_data="close_data")]
            ])
        )
        await msg.edit_text('<b>Vᴏᴛʀᴇ ᴄᴀᴘᴛᴜʀᴇ ᴅ\'ᴇ́ᴛᴏɪʟᴇ ᴀ ᴇᴛᴇ ᴇɴᴠᴏʏᴇ́ᴇ ᴀᴜx ᴀᴅᴍɪɴs</b>')

@Client.on_message(filters.private & filters.command("help"))
async def help_command(client, message):
    # Await get_me to get the bot's user object
    bot = await client.get_me()
    mention = bot.mention

    # Send the help message with inline buttons
    await message.reply_text(
        text=Txt.HELP_TXT.format(mention=mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("• ғᴏʀᴍᴀᴛ ᴅᴇ ʀᴇɴᴏᴍᴍᴀɢᴇ ᴀᴜᴛᴏᴍᴀᴛɪǫᴜᴇ •", callback_data='file_names')],
            [InlineKeyboardButton('• ᴠɪɢɴᴇᴛᴛᴇ', callback_data='thumbnail'), InlineKeyboardButton('ʟᴇ́ɢᴇɴᴅᴇ •', callback_data='caption')],
            [InlineKeyboardButton('• ᴍᴇᴛᴀᴅᴏɴɴᴇ́ᴇs', callback_data='meta'), InlineKeyboardButton('ғᴀɪʀᴇ ᴜɴ ᴅᴏɴ •', callback_data='donate')],
            [InlineKeyboardButton('• ᴀᴄᴄᴜᴇɪʟ', callback_data='home')]
        ])
    )
