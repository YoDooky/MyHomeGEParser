from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from config import bot_config


class CityMenu:
    def __init__(self, cities_list: List):
        self.cities_list = cities_list
        self.cities_counter = 0
        self.max_elements = bot_config.MAX_MENU_ITEMS  # max elements count in inline menu

    def get_select_menu(self, scroll: str = None):
        """Cities menu with scroll (on buttons)"""
        back_button = InlineKeyboardButton(text='👈 BACK', callback_data='back')
        next_button = InlineKeyboardButton(text='NEXT 👉', callback_data='next')
        select_menu = InlineKeyboardMarkup(row_width=3)
        if not scroll:
            self.__start_select_menu(select_menu, next_button)
        elif scroll == 'next':
            self.__next_select_menu(select_menu, next_button, back_button)
        elif scroll == 'back':
            self.__back_select_menu(select_menu, next_button, back_button)
        return select_menu

    def __start_select_menu(self, select_menu, next_button):
        cities = self.__slice_cities_list(self.max_elements)
        select_menu = self.__add_city_buttons(cities, select_menu)
        if len(self.cities_list) > len(cities):
            select_menu.insert(next_button)

    def __next_select_menu(self, select_menu, next_button, back_button):
        cities = self.__slice_cities_list(self.max_elements, 'next')
        select_menu.insert(back_button)
        select_menu = self.__add_city_buttons(cities, select_menu)
        if self.cities_counter + self.max_elements < len(self.cities_list):
            select_menu.insert(next_button)

    def __back_select_menu(self, select_menu, next_button, back_button):
        cities = self.__slice_cities_list(self.max_elements, 'back')
        if self.cities_counter != 0:
            select_menu.insert(back_button)
        select_menu = self.__add_city_buttons(cities, select_menu)
        select_menu.insert(next_button)

    @staticmethod
    def __add_city_buttons(items, select_menu):
        for item in items:
            select_city_button = InlineKeyboardButton(text=f'{item}', callback_data=f'selected_city_{item}')
            select_menu.insert(select_city_button)
        return select_menu

    def __slice_cities_list(self, max_len: int, choice: str = None) -> List:
        if not choice:
            return self.cities_list[0: max_len]  # return first selected elements
        if choice == 'next':
            self.cities_counter = min(self.cities_counter + max_len, len(self.cities_list) - 1)
            return self.cities_list[self.cities_counter:self.cities_counter + max_len]
        else:
            self.cities_counter = max(self.cities_counter - max_len, 0)
            return self.cities_list[self.cities_counter: self.cities_counter + max_len]


def get_main_menu():
    main_menu = InlineKeyboardMarkup(row_width=1)
    choose_city_button = InlineKeyboardButton(text='Выберите город 🏙', callback_data='choose_city')
    main_menu.insert(choose_city_button)
    return main_menu


def get_approve_menu():
    approve_menu = InlineKeyboardMarkup(row_width=2)
    approve_choice_button = InlineKeyboardButton(text='Подтверждаю 👌', callback_data='approve_choice')
    cancel_choice_button = InlineKeyboardButton(text='👈 Вернуться к выбору города', callback_data='cancel_choice')
    approve_menu.insert(approve_choice_button)
    approve_menu.insert(cancel_choice_button)
    return approve_menu


def get_load_more_menu():
    load_more_menu = InlineKeyboardMarkup(row_width=2)
    load_more_button = InlineKeyboardButton(text='🔎 Показать еще...', callback_data='load_more')
    cancel_choice_button = InlineKeyboardButton(text='👈 Вернуться к выбору города', callback_data='cancel_choice')
    load_more_menu.insert(load_more_button)
    load_more_menu.insert(cancel_choice_button)
    return load_more_menu
