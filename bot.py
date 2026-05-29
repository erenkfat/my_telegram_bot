
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import json
import os

BOT_TOKEN = "7977638851:AAFA9OdETtQubfY4-_nmyNubxlb7pjk2Hys"

SETTINGS_FILE = "settings.json"
WEATHER_CITIES = "cities.json"

settings = {"lang_from": "en", "lang_to": "ar"}
saved_cities = []

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE) as f:
        settings = json.load(f)
if os.path.exists(WEATHER_CITIES):
    with open(WEATHER_CITIES) as f:
        saved_cities = json.load(f)

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def save_cities():
    with open(WEATHER_CITIES, "w") as f:
        json.dump(saved_cities, f)

SONGS = {
    "trending": [
        "Sabrina Carpenter - Espresso",
        "Billie Eilish - What Was I Made For",
        "SZA - Snooze",
        "Olivia Rodrigo - Vampire",
        "The Weeknd - Blinding Lights",
        "Dua Lipa - Dance The Night",
        "Taylor Swift - Cruel Summer",
        "Harry Styles - As It Was",
        "Miley Cyrus - Flowers",
        "Doja Cat - Paint The Town Red",
        "Tate McRae - Greedy",
        "Drake - One Dance",
        "Ed Sheeran - Shape of You",
        "Adele - Easy On Me",
        "Coldplay - Yellow",
        "Imagine Dragons - Believer",
        "Eminem - Lose Yourself",
        "Rihanna - Diamonds",
        "Bruno Mars - Leave The Door Open",
        "Post Malone - Circles",
        "Kendrick Lamar - Not Like Us",
        "Chappell Roan - Good Luck Babe",
        "Sabrina Carpenter - Please Please Please",
        "Tyla - Water",
        "Tommy Richman - Million Dollar Baby",
        "Jack Harlow - Lovin On Me",
        "Teddy Swims - Lose Control",
        "Benson Boone - Beautiful Things",
        "Noah Kahan - Stick Season",
        "Zach Bryan - I Remember Everything",
    ],
    "arabic": [
        "Fairuz - Saalouni El Nas",
        "Umm Kulthum - Enta Omri",
        "Abdel Halim Hafez - Ahwak",
        "Amr Diab - Tamally Maak",
        "Nancy Ajram - Ah W Noss",
        "Mohamed Mounir - Shababeek",
        "Sherine - Masha'er",
        "Elissa - Hobak Wajaa",
    ],
    "classic": [
        "Queen - Bohemian Rhapsody",
        "Michael Jackson - Billie Jean",
        "The Beatles - Hey Jude",
        "Eagles - Hotel California",
        "Pink Floyd - Comfortably Numb",
        "Led Zeppelin - Stairway to Heaven",
        "Bob Marley - No Woman No Cry",
    ]
}

LYRICS = {
    "Sabrina Carpenter - Espresso": "Now he's thinkin' bout me every night, oh\nIs it that sweet? I guess so\nSay you can't sleep, baby I know\nThat's that me, espresso",
    "Billie Eilish - What Was I Made For": "I used to float, now I just fall down\nI used to know, but I'm not sure now\nWhat was I made for?",
    "Taylor Swift - Cruel Summer": "Fever dream high in the quiet of the night\nYou know that I caught it\nBad bad boy, shiny toy with a price\nYou know that I bought it",
    "The Weeknd - Blinding Lights": "I said, ooh, I'm blinded by the lights\nNo, I can't sleep until I feel your touch",
    "Queen - Bohemian Rhapsody": "Is this the real life? Is this just fantasy?\nCaught in a landslide, no escape from reality",
    "Fairuz - Saalouni El Nas": "Saalouni el nas, saalouni el nas\nAn habibi, an habibi",
    "Umm Kulthum - Enta Omri": "Enta omri, enta habibi\nEnta elli khala't albi",
}

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
--- لوحة الاوامر ---

/start - تشغيل
/commands - القائمة

--- اغاني ---
/rsong - اغنية عشوائية
/playrsong - ارسال اغنية عشوائية
/searchsong اسم - بحث

--- طقس ---
/weather مدينة - طقس
/addcity مدينة - حفظ مدينة
/mycities - مدني
/quickweather - طقس مدني

--- قرآن ---
/quran - اية عشوائية
/playquran - السورة كاملة
/searchquran كلمة - بحث

