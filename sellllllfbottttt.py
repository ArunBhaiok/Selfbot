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
from telethon.tl.functions.account import UpdateProfileRequest




# Enter your own API details
API_ID = 24036023
API_HASH = "e40bd95bfc9f55e578512c868269eaeb"
BOT = TelegramClient('bot', API_ID, API_HASH).start()

BOT_OWNER = "@shriram4311"
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
    "Teri maa ko chamar pel gaya 😝",
    "Teri maa di fuddi🍌",
    "Teri maa ke silencer mai mera kela 🍌",
    "Teri maa 150 ki raand😝",
    "Teri maa top seller hai lavde 😝"
    "Teri maa ka dealer hu 🤝",
    "Aaj ki raat ...teri maa k sathh👅💦",
    "Teri maa ka ashiq hu 🗿",
    "Teri maa ne mera choco liya 😝🍌",
    "Teri maaa pr udaa bhoot....dekh yaha tera baap",
    "Teri maa ki chut chaatke paani nikaluga 👅👅💦💦",
    "Teri ma ki chut jaise rasmalai jaisi mithai",
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
    "हिंदी की मात्रा बनाते हुए तेरी दीदी पेल दूंगा चमार की औलाद 🤭🤣",
    "Tu yaha typing kar rha or idhar teri mummy chud rahi chutiye💀",
    "Jhaat se baandhkr teri mummy ko faasi laga dunga randi ke😂😎",
    "Aisa lund fek ke marunga ki tera khandan chud jayega hizde ki paidaish 👹🙈",
    "Abe chamar teri mummy ko 🪑कुर्सी pe bitha ke इमरान हाशमी wala scene re-create kar dunga💀🤣",
    "Chup chhoti jaat ke !! Bhosdike teri awkaat ni hai av mere saamne bolne ki अछूत 🖕🏻🗣️",
    "Main yaha imagine karunga or waha teri behan pregnant ho jayegi😝🥱",
    "झाटे ना चूची तेरी मम्मी मेरी कुची पूची 😍🥰🙈",
    "ठंडी आ गई ना? तेरी मम्मी के भोसड़े में आग लगाकर अपने हाथ सेक लूंगा🤡",
    "लाइफबॉय का साबुन डव वाले शैंपू में, तेरी मम्मी चुदेगी बेटा चलते हुए टेंपू में⚙️😈️",
    "Muh band rkh 1 dollar me bikne wali ke bete🤫😂",
    "GAND KII DHAAR BHOSDIKE FATEE HUE CONDOM KI NAAJAIS PAIDAISH",
    "Teri maa ki choot gand kay tatto teri maa ka bhosda karke uski gaand mai ping pong kar dunga",
    "madar chod bhosdke esa lagta h apne hii taaate kaat ke chipka diya apni shakal dekh lodee jese shakal aur gand me h aakal",
    "Teri ma ki gand me hathi ka lund dalke asa chodunga Na Bacha hojayega Johny sins ,ke lund se chudwaungu bhosdike",
    "GAND MAI VIMAL KI GOLI BNA KAR DE DUNGA BHENCHO TERI GAAND MAI RAILWAY STATION KA FATAK DE DUNGA 😂😂🤬🖕",
    "teri maa k bhosde mai MDH CHANA MASALA daal k tere baap ko vo spicy bhosda khila dunga 🥵🤮",
    "maa k lode tere jese randi k baccho ko bachpan mai maar dena chiye",
    "madarchod chutmarke teri tatti jesi shakl pe pad dunga bhen k lode chutiye",
    "Bhenchod baap se panga matt le Warna maa chodh di Jayegi 🤬",
    "Abbe teri maa ki chut ko kutte se katva dunga randi k pille 😡😠😤teri behn ki chut mai set top box ghusa dunga mai madarchod 😳",
    "chutmarik teri tatti jesi shakl pe pad dunga bhen k lode chutiye madarchod kitna chutiya aadmi hai Tu😡",
    "jaya bachan bana kai chod dunga teri behn ko😋 maa k lode tere jese randi k baccho ka abortion krva dena chiye 😤",
    "bhosdk teri maa k bhosde mai MDH CHANA MASALA daal k tere baap ko vo spicy bhosda khila dunga 🤢",
    "Tere dalle baap ka lund uth'ta hai nhi tbhi teri maa 150 k bhav se deti hai 😍 madarchod k baache sudhar ja 😡😠😤",
    "ABA SUN ☀ CHOR BHOSDI TERI MAA KO 🤶 NANGHI KR 🆎 KA 🔫 LUNDO KI 🆖🤴🅱 MALA PAHNAKA CHAURAHA KASAO CHAKKAR MARVAUNGA",
    "Jhaatu",
    "Chamar",
    "randike",
    "Tujhe pta hai teri behan bhi teri mummy ki tarah randi ban rhi🤭😮‍💨",
    "q teri maa randipanti chhor ke sudharna chahti hai?, mere lund pe bitha pehle💀💞",
    "Sun? Teri maa rand ki sardarni otey¿?🤗",
    "Teri mummy ke boobs dabau ya chut khau?😘",
    "teri mummy ki chut ki seal toot gyi kya?😁",
    "Randike chup ho jaa",
    "Achha? oohhohoho? Chup teri maaki chut",
    "Hatt bhosdiwale",
    "Ger ger ke marunga",
    "patak patak ke chodunga teri didi ko",
    "Sadi hi chut wali ke bete",
    "Teri mummy ki chut me bidi fook dunga",
    "Jhaate saaf kr du kya teri mummy ke?",
    "Kutte se chudwa dunga teri behan ko",
    "सस्ती रण्डी के बच्चे",
    "kutte ki paidaish",
    "Chup gareeb",
    "Tere baap 6kka tha isilye ye proof hai ki tu mera hi beta hai",
    "kaali ghaati ke andhere me teri mummy pelkar bhaag jaunga",
    "Ghar ghar me shor hai teri mummy ki chut kamjor hai, kabhi bhi fatt skti hai💀",
    "Gang rape krwa du kya teri mummy ka?",
    "Sun tujhe pta hai teri behan kitno se chudi hai¿?",
    "Kutte ka lund or teri mummy ki chut",
    "Apne ghar ki saaf safai krwa lunga teri mummy se",
    "Teri bua ki jhuka kr gand maar lunga",
    "aisa lund fek ke marunga kibteri puri khandan chud jaegi",
    "Tu mera hi beta hai chutiye",
    "Teri mummy ki kaali gand",
    "teri budhi bua ki safed chut ki baal",
    "Jhate saaf krwaunga teri behan se apne",
    "teri mummy ki gand me mera smily emoji",
    "mera mental health teri mummy ki tarah hai, hmesa chudta rehta",
    "teri maa kitno se chudi hai?",
    "jhaat ke baal",
    "gadhe ke bachhe",
    "kutti ke pille",
    "Tere baap ki biwi mere lwde pe",
    "Maja aaya chudkr?",
    "aagya swaad?",
    "Kaisa laga chudkr bete?",
    "Buddhi ke baal",
    "Teri mummy mere bed pr",
    "teri ammy ke jh@nto ko pakad ke building se latka dunga.",
    "Kaali ch00t wali r@nd ke bachhe behnch0d",
    "Paodaan ki shakal ke g@ndu sale.",
    "Vimal khane wale r@ndi ke bachhe m@dharch0d."
    # More non-offensive or creative insults
]

