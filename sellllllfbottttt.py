import requests
import random
import os
import asyncio
import re
import math
from telethon import TelegramClient, events
from flask import Flask 
from threading import Thread
import uuid
import string
import instaloader
from telethon.tl.functions.contacts import BlockRequest



# Enter your own API details
API_ID = 24036023
API_HASH = "e40bd95bfc9f55e578512c868269eaeb"
BOT = TelegramClient('bot', API_ID, API_HASH).start()

app = Flask('')

@app.route('/')
def home():
    return "I am alive"

def run_http_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http_server)
    t.start()

# Your Telegram ID (Only you can use commands)
ADMIN_ID = 5123961345

# Track muted users
muted_users = set()

# Track targeted users for abuse
targeted_users = {}

# Abuses (can be modified with more non-offensive alternatives)
abuses = [
    "Teri mummy ki flipcart se order kar lunga",
    "Abe chamar teri mummy ko 🪑कुर्सी pe bitha ke इमरान हाशमी wala scene re-create kar dunga💀🤣",
    "Teri mummy ki flipcart se order kar lunga",
    "Abe chamar teri mummy ko 🪑कुर्सी pe bitha ke इमरान हाशमी wala scene re-create kar dunga💀🤣",
    "Gang rape krwa du kya teri mummy ka?",
    "Tera baap hizda",
    "Sasti naali ke keede chup",
    "गोभी प्याज भिंडी आलू, क्या तेरी बहन को मैं पटालूं¿?",
    "Teri mummy mere ghar me kam karne wali baai",
    "Teri behan ki chut me kutte ka sperm",
    "kutte ki paidaish",
    "Teri mummy ko momos khilakr chod dunga",
    "TERI MAA KE BHOSDA PE MUKKA MAARU",
    "TMKC MEII BILLI",
    "TMKC MEI DOG",
    "MAA CHUDA RANDIKE BACCHE",
    "gadhe ke bachhe",
    "chup madarchod",
    "Chup gareeb",
    "काली घाटी के अंधेरे में तेरी मम्मी चोद कर भाग जाऊंगा🥱😝",
    "Kutte se chudwa dunga teri behan ko",
    "Gali gali me rehta hai saand, teri mummy ko itna choda ki wo ban gyi Raand😁",
    "Maja aaya chudkr?",
    "chup chudi hui raand ke bette",
    "ठंडी आ गई ना? तेरी मम्मी के भोसड़े में आग लगाकर अपने हाथ सेक लूंगा🤡",
    "Teri behan ki yaado me jee rha hu ab bss",
    "Tu apni behan ko smjha randi ke pehle kahi wo v teri mummy ki tarah professional randi na ban jaaye💀",
    "Ter behan ko hentai dikha dunga",
    "kutte ke muh me ghee or tu mera lund pee randike",
    "Tu or teri mummy mere lwde pe",
    "chup reh warna teri behan ke sath shower together le lunga",
    "GAND MAI VIMAL KI GOLI BNA KAR DE DUNGA BHENCHO TERI GAAND MAI RAILWAY STATION KA FATAK DE DUNGA 😂😂🤬🖕",
    "Janta dukhi hai modi se, teri mummy ko uthne nahi dunga aaj apni godi se",
    "तेरी मम्मी ने last time अपनी झाटे कब काटी थी...?🤗",
    "तू अपनी बहन को बोल न मुझे अपने जांघों के बीच दबा कर मार दे🙈",
    "Bhenchod baap se panga matt le Warna maa chodh di Jayegi 🤬",
    "Teri mummy ke muh se apna zip khulwa lunga",
    "jannat me jaakr teri pardadi ko chod dunga",
    "Bhosadchod Teri mayya ki gaand me Teri bahan ko le ghuskar itne bache paida karunga ki tujhe ye decide karte karte heart attack a jayega ki tu unka mama hai ya bhayya",
    "Maine to sapne bhi teri behan ko chodne wale dekhe hn",
    "Bura mat maniyo teri mummy ni chod sakta, apni wali ke liye loyal hu",
    "Tera baap hizda",
    "gb road ki paidaish hai tu",
    "Teri budhiya dadi mere bathroom me fisal gyi",
    "Teri mummy ko promise kiya hu ki use aaj bikni gift karunga",
    "Teri behan ki gori chut hai ya kaali¿?",
    "Kaapta hai kutta thand me, or teri mummy ko khushi milti bs mere lund me",
    "1+1=3 (क्योंकि तेरी मम्मी को बिन condom के चो*द दिया था मैं)",
    "Tere muh me hag dunga •_•",
    "madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye",
    "TARI MAA KO CHOD KA 9MONTH BAAD EK OUR RAAVAN NIKALGA BHAN KA LODO SAMBAL KA RAHNA BAAP SA MAA CHOD DAGA JIS NA BHI FAADA KIYA MUJSA..# 🤧😡🤬",
    "Jhate saaf krwaunga teri behan se apne",
    "Teri mummy ko sexually harass kar dunga😈👍🏻",
    "Chudayi kar du aapni mummy ki??",
    "Janta dukhi hai modi se, teri mummy ko uthne nahi dunga aaj apni godi se",
    "Jana lwde teri mummy ko chudne se bacha",
    "Aadat se लचार hu, teri mummy ka purana भतार hu",
    "TERA BAAP JOHNY SINS CIRCUS KAY BHOSDE JOKER KI CHIDAAS 14 LUND KI DHAAR TERI MUMMY KI CHUT MAI 200 INCH KA LUND."
    # More non-offensive or creative insults
]

