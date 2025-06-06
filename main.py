import os
import asyncio
from pyrogram import Client
from pymongo import MongoClient

API_ID = int(os.getenv("API_ID", 28712296))
API_HASH = os.getenv("API_HASH", "25a96a55e729c600c0116f38564a635f")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7462333733:AAGTipaAqOSqPORNOuwERnEHBQGLoPbXxfE")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://lucas:00700177@lucas.miigb0j.mongodb.net/?retryWrites=true&w=majority&appName=lucas")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002115202685")  # @moviestera1

client = MongoClient(MONGO_URI)
db = client["lucas"]
collection = db["Telegram_files"]

app = Client("fetch_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message()
async def handler(_, __): pass  # No need to handle messages

async def fetch_and_store():
    async with app:
        async for message in app.get_chat_history(int(CHANNEL_ID)):
            if message.caption:
                first_line = message.caption.strip().split("\n")[0]
                exists = collection.find_one({"message_id": message.id})
                if not exists:
                    data = {
                        "message_id": message.id,
                        "file_name": first_line,
                        "text": message.caption,
                        "telegram_link": f"https://t.me/moviestera1/{message.id}"
                    }
                    collection.insert_one(data)
        print("✅ Done fetching and storing messages.")

if __name__ == "__main__":
    asyncio.run(fetch_and_store())