# Modified commands list with new descriptions
commands = """  
******```𝗔𝘃𝗮𝗶𝗹𝗮𝗯𝗹𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:**  

➤ `.mute` → Mute a user (Admin only).  
➤ `.unmute` → Unmute a muted user.  
➤ `.kick` → Remove a user from the group.  
➤ `.block` → Block a user (Reply required).  
➤ `.unblock` → Unblock a user (Reply required).  
➤ `.delete` → Delete all messages in private or replied user's messages in a group.  
➤ `.id` → Get a user's Telegram ID.  
➤ `.info <user_id>` → Fetch user details.
➤ `.instaid` → Get Owners Instagram Id. 
➤ `.channel` → Get bot’s official channel link.➤ `.insta <username>` → Get Instagram user details.  
➤ `.reset <username/email>` → Request an Instagram password reset.  
➤ `.calc <expression>` → Perform a math calculation.
➤ `.broadcast <message>` → Send a message to all private chats.  
➤ `.dm <username> <message>` → Send a direct message. 
   - **Without message:** Sends `"Hi There @botplays90 This Side 😄"`  
➤ `.chudle` → Target a user for abuses (Reply required).  
➤ `.soja` → Stop abusing a targeted user.  
➤ `.chudai` →  
   - **In DMs:** Send continuous abuses.  
   - **In groups (Reply):** Abuse the replied user.  
   - **In groups (No reply):** Abuse with sender's name.  
➤ `.rukja` → Stop `.chudai` abuse spam.  
➤ `.translate` →  
   - **Reply method:** Translate the replied message.  
   - **Direct method:** `.translate <message>` to translate text.  
➤ `.upi` → Show UPI QR code for payments.
➤ `.phoneinfo` → Get Basic Mobile Number Information
➤ `.ip` <Ip Address> → Get Ip Address Details.
➤ `.wthr` <city> → See Weather Status.
➤ `.status` <online/offline> → Set bot status.  
   - .status → Show current status.
➤ `.setbio` → Sets Your Bio.
➤ `.pline` → Get a random pickup line.
➤ `.pin [reply/message ID/text]` → Pin a message in the chat.  
➤ `.unpin` → Unpin the latest pinned message.➤ `.ai <question>` → Ask Google Gemini AI.  
➤ `.search <query>` → Search Google and get top results.    


**𝗡𝗼𝘁𝗲:**  
The bot must be an admin for certain commands to work in groups.```  

"""