# Modified commands list with new descriptions
commands = """******𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:**  

➤ `.mute` → Mute a user (Admin required).  
➤ `.unmute` → Unmute a user (Admin required).  
➤ `.kick` → Kick a user from the group (Admin required).  
➤ `.block` → Block a user (Reply to a user's message).  
➤ `.unblock` → Unblock a user (Reply to a user's message).  
➤ `.chudle` → Target a user for abuses.  
➤ `.soja` → Stop abusing a targeted user.  
➤ `.cmd` → Show all commands.  
➤ `.calc <expression>` → Perform a math calculation.  
➤ `.reset <username/email>` → Send an Instagram password reset link.  
➤ `.delete` →  
   - **In private chat:** Deletes all messages.  
   - **In groups:** Deletes all messages sent by a user (if replied).  
➤ `.id` → Get a user's Telegram ID (or your own).  
➤ `.channel` → Get the bot’s official channel link.  
➤ `.info <user_id>` → Fetch Telegram user details.  
➤ `.upi` → Show UPI QR code for payments.  
➤ `.insta <username>` → Fetch Instagram user details.  

**𝗡𝗼𝘁𝗲:**  
The bot must be an admin for certain commands to work in groups.  

"""

# Fetch the admin's first name with username link
async def get_admin_name():
    admin = await BOT.get_entity(ADMIN_ID)
    return f"[{admin.first_name}](tg://user?id={ADMIN_ID})"

# Handle the `.upi` command for generating QR Code
QR_CODE_PATH = "UPI.jpg"  # Change this to your actual file path
@BOT.on(events.NewMessage(pattern=r"\.upi"))
async def upi(event):
    if not os.path.exists(QR_CODE_PATH):
        await event.edit("Error: QR Code image not found!")
        return

    caption = """🧸 **UPI ID**: `shriramdhoot20@okicici`
Please confirm the name **'Shriram Dhoot'** before sending any funds. Thanks."""
    
    await event.edit("Generating QR Code...")
    await asyncio.sleep(1)
    await BOT.send_file(event.chat_id, QR_CODE_PATH, caption=caption)

