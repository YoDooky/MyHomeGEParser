import main
from telegrambot import markups
from telegrambot import aux_functions

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext


class CitiesHandler:
    """Handlers for city selection"""
    def __init__(self):
        self.available_cities = main.get_cities()
        self.menu = markups.CityMenu(self.available_cities)

    async def city_start(self, call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        keyboard = self.menu.get_select_menu()
        await call.message.answer(text='Выберите город:',
                                  reply_markup=keyboard)

    async def back_command(self, call: types.CallbackQuery):
        """Last cities chunk"""
        keyboard = self.menu.get_select_menu('back')
        await call.message.edit_text('Back', reply_markup=keyboard)

    async def next_command(self, call: types.CallbackQuery):
        """Next cities chunk"""
        keyboard = self.menu.get_select_menu('next')
        await call.message.edit_text('Next', reply_markup=keyboard)

    @staticmethod
    async def city_choosen(call: types.CallbackQuery, state: FSMContext):
        selected_city = call.data.split('selected_city_')[1].capitalize()
        keyboard = markups.get_approve_menu()
        await state.update_data(choosen_city=selected_city)
        await call.message.edit_text(text=f'Выбранный город "{selected_city}"',
                                     reply_markup=keyboard)

    @staticmethod
    async def load_ad_data(call: types.CallbackQuery, state: FSMContext):
        await state.update_data(data_part='1')
        user_data = await state.get_data()

        await call.message.edit_text(text='Идет загрузка...')
        useful_data = main.get_demand_data(city=user_data.get('choosen_city'),
                                           demand_data_part=int(user_data.get("data_part")))
        if not useful_data:
            await call.message.edit_text(text=f'Не найдено объявлений в городе "{user_data.get("choosen_city")}"')
            await state.finish()
        await aux_functions.send_ad_to_chat(call, useful_data)
        keyboard = markups.get_load_more_menu()
        await call.message.answer(text='Выберите действие: ',
                                  reply_markup=keyboard)

    @staticmethod
    async def load_more(call: types.CallbackQuery, state: FSMContext):
        user_data = await state.get_data()
        await state.update_data(data_part=str(int(user_data.get("data_part")) + 1))
        user_data = await state.get_data()
        await call.message.answer(text='Идет загрузка...')
        useful_data = main.get_demand_data(city=user_data.get('choosen_city'),
                                           demand_data_part=int(user_data.get("data_part")))
        keyboard = markups.get_load_more_menu()
        if not useful_data:
            await call.message.edit_text(text=f'Больше не найдено объявлений')
            await state.finish()
        await aux_functions.send_ad_to_chat(call, useful_data)
        await call.message.answer(text='Выберите действие: ',
                                  reply_markup=keyboard)

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.city_start, text='choose_city')
        dp.register_callback_query_handler(self.city_start, text='cancel_choice')
        dp.register_callback_query_handler(self.back_command, text='back')
        dp.register_callback_query_handler(self.next_command, text='next')
        dp.register_callback_query_handler(self.city_choosen, Text(contains='selected_city'))
        dp.register_callback_query_handler(self.load_ad_data, text='approve_choice')
        dp.register_callback_query_handler(self.load_more, text='load_more')