# Fetch the admin's first name with username link
async def get_admin_name():
    admin = await BOT.get_entity(ADMIN_ID)
    return f"[{admin.first_name}](tg://user?id={ADMIN_ID})"

import os
import random

@BOT.on(events.NewMessage(pattern=r"\.upi"))
async def upi(event):
    qr_files = [f for f in os.listdir() if f.startswith("UPI") and (f.endswith(".jpg") or f.endswith(".png"))]
    
    if not qr_files:
        await event.edit("Error: No QR codes found in the directory!")
        return

    random_qr = random.choice(qr_files)

    caption = """🧸 **UPI ID**: `shriramdhoot20@okicici`
Please confirm the name **'Shriram Dhoot'** before sending any funds. Thanks."""
    
    await event.edit("Fetching QR Code...")
    await asyncio.sleep(1)
    await BOT.send_file(event.chat_id, random_qr, caption=caption)


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
    await event.edit("🔗 **Join our channel:** [ROLEX ™ 🦁👑❤️](https://t.me/+0WbqKl-rzv45MmM1)")
    
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
        
@BOT.on(events.NewMessage(pattern=r"\.info(?:\s+(\d+))?"))
async def get_user_info(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
    else:
        user_id = event.pattern_match.group(1)
        if not user_id:
            await event.edit("❌ **Reply to a message or provide a User ID!**")
            return
        user_id = int(user_id)

    await event.edit("🔍 **Fetching user info...**")

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

    except ValueError:
        await event.edit("❌ **Invalid User ID!**")
    except Exception as e:
        await event.edit("❌ **Error fetching user info:**\n"
                         "📌 Possible reasons:\n"
                         "- User has **privacy settings** enabled.\n"
                         "- User has **never interacted** with the bot.\n"
                         "- Bot cannot access this user.\n\n"
                         f"🔍 **Error Details:** `{str(e)}`")



        

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

@BOT.on(events.NewMessage(pattern=r"\.broadcast (.+)"))
async def broadcast_message(event):
    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    message = event.pattern_match.group(1).strip()
    
    if not message:
        await event.edit("❌ Please provide a message to broadcast.")
        return

    await event.edit("📢 **Broadcasting message...**")

    count = 0
    async for dialog in BOT.iter_dialogs():
        if dialog.is_user and not dialog.entity.bot:  # Send only to real users
            try:
                await BOT.send_message(dialog.id, message)
                count += 1
                await asyncio.sleep(1)  # Avoid rate limits
            except Exception as e:
                print(f"Failed to send message to {dialog.id}: {str(e)}")

    await event.edit(f"✅ **Broadcast complete! Sent to {count} users.**")
    
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, ChannelPrivateError

@BOT.on(events.NewMessage(pattern=r"\.dm(?:\s+@?(\S+))?\s*(.*)"))
async def dm_user(event):
    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    args = event.pattern_match
    username = args.group(1)  # Extract username if provided
    message = args.group(2).strip()  # Extract message if provided
    default_message = f"Hi There {BOT_OWNER} This Side 😄"

    if event.is_reply and not username:  
        # If it's a reply and no username is given, DM the replied user
        reply_msg = await event.get_reply_message()
        user_id = reply_msg.sender_id
    elif username:  
        # If a username is provided, fetch the user
        try:
            user = await BOT.get_entity(username)
            user_id = user.id
        except:
            await event.edit("❌ **User not found!**")
            return
    else:
        await event.edit("❌ **Please reply to a message or mention a username.**")
        return

    # Use default message if none is provided
    if not message:
        message = default_message

    try:
        await BOT.send_message(user_id, message)
        await event.edit(f"✅ **Message sent successfully!**\n📩 `{message}`")
    except Exception as e:
        await event.edit(f"❌ **Failed to send message:** `{str(e)}`")



        
from telethon.tl.functions.messages import UpdatePinnedMessageRequest

import random

import random

# Dictionary to track users who are being spammed
active_abuse_targets = {}

import random

# Dictionary to track users who are being spammed
active_abuse_targets = {}

@BOT.on(events.NewMessage(pattern=r"\.chudai"))
async def start_sending_abuse(event):
    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    chat_id = event.chat_id
    abuse_target = None

    if event.is_group:
        if event.is_reply:
            reply_msg = await event.get_reply_message()
            abuse_target = f"[{reply_msg.sender.first_name}](tg://user?id={reply_msg.sender_id})"
        else:
            abuse_target = f"[{event.sender.first_name}](tg://user?id={event.sender_id})"

    if chat_id in active_abuse_targets:
        await event.edit("❌ **Abuses are already being sent in this chat!**")
        return

    await event.edit("🔞 **Starting abuse spam... Use `.rukja` to stop.**")
    active_abuse_targets[chat_id] = True

    while chat_id in active_abuse_targets:
        try:
            abuse = random.choice(abuses)  # Pick a random abuse
            
            if event.is_group:
                message = f"{abuse_target}, {abuse}"  # Tag user in groups
            else:
                message = abuse  # No tag in private chats
            
            await BOT.send_message(chat_id, message)  # Send abuse message
            await asyncio.sleep(2)  # Small delay to avoid spam detection
        except Exception as e:
            print(f"Error while sending abuse: {e}")
            break

@BOT.on(events.NewMessage(pattern=r"\.rukja"))
async def stop_sending_abuse(event):
    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    chat_id = event.chat_id

    if chat_id in active_abuse_targets:
        del active_abuse_targets[chat_id]
        await event.edit("🛑 **Abuse spam stopped!**")
    else:
        await event.edit("❌ **No abuse spam is active in this chat.**")

from googletrans import Translator

translator = Translator()

from googletrans import Translator

translator = Translator()

@BOT.on(events.NewMessage(pattern=r"\.translate(?:\s+(.+))?"))
async def translate_message(event):
    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    user_input = event.pattern_match.group(1)  # Extracts the text if given
    original_text = None

    if event.is_reply:
        # If it's a reply, use the replied message
        reply_msg = await event.get_reply_message()
        original_text = reply_msg.text
    elif user_input:
        # If message is given directly, use that
        original_text = user_input

    if not original_text:
        await event.edit("❌ **Reply to a message or provide text to translate!**")
        return

    try:
        translated = translator.translate(original_text, dest="en")
        detected_lang = translated.src.upper()
        translated_text = translated.text

        await event.edit(f"🌍 **Translated from {detected_lang}**\n\n🔤 **Original:** `{original_text}`\n📖 **Translation:** `{translated_text}`")
    except Exception as e:
        await event.edit(f"❌ **Translation failed:** `{str(e)}`")
        
import asyncio

bot_status = "online"  # Default status is online (no auto-replies)

import asyncio

bot_status = "online"  # Default status

@BOT.on(events.NewMessage(pattern=r"\.status(?:\s*(\w+))?"))
async def set_status(event):
    global bot_status

    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    status_input = event.pattern_match.group(1)  # Extract argument

    if not status_input:
        await event.edit(f"ℹ **Current Status:** `{bot_status.capitalize()}`")
        return

    status_input = status_input.lower()

    if status_input not in ["online", "offline"]:
        await event.edit("❌ **Invalid status! Use `.status online` or `.status offline`.**")
        return

    bot_status = status_input
    await event.edit(f"✅ **Status set to:** `{bot_status.capitalize()}`")

@BOT.on(events.NewMessage)
async def auto_reply_status(event):
    global bot_status

    # Don't reply if status is online, message is from bot, or from admin
    if bot_status == "online" or event.sender.bot or event.sender_id == ADMIN_ID:
        return

    # Only reply if it's a private chat (DM)
    if event.is_private:
        await asyncio.sleep(10)  # Wait 10 seconds before replying

        try:
            await event.reply(f"Hi There This Is An Automated Reply🤖, Shriram Is Offline. Still, If You Want To Contact Then DM @Rolexthefixerbot🙂")
        except Exception as e:
            print(f"Error sending auto-reply: {e}")


        
@BOT.on(events.NewMessage(pattern=r"\.instaid"))
async def send_channel_link(event):
    await event.edit("🔗 **Follow On Insta:** [Vulpix Bot🇮🇳](www.instagram.com/rolexthefixer)")

import requests
from bs4 import BeautifulSoup
from googlesearch import search

def get_direct_answer(query):
    """Fetches a direct answer from Google (if available)."""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try different Google answer boxes (Instant Answer, Knowledge Graph, etc.)
    answer = soup.find("div", class_="BNeawe iBp4i AP7Wnd")  # Regular Google Answer Box
    if not answer:
        answer = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")  # Alternative Answer Box
    if not answer:
        return None  # No direct answer found

    return answer.text.strip()
    
from duckduckgo_search import DDGS

@BOT.on(events.NewMessage(pattern=r"\.search (.+)"))
async def duckduckgo_search(event):
    query = event.pattern_match.group(1).strip()

    if not query:
        await event.edit("❌ **Please provide a search query!**")
        return

    await event.edit(f"🔍 **Searching DuckDuckGo for:** `{query}`...")

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            await event.edit("❌ **No results found!**")
            return

        response = f"🔎 **Search Results for:** `{query}`\n\n"
        for i, result in enumerate(results, start=1):
            response += f"🔹 [{i}] [{result['title']}]({result['href']})\n"

        await event.edit(response, link_preview=False)

    except Exception as e:
        await event.edit(f"❌ **Search failed:** `{str(e)}`")



import requests
from telethon import events

# Replace with your actual Gemini API Key
GEMINI_API_KEY = "AIzaSyANqyFr4My12-obl6IQr7dds9K7WOYqa30"
GEMINI_MODEL = "gemini-1.5-flash-002"  # Supported model

def ask_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if "candidates" in data and "content" in data["candidates"][0]:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        elif "error" in data:
            return f"❌ API Error: {data['error'].get('message', 'Unknown error')}"
        else:
            return "⚠️ Unexpected response format from Gemini API."

    except Exception as e:
        return f"❌ Error: {str(e)}"

@BOT.on(events.NewMessage(pattern=r"^\.ai (.+)"))
async def ai_command(event):
    prompt = event.pattern_match.group(1).strip()

    if not prompt:
        await event.reply("⚠️ Please provide a question after `.ai`")
        return

    loading_message = await event.reply("⏳ Generating response...")  # Show loading message
    
    response = ask_gemini(prompt)  # Get AI response
    
    await loading_message.edit(f"🤖 **AI Response:**\n\n{response}")  # Edit message with response

import requests
from telethon import events

WEATHER_API_KEY = "a368ca66c8dd935f59461f02c74effea"  # Your OpenWeatherMap API key

@BOT.on(events.NewMessage(pattern=r"\.wthr (.+)"))
async def fetch_weather(event):
    city = event.pattern_match.group(1).strip()

    if not city:
        await event.reply("❌ **Please provide a city name!**")
        return

    try:
        # Fetch weather data from OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()

        if response.get("cod") != 200:
            await event.reply(f"❌ **Could not fetch weather data for** `{city}`.")
            return

        # Extract required weather details
        weather_description = response["weather"][0]["description"].capitalize()
        temperature = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]
        country = response["sys"]["country"]
        city_name = response["name"]

        # Format the weather report
        weather_report = (
            f"🌍 **Weather in {city_name}, {country}:**\n\n"
            f"☀️ **Condition:** {weather_description}\n"
            f"🌡 **Temperature:** {temperature}°C\n"
            f"💧 **Humidity:** {humidity}%\n"
            f"💨 **Wind Speed:** {wind_speed} m/s"
        )

        await event.reply(weather_report)

    except Exception as e:
        await event.reply(f"❌ **Error fetching weather data:** `{str(e)}`")
        
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, PhoneNumberFormat
from telethon import events

