import time
import random
from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import config
# from PROMUSIC import app
from PROMUSIC.misc import _boot_
from PROMUSIC.plugins.sudo.sudoers import sudoers_list
from PROMUSIC.utils.database import get_served_chats, get_served_users, get_sudoers
from PROMUSIC.utils import bot_sys_stats
from PROMUSIC.utils.database import (
    add_served_chat_clone,
    add_served_user_clone,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from PROMUSIC.utils.decorators.language import LanguageStart
from PROMUSIC.utils.formatters import get_readable_time
from PROMUSIC.utils.inline import help_pannel, private_panel, start_panel, clone_private_panel, clone_start_panel
from config import BANNED_USERS
from strings import get_string

#--------------------------

NEXI_VID = [
"https://telegra.ph/file/1a3c152717eb9d2e94dc2.mp4",
"https://graph.org/file/ba7699c28dab379b518ca.mp4",
"https://graph.org/file/83ebf52e8bbf138620de7.mp4",
"https://graph.org/file/82fd67aa56eb1b299e08d.mp4",
"https://graph.org/file/318eac81e3d4667edcb77.mp4",
"https://graph.org/file/7c1aa59649fbf3ab422da.mp4",
"https://graph.org/file/2a7f857f31b32766ac6fc.mp4",

]



@Client.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    a = await client.get_me()
    await add_served_user_clone(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_video(
                random.choice(NEXI_VID),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)

            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, a.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
    
    else:
        out = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{a.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper"),
        ],
    ]
        # out = private_panel(_)
        await message.reply_video(
            random.choice(NEXI_VID),
            caption=_["start_2"].format(message.from_user.mention, a.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )


@Client.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    a = await client.get_me()
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_video(
        random.choice(NEXI_VID),
        caption=_["start_1"].format(a.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat_clone(message.chat.id)


@Client.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    a = await client.get_me()
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == a.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await client.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            a.mention,
                            f"https://t.me/{a.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await client.leave_chat(message.chat.id)

                # out = start_panel(_)
                out = [
                    [
                        InlineKeyboardButton(
                            text=_["S_B_1"], url=f"https://t.me/{a.username}?startgroup=true"
                        ),
                        InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
                    ],
                ]

                await message.reply_video(
                    random.choice(NEXI_VID),
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        a.mention,
                        message.chat.title,
                        a.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat_clone(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