--- ترجمة ---
/translate نص - ترجمة
/setlang - تغيير اللغة
/lang - اللغة الحالية
/setlang ar en - اختصار سريع

/calc - حاسبة
"""
    await update.message.reply_text(msg)

# ========== الاغاني ==========
last_song = None

async def rsong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_song
    all_songs = SONGS["trending"] + SONGS["arabic"] + SONGS["classic"]
    last_song = random.choice(all_songs)

    keyboard = [
        [InlineKeyboardButton("Lyrics", callback_data="lyrics")],
        [InlineKeyboardButton("بحث يوتيوب", callback_data="youtube")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"{last_song}", reply_markup=reply_markup)

async def playrsong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_song
    all_songs = SONGS["trending"] + SONGS["arabic"] + SONGS["classic"]
    last_song = random.choice(all_songs)

    keyboard = [
        [InlineKeyboardButton("Lyrics", callback_data="lyrics")],
        [InlineKeyboardButton("بحث يوتيوب", callback_data="youtube")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"{last_song}", reply_markup=reply_markup)

async def searchsong(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /searchsong Sabrina")
        return

    keyword = " ".join(context.args).lower()
    results = []
    for cat in SONGS.values():
        for song in cat:
            if keyword in song.lower():
                results.append(song)

    if results:
        await update.message.reply_text("نتائج البحث:\n\n" + "\n".join(results[:10]))
    else:
        await update.message.reply_text("لا توجد نتائج")

# ========== الطقس ==========
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /weather Riyadh")
        return
    city = context.args[0]
    try:
        r = requests.get(f"https://wttr.in/{city}?format=%l:+%c+%t+%h+%w", timeout=5)
        await update.message.reply_text(f"الطقس: {r.text}")
    except:
        await update.message.reply_text("خطا في جلب الطقس")

async def addcity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /addcity Riyadh")
        return
    city = context.args[0]
    if city not in saved_cities:
        saved_cities.append(city)
        save_cities()
        await update.message.reply_text(f"تم حفظ {city}")
    else:
        await update.message.reply_text("المدينة محفوظة مسبقا")

async def mycities(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if saved_cities:
        await update.message.reply_text("مدنك:\n" + "\n".join(saved_cities))
    else:
        await update.message.reply_text("لا توجد مدن محفوظة. استخدم /addcity")

async def quickweather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not saved_cities:
        await update.message.reply_text("احفظ مدن اولا: /addcity Riyadh")
        return

    msg = "طقس مدنك:\n\n"
    for city in saved_cities:
        try:
            r = requests.get(f"https://wttr.in/{city}?format=%l:+%c+%t", timeout=3)
            msg += r.text + "\n"
        except:
            msg += f"{city}: خطا\n"

    await update.message.reply_text(msg)

# ========== القرآن ==========
last_quran = None

async def quran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_quran
    try:
        r = requests.get("https://api.alquran.cloud/v1/ayah/random/ar", timeout=5)
        data = r.json()['data']
        last_quran = data

        keyboard = [
            [InlineKeyboardButton("السورة كاملة نص", callback_data="full_surah_text")],
            [InlineKeyboardButton("السورة كاملة صوت", callback_data="full_surah_audio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"{data['text']}\n\n- {data['surah']['name']}",
            reply_markup=reply_markup
        )
    except:
        await update.message.reply_text("خطا")

async def playquran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not last_quran:
        await update.message.reply_text("استخدم /quran اولا")
        return

    try:
        surah_num = last_quran['surah']['number']
        r = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_num}/ar", timeout=10)
        ayahs = r.json()['data']['ayahs']

        text = "\n".join([f"{a['numberInSurah']}. {a['text']}" for a in ayahs])

        if len(text) > 4000:
            for i in range(0, len(text), 4000):
                await update.message.reply_text(text[i:i+4000])
        else:
            await update.message.reply_text(f"{last_quran['surah']['name']}\n\n{text}")
    except:
        await update.message.reply_text("خطا في جلب السورة")

async def searchquran(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /searchquran رحمة")
        return

    keyword = " ".join(context.args)
    try:
        r = requests.get(f"https://api.alquran.cloud/v1/search/{keyword}/all/ar", timeout=5)
        matches = r.json()['data']['matches'][:5]

        if matches:
            msg = f"نتائج: {keyword}\n\n"
            for m in matches:
                msg += f"{m['text']}\n- {m['surah']['name']}\n\n"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("لا نتائج")
    except:
        await update.message.reply_text("خطا")

# ========== الترجمة ==========
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /translate Hello")
        return

    text = " ".join(context.args)
    pair = f"{settings['lang_from']}|{settings['lang_to']}"

    try:
        r = requests.get(f"https://api.mymemory.translated.net/get?q={text}&langpair={pair}", timeout=5)
        result = r.json()['responseData']['translatedText']
        await update.message.reply_text(f"ترجمة: {result}")
    except:
        await update.message.reply_text("خطا في الترجمة")

async def setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and len(context.args) == 2:
        settings['lang_from'] = context.args[0]
        settings['lang_to'] = context.args[1]
        save_settings()
        await update.message.reply_text(f"تم: {settings['lang_from']} --> {settings['lang_to']}")
        return

    keyboard = [
        [InlineKeyboardButton("English to Arabic", callback_data="lang_en_ar")],
        [InlineKeyboardButton("Arabic to English", callback_data="lang_ar_en")],
        [InlineKeyboardButton("English to French", callback_data="lang_en_fr")],
        [InlineKeyboardButton("English to Spanish", callback_data="lang_en_es")],
        [InlineKeyboardButton("English to German", callback_data="lang_en_de")],
        [InlineKeyboardButton("Arabic to French", callback_data="lang_ar_fr")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر اتجاه الترجمة:\nاو استخدم: /setlang ar en", reply_markup=reply_markup)

async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"الترجمة: {settings['lang_from']} --> {settings['lang_to']}")

# ========== الازرار ==========
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "lyrics":
        if last_song and last_song in LYRICS:
            await query.message.reply_text(f"Lyrics:\n\n{LYRICS[last_song]}")
        else:
            await query.message.reply_text(f"لا يوجد Lyrics متاحة.\nابحث: https://genius.com/search?q={last_song.replace(' ', '+')}")

    elif query.data == "youtube":
        if last_song:
            search = last_song.replace(' ', '+')
            await query.message.reply_text(f"https://www.youtube.com/results?search_query={search}")

    elif query.data == "full_surah_text":
        if last_quran:
            try:
                surah_num = last_quran['surah']['number']
                r = requests.get(f"https://api.alquran.cloud/v1/surah/{surah_num}/ar", timeout=10)
                ayahs = r.json()['data']['ayahs']
                text = "\n".join([f"{a['numberInSurah']}. {a['text']}" for a in ayahs])

                if len(text) > 4000:
                    for i in range(0, len(text), 4000):
                        await query.message.reply_text(text[i:i+4000])
                else:
                    await query.message.reply_text(f"{last_quran['surah']['name']}\n\n{text}")
            except:
                await query.message.reply_text("خطا")

    elif query.data == "full_surah_audio":
        if last_quran:
            surah_num = last_quran['surah']['number']
            audio_url = f"https://cdn.islamic.network/quran/audio/128/ar.alafasy/{surah_num}.mp3"
            await query.message.reply_text(f"استمع للسورة:\n{audio_url}")

    elif query.data.startswith("lang_"):
        parts = query.data.replace("lang_", "").split("_")
        settings['lang_from'] = parts[0]
        settings['lang_to'] = parts[1]
        save_settings()
        await query.message.reply_text(f"تم: {parts[0]} --> {parts[1]}")

async def calc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("استخدم: /calc 5+3")
        return
    try:
        result = eval("".join(context.args))
        await update.message.reply_text(f"= {result}")
    except:
        await update.message.reply_text("خطا")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("اهلا! اكتب /commands للقائمة")

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("commands", commands))
app.add_handler(CommandHandler("rsong", rsong))
app.add_handler(CommandHandler("playrsong", playrsong))
app.add_handler(CommandHandler("searchsong", searchsong))
app.add_handler(CommandHandler("weather", weather))
app.add_handler(CommandHandler("addcity", addcity))
app.add_handler(CommandHandler("mycities", mycities))
app.add_handler(CommandHandler("quickweather", quickweather))
app.add_handler(CommandHandler("quran", quran))
app.add_handler(CommandHandler("playquran", playquran))
app.add_handler(CommandHandler("searchquran", searchquran))
app.add_handler(CommandHandler("translate", translate))
app.add_handler(CommandHandler("setlang", setlang))
app.add_handler(CommandHandler("lang", lang))
app.add_handler(CommandHandler("calc", calc))
app.add_handler(CallbackQueryHandler(button))

print("البوت يعمل...")
app.run_polling()
