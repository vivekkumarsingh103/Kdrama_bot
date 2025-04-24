from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
import os

# Get secrets from Railway environment variables
API_ID = int(os.getenv("27169610"))
API_HASH = os.getenv("5a7c36388def1b135c277a839cf11837")
BOT_TOKEN = os.getenv("7538767807:AAFOuoLMq5E4SLwgVvPPHILNhZrgn8hNcwg")
CHANNEL = os.getenv("CHANNEL", "movieswovies")
FALLBACK_GROUP_LINK = os.getenv("FALLBACK_GROUP_LINK", "https://t.me/movieswovies")

app = Client("kdrama_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to K-Drama Bot! Just type the name of the drama you want.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def search_drama(client, message: Message):
    query = message.text.lower()
    results = []

    async for msg in app.search_messages(CHANNEL, query):
        if msg.video:
            results.append(msg)

    if results:
        for vid in results:
            await vid.copy(chat_id=message.chat.id)
            await asyncio.sleep(1)  # To prevent flood wait
    else:
        await message.reply(
            f"Drama not found. Please join our group {FALLBACK_GROUP_LINK} and type the name. We'll upload it soon!"
        )

app.run()
