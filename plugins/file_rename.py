from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message
from PIL import Image
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, humanbytes, convert
from helper.database import hyoshcoder
from config import Config
import os
import time
import re
import subprocess
import asyncio

renaming_operations = {}

# Pattern 1: S01E02 or S01EP02
pattern1 = re.compile(r'S(\d+)(?:E|EP)(\d+)')
# Pattern 2: S01 E02 or S01 EP02 or S01 - E01 or S01 - EP02
pattern2 = re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)(\d+)')
# Pattern 3: Episode Number After "E" or "EP"
pattern3 = re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)')
# Pattern 3_2: episode number after - [hyphen]
pattern3_2 = re.compile(r'(?:\s*-\s*(\d+)\s*)')
# Pattern 4: S2 09 ex.
pattern4 = re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE)
# Pattern X: Standalone Episode Number
patternX = re.compile(r'(\d+)')
#QUALITY PATTERNS 
# Pattern 5: 3-4 digits before 'p' as quality
pattern5 = re.compile(r'\b(?:.*?(\d{3,4}[^\dp]*p).*?|.*?(\d{3,4}p))\b', re.IGNORECASE)
# Pattern 6: Find 4k in brackets or parentheses
pattern6 = re.compile(r'[([<{]?\s*4k\s*[)\]>}]?', re.IGNORECASE)
# Pattern 7: Find 2k in brackets or parentheses
pattern7 = re.compile(r'[([<{]?\s*2k\s*[)\]>}]?', re.IGNORECASE)
# Pattern 8: Find HdRip without spaces
pattern8 = re.compile(r'[([<{]?\s*HdRip\s*[)\]>}]?|\bHdRip\b', re.IGNORECASE)
# Pattern 9: Find 4kX264 in brackets or parentheses
pattern9 = re.compile(r'[([<{]?\s*4kX264\s*[)\]>}]?', re.IGNORECASE)
# Pattern 10: Find 4kx265 in brackets or parentheses
pattern10 = re.compile(r'[([<{]?\s*4kx265\s*[)\]>}]?', re.IGNORECASE)
pattern11 = re.compile(r'[([<{]?\s*UHD\s*[)\]>}]?', re.IGNORECASE)
pattern12 = re.compile(r'[([<{]?\s*HD\s*[)\]>}]?', re.IGNORECASE)
pattern13 = re.compile(r'[([<{]?\s*SD\s*[)\]>}]?', re.IGNORECASE)
pattern14 = re.compile(r'[([<{]?\s*convertie\s*[)\]>}]?', re.IGNORECASE)
pattern15 = re.compile(r'[([<{]?\s*converti\s*[)\]>}]?', re.IGNORECASE)
pattern16 = re.compile(r'[([<{]?\s*convertis\s*[)\]>}]?', re.IGNORECASE)

def extract_quality(filename):
    # Try Quality Patterns
    match5 = re.search(pattern5, filename)
    if match5:
        print("Matched Pattern 5")
        quality5 = match5.group(1) or match5.group(2)  # Extracted quality from both patterns
        print(f"Quality: {quality5}")
        return quality5

    match6 = re.search(pattern6, filename)
    if match6:
        print("Matched Pattern 6")
        quality6 = "4k"
        print(f"Quality: {quality6}")
        return quality6

    match7 = re.search(pattern7, filename)
    if match7:
        print("Matched Pattern 7")
        quality7 = "2k"
        print(f"Quality: {quality7}")
        return quality7

    match8 = re.search(pattern8, filename)
    if match8:
        print("Matched Pattern 8")
        quality8 = "HdRip"
        print(f"Quality: {quality8}")
        return quality8

    match9 = re.search(pattern9, filename)
    if match9:
        print("Matched Pattern 9")
        quality9 = "4kX264"
        print(f"Quality: {quality9}")
        return quality9

    match10 = re.search(pattern10, filename)
    if match10:
        print("Matched Pattern 10")
        quality10 = "4kx265"
        print(f"Quality: {quality10}")
        return quality10 
    
    match11 = re.search(pattern11, filename)
    if match11:
        print("Matched Pattern 11")
        quality11 = "UHD"
        print(f"Quality: {quality11}")
        return quality11
    
    match12 = re.search(pattern12, filename)
    if match12:
        print("Matched Pattern 12")
        quality12 = "HD"
        print(f"Quality: {quality12}")
        return quality12
    
    match13 = re.search(pattern13, filename)
    if match13:
        print("Matched Pattern 13")
        quality13 = "SD"
        print(f"Quality: {quality13}")
        return quality13
    
    match14 = re.search(pattern14, filename)
    if match14:
        print("Matched Pattern 14")
        quality14 = "convertie"
        print(f"Quality: {quality14}")
        return quality14
    
    match15 = re.search(pattern15, filename)
    if match15:
        print("Matched Pattern 15")
        quality15 = "convertie"
        print(f"Quality: {quality15}")
        return quality15
    
    match16 = re.search(pattern16, filename)
    if match16:
        print("Matched Pattern 16")
        quality16 = "convertie"
        print(f"Quality: {quality16}")
        return quality16

    # Return "Unknown" if no pattern matches
    unknown_quality = "Unknown"
    print(f"Quality: {unknown_quality}")
    return unknown_quality
    

