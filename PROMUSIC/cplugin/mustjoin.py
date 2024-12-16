from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserNotParticipant, ChatAdminRequired

# Define the channel name or ID for the MUST_JOIN channel
MUST_JOIN = "ProBotts"

# Function in the main bot to check if a user is a member of the required channel
async def is_user_in_channel(app: Client, user_id: int) -> bool:
    """
    Check if a user is a member of the required channel.
    Args:
        app: The main bot instance.
        user_id: The user's Telegram ID.

    Returns:
        bool: True if the user is a member, False otherwise.
    """
    try:
        await app.get_chat_member(MUST_JOIN, user_id)
        return True  # User is a member
    except UserNotParticipant:
        return False  # User is not a member
    except ChatAdminRequired:
        print(f"Main bot needs admin rights in {MUST_JOIN} to check user membership!")
        return False


# Function in the clone bot to handle new users and check membership
@Client.on_message(filters.command("start") & filters.private)
async def handle_start(client: Client, msg: Message):
    """
    Handle the /start command in the clone bot and check channel membership.
    """
    user_id = msg.from_user.id

    # Import the main app for checking membership
    from PROMUSIC import app

    # Check membership using the helper function
    is_member = await is_user_in_channel(app, user_id)

    if not is_member:
        # If the user is not a member, generate the join link
        if MUST_JOIN.isalpha():
            link = f"https://t.me/{MUST_JOIN}"
        else:
            chat_info = await app.get_chat(MUST_JOIN)
            link = chat_info.invite_link or f"https://t.me/{MUST_JOIN}"

        # Send the join message using the clone bot
        await msg.reply_photo(
            photo="https://telegra.ph/file/9915defb71630019626fb.jpg",
            caption=(
                f"๏ ʏᴏᴜ'ʀᴇ ɴᴏᴛ ᴀ ᴍᴇᴍʙᴇʀ ᴏғ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ʏᴇᴛ!\n"
                f"ᴘʟᴇᴀsᴇ ᴊᴏɪɴ [๏sᴜᴘᴘᴏʀᴛ๏]({link}) ᴛᴏ ᴜsᴇ ᴍᴇ."
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("๏Jᴏɪɴ๏", url=link)]]
            ),
        )
    else:
        # User is a member; proceed with the usual bot functionality
        await msg.reply("Welcome! 🎉 You're all set to use the bot.")
