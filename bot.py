import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from config import BOT_TOKEN, CHANNEL_ID
from db import init_db, save_post, search_posts

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# 📌 Сохраняем новые посты из канала
@dp.channel_post()
async def channel_post_handler(message: Message):
    if message.text:
        await save_post(message.message_id, message.text)

# 🔍 Поиск по запросу пользователя
@dp.message(F.text)
async def search_handler(message: Message):
    query = message.text.strip()
    results = await search_posts(query)

    if not results:
        await message.answer("❌ Ничего не найдено")
        return

    for msg_id, in results[:5]:  # максимум 5 постов
        await bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_ID,
            message_id=msg_id
        )

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
