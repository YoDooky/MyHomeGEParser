from config.bot_config import TOKEN
from telegrambot.handlers import cities, common
from telegrambot import webhook_api
from fastapi import FastAPI

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.bot_command import BotCommand
import asyncio
import logging
import uvicorn


class BotInit:
    """Bot initialization"""

    def __init__(self):
        self.bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())


def init_handlers(dp):
    common.register_handlers(dp)
    city_handler = cities.CitiesHandler()
    city_handler.register_handlers(dp)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Рестарт бота"),
    ]
    await bot.set_my_commands(commands)


def set_logging(dp):
    logging.basicConfig(level=logging.INFO)
    dp.middleware.setup(LoggingMiddleware())


async def main():
    set_logging(bot_init.dp)
    init_handlers(bot_init.dp)
    await set_commands(bot_init.bot)


if __name__ == '__main__':
    bot_init = BotInit()
    asyncio.run(main())
    app = FastAPI()
    webhook_api.init_api(bot_init.bot, bot_init.dp, app)
    uvicorn.run(app, host='0.0.0.0', port=5010)
