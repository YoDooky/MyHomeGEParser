import re
from typing import Dict


class DataCollect:
    @staticmethod
    def __get_id(item):
        """Gets ad id"""
        try:
            string_object = " ".join(item.find('div', {'class': 'list-view-id-container'}).find('span').text.split())
            return parse_numb(string_object=string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_url(item):
        """Gets ad URL"""
        try:
            return item.attrs['href']
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_title(item):
        """Gets ad title"""
        try:
            return " ".join(item.find('h5', {'class': 'card-title'}).text.split())
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_address(item):
        """Gets address"""
        try:
            return " ".join(item.find('div', {'class': 'address'}).text.split())
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_floor(item):
        """Gets floor"""
        try:
            string_object = " ".join(item.find('div', {'data-tooltip': 'Floor'}).find('span').text.split())
            return parse_numb(string_object=string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_room(item):
        """Gets room amount"""
        try:
            string_object = " ".join(item.find('div', {'data-tooltip': 'Number of rooms'}).find('span').text.split())
            return parse_numb(string_object=string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_bedroom(item):
        """Gets bedroom amount"""
        try:
            string_object = " ".join(item.find('div', {'data-tooltip': 'Bedroom'}).find('span').text.split())
            return parse_numb(string_object=string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_size(item):
        """Gets home area"""
        try:
            string_object = " ".join(item.find('div', {'class': 'item-size'}).text.split())
            return parse_numb(string_object=string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_price(item):
        """Gets home price"""
        try:
            string_object = " ".join(item.find('b', {'class': 'item-price-usd'}).text.split())
            string_object = ''.join(string_object.split(','))
            return parse_numb(string_object=string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_date(item):
        """Gets ad announce date"""
        try:
            string_object = " ".join(item.find('div', {'class': 'statement-date'}).text.split())
            return convert_date(string_object)
        except AttributeError:
            return "no info"

    @staticmethod
    def __get_images_url(item):
        """Gets URL to all card's images"""
        img_amount = int(item.find('img', {'class': 'card-img'}).attrs['data-photos-cnt'])  # img amount
        if not img_amount:  # no image
            return 'https://www.myhome.ge/framework/templates/assets/img/pixel_grey.gif'
        img_url = item.find('img', {'class': 'card-img'}).attrs['data-src']  # first img url
        img_list = []
        for i in range(1, img_amount + 1):
            first_part = '.'.join(img_url.split('.')[:-2:])
            new_part = '_'.join([img_url.split('.')[-2].split('_')[0], str(i)])
            last_part = img_url.split('.')[-1]
            img_list.append('.'.join([first_part, new_part, last_part]))
        return ', '.join(img_list)

    def get_card_data(self, src) -> Dict:
        return {
            'id': self.__get_id(src),
            'url': self.__get_url(src),
            'title': self.__get_title(src),
            'address': self.__get_address(src),
            'floor': self.__get_floor(src),
            'room': self.__get_room(src),
            'bedroom': self.__get_bedroom(src),
            'size': self.__get_size(src),
            'price': self.__get_price(src),
            'date': self.__get_date(src),
            'img_url': self.__get_images_url(src)
        }


def parse_numb(string_object: str) -> int:
    return int(re.findall(r'\d+', string_object.strip())[0])


def convert_date(string_object: str) -> str:
    """Returns date in demand format"""
    month_list = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    def add_zero(value: str) -> str:
        if len(value) <= 1:
            return ''.join(['0', str(value)])
        return value

    year = '2022'
    month = add_zero(str(month_list.index(string_object.split(' ')[1].lower()) + 1))
    day = add_zero(string_object.split(' ')[0])
    time = string_object.split(' ')[2]
    return '-'.join([year, month, day]) + ' ' + time