# Event handler for commands
@BOT.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.id
    chat = await event.get_chat()

    # Only allow admin to execute commands
    if sender_id != ADMIN_ID:
        return

    # Show available commands
    if event.raw_text.lower() == ".cmd":
        await event.edit(commands)
        return

    # .calc command to perform calculations
    if event.raw_text.lower().startswith(".calc "):
        expression = event.raw_text[6:].strip()
        expression = expression.replace('×', '*').replace('÷', '/').replace('π', str(math.pi))
        expression = re.sub(r'√(\d+)', r'math.sqrt(\1)', expression)

        if not re.match(r"^[0-9+\-*/(). math.sqrt]+$", expression):
            await event.edit("❌ Invalid expression.")
            return

        try:
            result = eval(expression)
            await event.edit(f"🧮 **Calculation:** `{expression}`\n📊 **Result:** `{result}`")
        except:
            await event.edit("❌ Error in calculation.")
        return

    # Mute command: Deletes messages from muted users
    if event.raw_text.lower() == ".mute" and event.is_reply:
        reply_msg = await event.get_reply_message()
        muted_user = reply_msg.sender_id
        if muted_user not in muted_users:
            muted_users.add(muted_user)
            muted_name = f"[{reply_msg.sender.first_name}](tg://user?id={muted_user})"
            admin_name = await get_admin_name()
            await event.edit(f"🔇 {muted_name} has been muted.\n\n**Made by {admin_name}**")
        return

    # Unmute command: Allows muted user to send messages again
    if event.raw_text.lower() == ".unmute" and event.is_reply:
        reply_msg = await event.get_reply_message()
        muted_user = reply_msg.sender_id
        if muted_user in muted_users:
            muted_users.remove(muted_user)
            muted_name = f"[{reply_msg.sender.first_name}](tg://user?id={muted_user})"
            admin_name = await get_admin_name()
            await event.edit(f"🔊 {muted_name} has been unmuted.\n\n**Made by {admin_name}**")
        return

    # Kick command: Remove a user from the group
    if event.raw_text.lower() == ".kick" and event.is_reply and event.is_group:
        reply_msg = await event.get_reply_message()
        kicked_user = reply_msg.sender_id
        try:
            await BOT.kick_participant(chat.id, kicked_user)
            kicked_name = f"[{reply_msg.sender.first_name}](tg://user?id={kicked_user})"
            admin_name = await get_admin_name()
            await event.edit(f"👢 {kicked_name} has been kicked from the group.\n\n**Made by {admin_name}**")
        except:
            await event.edit("❌ I need admin rights to kick users!")
        return

    # .chudle command: Target a user for abuse
    if event.raw_text.lower() == ".chudle" and event.is_reply:
        reply_msg = await event.get_reply_message()
        target_user = reply_msg.sender_id
        targeted_users[target_user] = True
        target_name = f"[{reply_msg.sender.first_name}](tg://user?id={target_user})"
        admin_name = await get_admin_name()
        await event.edit(f"🔴 {target_name} has been targeted for abuses!\n\n**Made by {admin_name}**")
        return

    # .soja command: Stop abuse targeting for a user
    if event.raw_text.lower() == ".soja" and event.is_reply:
        reply_msg = await event.get_reply_message()
        target_user = reply_msg.sender_id
        if target_user in targeted_users:
            del targeted_users[target_user]
            target_name = f"[{reply_msg.sender.first_name}](tg://user?id={target_user})"
            admin_name = await get_admin_name()
            await event.edit(f"🛑 {target_name} is no longer targeted for abuses.\n\n**Made by {admin_name}**")
        return

# Event to delete muted users' messages automatically
@BOT.on(events.NewMessage)
async def delete_muted_messages(event):
    sender_id = event.sender_id
    if sender_id in muted_users:
        await event.delete()
        
