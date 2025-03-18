import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import os
import psycopg2
from image_processing import extract_text, parse_wood_data

API_TOKEN = "7768373361:AAGwbnauI9QF52yrP_lUaj1qWySeWr1bkgs"
DB_CONNECTION = "postgresql://neondb_owner:npg_S5FME2mLobIN@ep-round-lab-a5x3kfeb-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Подключение к БД
def save_to_db(user_id, wood_data):
    conn = psycopg2.connect(DB_CONNECTION)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO logs (user_id, image_path, status) VALUES (%s, %s, %s) RETURNING id", 
                   (user_id, "image_path_placeholder", "confirmed"))
    log_id = cursor.fetchone()[0]
    
    for entry in wood_data:
        cursor.execute("""
            INSERT INTO wood_entries (log_id, wood_type, length_cm, diameter_cm, quantity, volume_m3)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (log_id, entry['wood_type'], entry['length_cm'], entry['diameter_cm'], entry['quantity'], entry['volume_m3']))
    
    conn.commit()
    cursor.close()
    conn.close()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📷 Отправить бланк"))
    await message.answer("Привет! Отправь фото бланка сортировки для обработки.", reply_markup=keyboard)

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    
    downloaded_file = await bot.download_file(file_path)
    image_path = f"temp/{photo.file_id}.jpg"
    os.makedirs("temp", exist_ok=True)
    with open(image_path, "wb") as new_file:
        new_file.write(downloaded_file.read())
    
    extracted_text = extract_text(image_path)
    wood_data = parse_wood_data(extracted_text)
    
    if wood_data:
        response_text = "📊 Обнаружены следующие данные:\n"
        for entry in wood_data:
            response_text += (f"\nПорода: {entry['wood_type']}\n"
                              f"Длина: {entry['length_cm']} см\n"
                              f"Диаметр: {entry['diameter_cm']} см\n"
                              f"Количество: {entry['quantity']} шт\n"
                              f"Объем: {entry['volume_m3']} м³\n")
        await message.answer(response_text)
    else:
        await message.answer("❌ Не удалось распознать данные. Попробуйте отправить более четкое фото.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