def get_location_info():
    """Fetch geolocation info using IP-based lookup (example using ipinfo.io API)."""
    ip_api_url = "https://ipinfo.io"
    try:
        response = requests.get(ip_api_url)
        data = response.json()
        location = data.get("loc", "Not available")
        ip_address = data.get("ip", "Not available")

        # Split latitude and longitude if location is available
        latitude, longitude = location.split(',') if location != "Not available" else ("Not available", "Not available")

        return latitude, longitude, ip_address
    except requests.exceptions.RequestException:
        return "Not available", "Not available", "Not available"

def phone_number_info(phone_number: str) -> str:
    """Fetch detailed phone number information."""
    try:
        parsed_number = phonenumbers.parse(phone_number)

        # Extract details
        region = geocoder.description_for_number(parsed_number, 'en')
        timezone_zones = timezone.time_zones_for_number(parsed_number)
        isp = carrier.name_for_number(parsed_number, 'en')
        national_format = phonenumbers.format_number(parsed_number, PhoneNumberFormat.NATIONAL)
        international_format = phonenumbers.format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)
        number_type = phonenumbers.number_type(parsed_number)
        possible_number = phonenumbers.is_possible_number(parsed_number)
        number_length = len(str(parsed_number.national_number))
        country = geocoder.region_code_for_number(parsed_number)

        # Determine number type
        if number_type == phonenumbers.PhoneNumberType.MOBILE:
            number_type_desc = "📱 Mobile Number"
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE:
            number_type_desc = "☎️ Fixed Line Number"
        elif number_type == phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE:
            number_type_desc = "🔄 Fixed or Mobile Number"
        else:
            number_type_desc = "❓ Unknown Number Type"

        # Fetch geolocation info
        latitude, longitude, ip_address = get_location_info()

        # Format response
        info = (
            f"📞 **Phone Number Information**\n\n"
            f"🌍 **Region:** {region}\n"
            f"🕒 **Time Zone:** {', '.join(timezone_zones)}\n"
            f"📶 **Carrier:** {isp}\n"
            f"🔢 **National Format:** {national_format}\n"
            f"🌎 **International Format:** {international_format}\n"
            f"🇺🇳 **Country Code:** {country}\n"
            f"✅ **Valid Number:** {possible_number}\n"
            f"🔢 **Number Length:** {number_length}\n"
            f"{number_type_desc}\n\n"
            f"🌍 **Location Data (IP-Based)**\n"
            f"📍 **Latitude:** {latitude}\n"
            f"📍 **Longitude:** {longitude}\n"
            f"💻 **IP Address:** {ip_address}"
        )

        return info

    except phonenumbers.phonenumberutil.NumberParseException:
        return "❌ **Invalid phone number! Please provide a valid number with country code.**"