@BOT.on(events.NewMessage(pattern=r"\.id"))
async def get_user_id(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
        user_name = reply_msg.sender.first_name
        await event.edit(f"🆔 **User ID:** `{user_id}`\n👤 **Name:** {user_name}")
    else:
        await event.edit(f"🆔 **Owner ID:** `{ADMIN_ID}`")

@BOT.on(events.NewMessage(pattern=r"\.channel"))
async def send_channel_link(event):
    await event.edit("🔗 **Join our channel:** [ROLEX THE FIXER](https://t.me/+0WbqKl-rzv45MmM1)")
    
INSTAGRAM_RESET_URL = "https://i.instagram.com/api/v1/accounts/send_password_reset/"

@BOT.on(events.NewMessage(pattern=r"\.reset (.+)"))
async def reset_instagram_password(event):
    user_input = event.pattern_match.group(1).strip()

    if not user_input:
        await event.edit("❌ **Please provide a valid Instagram username or email.**")
        return

    await event.edit(f"🔄 **Requesting password reset for:** `{user_input}`")

    # Generate CSRF token and device details
    data = {
        "_csrftoken": "".join(random.choices(string.ascii_letters + string.digits, k=32)),
        "guid": str(uuid.uuid4()),
        "device_id": str(uuid.uuid4()),
    }

    # Check if input is an email or username
    if "@" in user_input:
        data["user_email"] = user_input
    else:
        data["username"] = user_input

    # Generate a random User-Agent to mimic Instagram's mobile app
    user_agent = f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)"

    headers = {
        "user-agent": user_agent
    }

    # Send the request
    response = requests.post(INSTAGRAM_RESET_URL, headers=headers, data=data)

    # Process response
    if "obfuscated_email" in response.text:
        await event.edit(f"✅ **Password reset link sent successfully to:** `{user_input}`\nCheck your email or messages.")
    else:
        await event.edit(f"❌ **Failed to send reset link. Response:** `{response.text}`")

@BOT.on(events.NewMessage(pattern=r"\.delete(?: (.+))?"))
async def delete_messages(event):
    # Case 1: Private Chat - Delete all messages
    if event.is_private:
        try:
            async for message in BOT.iter_messages(event.chat_id):
                await message.delete()
            
            # Send confirmation message and delete it after 3 seconds
            confirmation = await event.respond("✅ **Deleted all messages in this chat.**")
            await asyncio.sleep(3)
            await confirmation.delete()
            
        except Exception as e:
            await event.respond(f"❌ **Error:** `{str(e)}`")

    # Case 2: Group Chat - Delete all messages from a user (if replied)
    elif event.is_group and event.is_reply:
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id

        if not user_id:
            await event.edit("❌ **Could not find the user.**")
            return

        try:
            count = 0
            async for message in BOT.iter_messages(event.chat_id, from_user=user_id):
                await message.delete()
                count += 1

            await event.edit(f"✅ **Deleted {count} messages from the user.**")
        except Exception as e:
            await event.edit(f"❌ **Error:** `{str(e)}`")

    else:
        await event.edit("❌ **Invalid usage. Reply to a message in a group or use in private chat.**")
        
@BOT.on(events.NewMessage(pattern=r"\.info (\d+)"))
async def get_user_info(event):
    user_id = int(event.pattern_match.group(1))  # Extract user ID from command

    try:
        user = await BOT.get_entity(user_id)  # Fetch user details

        username = f"@{user.username}" if user.username else "Not set"
        first_name = user.first_name if user.first_name else "Not set"
        last_name = user.last_name if user.last_name else "Not set"

        response = (
            f"🔍 **User Info:**\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"👤 **First Name:** {first_name}\n"
            f"👥 **Last Name:** {last_name}\n"
            f"📛 **Username:** {username}"
        )

        await event.edit(response)

    except Exception as e:
        await event.edit(f"❌ **Error:** {str(e)}")
        

L = instaloader.Instaloader()

