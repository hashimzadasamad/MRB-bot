from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from main import MovieRecommendationSystem
import os

tg_key = "7046458454:AAHaCL3w1mtoig7L0Xwi9TqJ8ycBfsdcGkg"
storage = MemoryStorage()

bot = Bot(token=tg_key)
dp = Dispatcher(bot, storage=storage)

recommender = MovieRecommendationSystem("movies.csv")
recommender.preprocess_data()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Hi, welcome to MRB (Movies Recommendation Bot). For getting recommendations, please use /recommend followed by the movie name or genre you would like to see.')

@dp.message_handler(commands=['recommend'])
async def recommend_movies(message: types.Message):
    movie_name = " ".join(message.text.split()[1:]) if len(message.text.split()) > 1 else None
    if not movie_name:
        await message.reply("Please provide a movie name after the /recommend command!")
        return


    recommendations = recommender.recommend_movies(movie_name)
    if recommendations is None:
        await message.reply("Sorry, no recommendations found for that movie!")
        return

    await message.reply("Movies suggested for you:\n" + recommendations)
    print(message.text)

    print(message.text.split())

    if os.path.exists('vote_averages.png'):
        with open('vote_averages.png', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)

async def on_startup(dispatcher):
    await bot.set_webhook("")
    await dp.start_polling(bot)

async def on_shutdown(dispatcher):
    await bot.close()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