@BOT.on(events.NewMessage(pattern=r"\.phoneinfo (\+?\d+)"))
async def handle_phone_info(event):
    """Handles .phoneinfo command to fetch number details."""
    phone_number = event.pattern_match.group(1)

    if not phone_number:
        await event.reply("❌ **Please provide a valid phone number.**")
        return

    result = phone_number_info(phone_number)
    await event.reply(f"```{result}```")
    
import ipapi
import asyncio
from telethon import events

def get_ip_info(ip_address):
    """Fetch and format IP geolocation details using ipapi."""
    try:
        location = ipapi.location(ip_address)

        if not location or "error" in location:
            return "❌ **Invalid IP Address or Data Unavailable.**"

        # Format response with emojis
        info_message = "🌍 **IP Address Information**\n\n"
        
        emojis = {
            "ip": "🌐", 
            "network": "🌐", 
            "version": "💻", 
            "city": "🏙️", 
            "region": "🌍", 
            "region_code": "🔠", 
            "country": "🇺🇳", 
            "country_name": "🌏", 
            "country_code": "🔤", 
            "country_code_iso3": "🔤", 
            "country_capital": "🏛️", 
            "country_tld": "🌐", 
            "continent_code": "🌍", 
            "in_eu": "🇪🇺", 
            "postal": "📬", 
            "latitude": "📍", 
            "longitude": "📍", 
            "timezone": "🕰️", 
            "utc_offset": "⏱️", 
            "country_calling_code": "📞", 
            "currency": "💰", 
            "currency_name": "💰", 
            "languages": "🗣️", 
            "country_area": "🗺️", 
            "country_population": "👥", 
            "asn": "🔌", 
            "org": "🏢"
        }

        for key, value in location.items():
            emoji = emojis.get(key, "❓")  # Default emoji if key isn't in the dictionary
            info_message += f"{emoji} **{key.capitalize()}**: {value}\n"

        return info_message

    except Exception as e:
        return f"❌ **An error occurred:** `{str(e)}`"