def extract_episode_number(filename):    
    # Try Pattern 1
    match = re.search(pattern1, filename)
    if match:
        print("Matched Pattern 1")
        return match.group(2)  # Extracted episode number
    
    # Try Pattern 2
    match = re.search(pattern2, filename)
    if match:
        print("Matched Pattern 2")
        return match.group(2)  # Extracted episode number

    # Try Pattern 3
    match = re.search(pattern3, filename)
    if match:
        print("Matched Pattern 3")
        return match.group(1)  # Extracted episode number

    # Try Pattern 3_2
    match = re.search(pattern3_2, filename)
    if match:
        print("Matched Pattern 3_2")
        return match.group(1)  # Extracted episode number
        
    # Try Pattern 4
    match = re.search(pattern4, filename)
    if match:
        print("Matched Pattern 4")
        return match.group(2)  # Extracted episode number

    # Try Pattern X
    match = re.search(patternX, filename)
    if match:
        print("Matched Pattern X")
        return match.group(1)  # Extracted episode number
        
    # Return None if no pattern matches
    return None

# Example Usage:
filename = "Naruto Shippuden S01 - EP07 - convertie [Dual Audio] @hyoshassistantbot.mkv"
episode_number = extract_episode_number(filename)
episode_quality = extract_quality(filename)
print(f"Extracted Episode Number: {episode_number} and Quality: {episode_quality}")


