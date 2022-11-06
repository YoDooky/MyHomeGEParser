from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from telegrambot import markups
from database.models.utils import dbcontrol


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = markups.get_main_menu()
    collect_user_data(message.chat.values)
    await message.answer('Добро пожаловать в агрегатор недвижимости Грузии 🇬🇪 ✌',
                         reply_markup=keyboard)


def register_handlers(dp: Dispatcher):
    """Register message handlers"""
    dp.register_message_handler(start, commands="start", state='*')


def collect_user_data(user_data):
    """Colelcts user data from telegram chat"""
    data = {
        'id': user_data['id'],
        'first_name': user_data['first_name'],
        'username': user_data['username'],
        'type': user_data['type'],
    }
    dbcontrol.insert_db('users', data)