@BOT.on(events.NewMessage(pattern=r"\.ip (\S+)"))
async def handle_ip_lookup(event):
    """Handles .ip command to fetch geolocation details of an IP."""
    ip_address = event.pattern_match.group(1)

    if not ip_address:
        await event.reply("❌ **Please provide a valid IP address!**\n\n📌 Usage: `.ip <ip_address>`")
        return

    # Send initial lookup message
    lookup_message = await event.reply(f"🔍 **Looking up IP:** `{ip_address}`...")

    await asyncio.sleep(1)  # Simulate processing delay

    # Fetch IP information
    result = get_ip_info(ip_address)

    # Update message with IP info
    await lookup_message.edit(f"```{result}```")
    
@BOT.on(events.NewMessage(pattern=r"^\.setbio(?:\s+(.+))?"))
async def set_bio(event):
    if event.sender_id != ADMIN_ID:
        return  # Only the admin can use this command

    bio = event.pattern_match.group(1)  # Extract bio text

    if not bio:
        await event.reply("❗ **Please provide a new bio after** `.setbio <your bio>`.")
        return

    try:
        await BOT(UpdateProfileRequest(about=bio))
        await event.reply(f"✅ **Bio updated successfully to:** `{bio}`")
    except Exception as e:
        await event.reply(f"❌ **Failed to update bio. Error:** `{str(e)}`")