def get_instagram_user_details(user):
    try:
        # Load the profile of the user
        profile = instaloader.Profile.from_username(L.context, user)

        # Extract user details
        name = profile.full_name
        username = profile.username
        user_id = profile.userid
        followers = profile.followers
        following = profile.followees
        posts = profile.mediacount
        profile_pic_url = profile.profile_pic_url

        # Define the ID ranges and corresponding years
        ranges = [
            (1279000, 2010),
            (17750000, 2011),
            (279760000, 2012),
            (900990000, 2013),
            (1629010000, 2014),
            (2500000000, 2015),
            (3713668786, 2016),
            (5699785217, 2017),
            (8597939245, 2018),
            (21254029834, 2019),
            (43464475395, 2020),
            (50289297647, 2021),
            (57464707082, 2022),
            (63313426938, 2023)
        ]

        # Determine the year based on the user ID
        year_associated = "Year not found"
        for user_range, year in ranges:
            if user_id <= user_range:
                year_associated = year
                break

        # Create the Instagram URL
        insta_url = f"https://www.instagram.com/{username}/"

        # Return formatted details
        return f"👤 **Name**: `{name}`\n\n" \
               f"💬 **Username**: `{username}`\n\n" \
               f"🆔 **User ID**: `{user_id}`\n\n" \
               f"👥 **Followers**: `{followers}`\n\n" \
               f"📈 **Following**: `{following}`\n\n" \
               f"📸 **Posts**: `{posts}`\n\n" \
               f"🖼️ **Profile Picture**: [View Profile Pic]({profile_pic_url})\n\n" \
               f"🔗 **Instagram Profile**: [Click here]({insta_url})\n\n" \
               f"📅 **Year of Creation**: `{year_associated}`\n"

    except Exception as e:
        return "❌ Failed to retrieve details."

# Telegram command handler for `.insta`
@BOT.on(events.NewMessage(pattern=r"\.insta (\S+)"))
async def insta_handler(event):
    user = event.pattern_match.group(1).strip()

    # Remove '@' if it's at the start of the username
    if user.startswith('@'):
        user = user[1:]

    # Get user details
    user_details = get_instagram_user_details(user)

    # Send the details back to the user
    await event.respond(user_details, parse_mode='Markdown')
    
from telethon.tl.functions.contacts import BlockRequest

from telethon.tl.functions.contacts import BlockRequest

from telethon.tl.functions.contacts import BlockRequest

from telethon.tl.functions.contacts import BlockRequest

from telethon.tl.functions.contacts import BlockRequest

@BOT.on(events.NewMessage(pattern=r"\.block"))
async def block_user(event):
    if event.is_reply:
        # In both private chat and group, block the user being replied to
        reply_msg = await event.get_reply_message()
        user = await BOT.get_entity(reply_msg.sender_id)  # Get the user being replied to
        
        try:
            await BOT(BlockRequest(user))  # Block the user
            user_name = f"[{user.first_name}](tg://user?id={user.id})"
            await event.edit(f"🚫 **Blocked:** {user_name}")
        except Exception as e:
            await event.edit(f"❌ Failed to block user: `{str(e)}`")
    else:
        await event.edit("❗ **Reply to a user's message to block them.**")

from telethon.tl.functions.contacts import UnblockRequest

@BOT.on(events.NewMessage(pattern=r"\.unblock"))
async def unblock_user(event):
    if event.is_reply:
        # In both private chat and group, unblock the user being replied to
        reply_msg = await event.get_reply_message()
        user = await BOT.get_entity(reply_msg.sender_id)  # Get the user being replied to
        
        try:
            await BOT(UnblockRequest(user))  # Unblock the user
            user_name = f"[{user.first_name}](tg://user?id={user.id})"
            await event.edit(f"✅ **Unblocked:** {user_name}")
        except Exception as e:
            await event.edit(f"❌ Failed to unblock user: `{str(e)}`")
    else:
        await event.edit("❗ **Reply to a user's message to unblock them.**")
        r




        
    
               
               
# Continuously send abuses if the user is targeted
@BOT.on(events.NewMessage)
async def send_abuse_to_targeted_user(event):
    sender_id = event.sender.id
    if sender_id in targeted_users:
        abuse = random.choice(abuses)
        target_name = f"[{event.sender.first_name}](tg://user?id={sender_id})"
        admin_name = await get_admin_name()
        await event.reply(f"💥 {abuse}")
        await asyncio.sleep(2)  # Add a delay of 2 seconds between abuses to avoid rate limit
keep_alive( )
print("Bot is running on Pydroid 3...")
BOT.run_until_disconnected()