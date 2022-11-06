from config.bot_config import token
from handlers import cities, common
from main import get_cities as get_cities_data
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
import asyncio


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Рестарт бота"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())
    common.register_handlers(dp)
    city_handler = cities.CitiesHandler()
    city_handler.register_handlers(dp)
    await set_commands(bot)
    await dp.start_polling(dp)


def awdawdawd():
    WEBHOOK_HOST = 'https://your.domain'
    WEBHOOK_PATH = '/path/to/api'
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

    # webserver settings
    WEBAPP_HOST = 'localhost'  # or ip
    WEBAPP_PORT = 3001


if __name__ == '__main__':
    available_cities = get_cities_data()
    asyncio.run(main())