import asyncio
from telethon import events
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.errors import ChatAdminRequiredError


@BOT.on(events.NewMessage(pattern=r'\.pin(.*)'))
async def pin_message(event):
    if event.sender_id != ADMIN_ID:
        return

    if event.is_reply:
        reply_message = await event.get_reply_message()
        try:
            await BOT(UpdatePinnedMessageRequest(event.chat_id, reply_message.id, silent=True))
            notification = await event.edit('✅ **Message pinned!**')
            await asyncio.sleep(2.3)
            await notification.delete()
        except ChatAdminRequiredError:
            await event.reply('🛑 **I need admin rights to pin messages!** 🚫')
        except Exception as e:
            await event.reply(f'❌ **Error:** `{str(e)}`')

    else:
        message_to_pin = event.pattern_match.group(1).strip()
        if message_to_pin:
            try:
                if message_to_pin.isdigit():
                    msg = await BOT.get_messages(event.chat_id, ids=int(message_to_pin))
                else:
                    messages = await BOT.get_messages(event.chat_id, search=message_to_pin, limit=1)
                    msg = messages[0] if messages else None

                if msg:
                    await BOT(UpdatePinnedMessageRequest(event.chat_id, msg.id, silent=True))
                    notification = await event.edit('✅ **Message pinned!**')
                    await asyncio.sleep(2.5)
                    await notification.delete()
                else:
                    await event.edit('⚠️ **Could not find the message to pin.**')

            except ChatAdminRequiredError:
                await event.edit('🛑 **I need admin rights to pin messages!** 🚫')
            except Exception as e:
                await event.edit(f'❌ **Error:** `{str(e)}`')

        else:
            await event.edit('⚠️ **Please reply to a message or provide a valid message ID or text to pin.**')