@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def auto_rename_files(client, message):
    user_id = message.from_user.id
    format_template = await hyoshcoder.get_format_template(user_id)
    media_preference = await hyoshcoder.get_media_preference(user_id)

    if not format_template:
        return await message.reply_text(
            "ᴠᴇᴜɪʟʟᴇᴢ ᴅ'ᴀʙᴏʀᴅ ᴅᴇ́ғɪɴɪʀ ᴜɴ ғᴏʀᴍᴀᴛ ᴅᴇ ʀᴇɴᴏᴍᴍᴀɢᴇ ᴀᴜᴛᴏᴍᴀᴛɪǫᴜᴇ ᴇɴ ᴜᴛɪʟɪsᴀɴᴛ //autorename"
        )

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        media_type = media_preference or "document"
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_name}.mp4"
        media_type = media_preference or "video"
    elif message.audio:
        file_id = message.audio.file_id
        file_name = f"{message.audio.file_name}.mp3"
        media_type = media_preference or "audio"
    else:
        return await message.reply_text("Unsupported File Type")

    if file_id in renaming_operations:
        elapsed_time = (datetime.now() - renaming_operations[file_id]).seconds
        if elapsed_time < 10:
            return

    renaming_operations[file_id] = datetime.now()

    episode_number = extract_episode_number(file_name)
    if episode_number:
        placeholders = ["episode", "Episode", "EPISODE", "{episode}"]
        for placeholder in placeholders:
            format_template = format_template.replace(placeholder, str(episode_number), 1)

        # Add extracted qualities to the format template
        quality_placeholders = ["quality", "Quality", "QUALITY", "{quality}"]
        for quality_placeholder in quality_placeholders:
            if quality_placeholder in format_template:
                extracted_qualities = extract_quality(file_name)
                if extracted_qualities == "Unknown":
                    await message.reply_text("**ᴊᴇ ɴ'ᴀɪ ᴘᴀs ᴘᴜ ᴇxᴛʀᴀɪʀᴇ ʟᴀ ǫᴜᴀʟɪᴛᴇ́ ᴄᴏʀʀᴇᴄᴛᴇᴍᴇɴᴛ. ʀᴇɴᴏᴍᴍᴀɢᴇ ᴇɴ 'Unknown'...**")
                    # Mark the file as ignored
                    del renaming_operations[file_id]
                    return  # Exit the handler if quality extraction fails
                
                format_template = format_template.replace(quality_placeholder, "".join(extracted_qualities))

    _, file_extension = os.path.splitext(file_name)
    renamed_file_name = f"{format_template}{file_extension}"
    renamed_file_path = f"downloads/{renamed_file_name}"
    metadata_file_path = f"Metadata/{renamed_file_name}"
    os.makedirs(os.path.dirname(renamed_file_path), exist_ok=True)
    os.makedirs(os.path.dirname(metadata_file_path), exist_ok=True)

    download_msg = await message.reply_text("**__ᴛᴇʟᴇ́ᴄʜᴀʀɢᴇᴍᴇɴᴛ...__**")

    try:
        path = await client.download_media(
            message,
            file_name=renamed_file_path,
            progress=progress_for_pyrogram,
            progress_args=("ᴛᴇʟᴇ́ᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀs...", download_msg, time.time()),
        )
    except Exception as e:
        del renaming_operations[file_id]
        return await download_msg.edit(f"**ᴇʀʀᴇᴜʀ ᴅᴇ ᴛᴇʟᴇ́ᴄʜᴀʀɢᴇᴍᴇɴᴛ:** {e}")

    await download_msg.edit("**__ʀᴇɴᴏᴍᴍᴀɢᴇ ᴇᴛ ᴀᴊᴏᴜᴛ ᴅᴇ ᴍéᴛᴀᴅᴏɴɴéᴇs...__**")

    try:
        # Rename the file first
        os.rename(path, renamed_file_path)
        path = renamed_file_path

        # Add metadata if needed
        metadata_added = False
        _bool_metadata = await hyoshcoder.get_metadata(user_id)
        if _bool_metadata:
            metadata = await hyoshcoder.get_metadata_code(user_id)
            if metadata:
                cmd = f'ffmpeg -i "{renamed_file_path}"  -map 0 -c:s copy -c:a copy -c:v copy -metadata title="{metadata}" -metadata author="{metadata}" -metadata:s:s title="{metadata}" -metadata:s:a title="{metadata}" -metadata:s:v title="{metadata}"  "{metadata_file_path}"'
                try:
                    process = await asyncio.create_subprocess_shell(
                        cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await process.communicate()
                    if process.returncode == 0:
                        metadata_added = True
                        path = metadata_file_path
                    else:
                        error_message = stderr.decode()
                        await download_msg.edit(f"**ᴇʀʀᴇᴜʀ ᴅᴇ ᴍéᴛᴀᴅᴏɴɴéᴇs:**\n{error_message}")
                except asyncio.TimeoutError:
                    await download_msg.edit("**ᴄᴏᴍᴍᴀɴᴅᴇ ғғᴍᴘᴇɢ ᴇxᴘɪʀéᴇ.**")
                    return
                except Exception as e:
                    await download_msg.edit(f"**ᴜɴᴇ ᴇxᴄᴇᴘᴛɪᴏɴ s'ᴇsᴛ ᴘʀᴏᴅᴜɪᴛᴇ:**\n{str(e)}")
                    return
        else:
            metadata_added = True

        if not metadata_added:
            # Metadata addition failed; upload the renamed file only
            await download_msg.edit(
                "L'ᴀᴊᴏᴜᴛ ᴅᴇs mᴇ́tᴀᴅᴏɴᴇᴇs ᴀ échoué. ᴛéʟᴇᴠᴇʀsᴇᴍᴇɴᴛ du ғɪchiᴇr ʀᴇɴᴏᴍᴍé."
            )
            path = renamed_file_path

        # Upload the file
        upload_msg = await download_msg.edit("**ᴛéʟᴇᴠᴇʀsᴇᴍᴇɴᴛ...__**")

        ph_path = None
        c_caption = await hyoshcoder.get_caption(message.chat.id)
        c_thumb = await hyoshcoder.get_thumbnail(message.chat.id)

        if message.document:
            file_size = humanbytes(message.document.file_size)
            duration = convert(0)
        elif message.video:
            file_size = humanbytes(message.video.file_size)
            duration = convert(message.video.duration or 0) 
        else:
            await message.reply("Le message ne contient pas de document ou de vidéo pris en charge.")
            return

        caption = (
            c_caption.format(
                filename=renamed_file_name,
                filesize=file_size,
                duration=duration,
            )
            if c_caption
            else f"**{renamed_file_name}**"
        )


        if c_thumb:
            ph_path = await client.download_media(c_thumb)
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            img = Image.open(ph_path).convert("RGB")
            img = img.resize((320, 320))
            img.save(ph_path, "JPEG")

        try:
            if media_type == "document":
                await client.send_document(
                    message.chat.id,
                    document=path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("ᴛéʟᴇᴠᴇʀsᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀs...", upload_msg, time.time()),
                )
            elif media_type == "video":
                await client.send_video(
                    message.chat.id,
                    video=path,
                    caption=caption,
                    thumb=ph_path,
                    duration=0,
                    progress=progress_for_pyrogram,
                    progress_args=("ᴛéʟᴇᴠᴇʀsᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀs...", upload_msg, time.time()),
                )
            elif media_type == "audio":
                await client.send_audio(
                    message.chat.id,
                    audio=path,
                    caption=caption,
                    thumb=ph_path,
                    duration=0,
                    progress=progress_for_pyrogram,
                    progress_args=("ᴛéʟᴇᴠᴇʀsᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀs...", upload_msg, time.time()),
                )
        except Exception as e:
            os.remove(renamed_file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")

        await download_msg.delete() 
        os.remove(renamed_file_path)
        if ph_path:
            os.remove(ph_path)

    finally:
        # Clean up
        if os.path.exists(renamed_file_path):
            os.remove(renamed_file_path)
        if os.path.exists(metadata_file_path):
            os.remove(metadata_file_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)
        del renaming_operations[file_id]
