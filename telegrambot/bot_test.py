from config.bot_config import token
from handlers import cities, common
from main import get_cities as get_cities_data
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from aiogram.types import CallbackQuery
import asyncio
from telegrambot import buttons
from telegrambot import markups
from typing import List, Dict
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.markdown import hbold, hlink


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Рестарт бота"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    test_list = [f'LongCity #{i}' for i in range(50)]
    menu = markups.CityMenu(test_list)

    @dp.message_handler(commands='start')
    async def start_command(message: types.Message):
        keyboard = menu.get_select_menu()
        await message.answer('Sup', reply_markup=keyboard)

    @dp.callback_query_handler(text='back')
    async def back_command(call: CallbackQuery):
        keyboard = menu.get_select_menu('back')
        await call.message.edit_text('Back', reply_markup=keyboard)

    @dp.callback_query_handler(text='next')
    async def next_command(call: CallbackQuery):
        keyboard = menu.get_select_menu('next')
        await call.message.edit_text('Next', reply_markup=keyboard)

    await dp.start_polling(dp)


if __name__ == '__main__':
    asyncio.run(main())