@BOT.on(events.NewMessage(pattern=r'\.unpin'))
async def unpin_message(event):
    if event.sender_id != ADMIN_ID:
        return

    try:
        await BOT(UpdatePinnedMessageRequest(peer=event.chat_id, id=0, unpin=True))  # Unpin all messages
        notification = await event.reply('✅ **Unpinned the latest pinned message!**')
        await asyncio.sleep(2.3)
        await notification.delete()
    except ChatAdminRequiredError:
        await event.reply('🛑 **I need admin rights to unpin messages!** 🚫')
    except Exception as e:
        await event.reply(f'❌ **Error:** `{str(e)}`')

@BOT.on(events.NewMessage(pattern=r"\.pline"))
async def send_pickup_line(event):
    pickup_lines = [
        "Are you a magician? Because whenever I look at you, everyone else disappears.",
        "Are you French? Because Eiffel for you.",
        "Do you have a map? I keep getting lost in your eyes.",
        "Is your name Google? Because you have everything I'm searching for.",
        "Are you a time traveler? Because I see you in my future.",
        "If you were a vegetable, you’d be a cute-cumber.",
        "Do you have a name, or can I call you mine?",
        "Are you a camera? Because every time I look at you, I smile.",
        "Do you have a Band-Aid? Because I just scraped my knee falling for you.",
        "Is your name Wi-Fi? Because I’m really feeling a connection.",
        "Do you believe in love at first sight, or should I walk by again?",
        "Are you a parking ticket? Because you’ve got FINE written all over you.",
        "If beauty were time, you’d be an eternity.",
        "Are you a loan from a bank? Because you have my interest!",
        "Are you a light bulb? Because you brighten up my day.",
        "Are you a beaver? Because daaaaam!",
        "Are you a campfire? Because you’re hot and I want s’more.",
        "Do you have a sunbeam in your pocket? Because you light up my day.",
        "Are you made of copper and tellurium? Because you’re Cu-Te.",
        "Is your name Chapstick? Because you’re da balm.",
        "Can I follow you home? Because my parents always told me to follow my dreams.",
        "If kisses were snowflakes, I’d send you a blizzard.",
        "Are you a star? Because your beauty lights up the night.",
        "Are you an angel? Because heaven is missing one.",
        "Are you a sunrise? Because you make my morning brighter.",
        "Are you the ocean? Because I’m lost at sea.",
        "Are you a superhero? Because you just saved my day.",
        "Are you a piece of art? Because you’re priceless.",
        "Do you believe in fate? Because I think we were meant to meet.",
        "Are you lightning? Because you just struck my heart.",
        "Are you a cat? Because you’re purr-fect.",
        "Are you a dictionary? Because you add meaning to my life.",
        "Is your name Starbucks? Because I like you a latte.",
        "Are you a vampire? Because you’ve got me under your spell.",
        "Do you have a quarter? Because I want to call my mom and tell her I met the one.",
        "Are you a mirror? Because I see myself in you.",
        "If you were a fruit, you’d be a fineapple.",
        "Are you the wind? Because you’ve just swept me off my feet.",
        "Are you a marathon? Because you’ve just taken my breath away.",
        "Are you a constellation? Because you’ve lit up my darkest nights.",
        "Are you a cupcake? Because you’re the sweetest thing here.",
        "Are you a butterfly? Because you’ve got my heart fluttering.",
        "Is your heart a lock? Because I’ve got the key.",
        "Are you gravity? Because you’ve just made me fall for you.",
        "Are you the North Star? Because you guide me home.",
        "Is your love a flame? Because you’ve set my heart on fire.",
        "Are you an eclipse? Because you’ve just shadowed everyone else.",
        "Are you a locksmith? Because you’ve just unlocked my heart.",
        "Are you a gardener? Because you’ve just planted yourself in my heart.",
        "Are you a jewel? Because you’re truly priceless."
    ]
    
    random_line = random.choice(pickup_lines)
    await event.reply(f"💬 **Pickup Line:**\n\n_{random_line}_")
    
           
       
           
               
                   
                       
                           
                                   

        

      
                  
               
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