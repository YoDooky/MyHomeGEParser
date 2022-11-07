import json
from typing import Dict, List
from sqlite3 import OperationalError
import requests
from bs4 import BeautifulSoup
from collect_data import DataCollect

from config import server_config
from database.models.utils import dbcontrol
from database.controllers import cities_controller
from database.models.utils import format_data
from config import bot_config


class PageData:
    """Parse page data and write to DB"""

    def __init__(self):
        self.header = server_config.HEADER

    def get_cities(self) -> Dict:
        """Get all cities and cities id dict"""
        url = 'https://www.myhome.ge/en/search/getCities'
        req = requests.post(url, headers=self.header)
        src = req.text
        src_dict = json.loads(src)
        cities_dict = {}
        for each in src_dict['subLocs']:
            cities_dict[int(each['osm_id'])] = each['name']['en']
        return cities_dict

    def get_pages_amount(self, city: str) -> int:
        """Returns city pages amount"""
        url = server_config.get_url(city)
        req = requests.get(url, headers=self.header)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        return int(soup.find('li', {'class': 'space-item-last'}).text)

    def get_page_data(self, city: str, page_number: int) -> List:
        """Returns only useful data"""
        url = server_config.get_url(city, page_number)
        req = requests.get(url, headers=self.header)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        card_container = soup.find_all('a', {'class': 'card-container'})
        data_collect = DataCollect()
        data = []
        for each in card_container:
            data.append(data_collect.get_card_data(each))
        return data


def remove_duplicate(city: str, ad_data: List[Dict]) -> bool:
    """Removes element from list if it's id is already in DB"""
    try:
        city = format_data.mod_string(city)  # replace spaces with underscore
        db_city_ids = dbcontrol.fetchall(city, ['id'])
    except OperationalError:
        return False
    db_city_id_list = [each['id'] for each in db_city_ids]
    result = False
    for num, each in enumerate(ad_data):
        if each['id'] in db_city_id_list:
            del ad_data[num]
            result = True
    return result


def update_db_data(city: str, data_amount: int):
    """Updates data in db if there is new data on page"""
    page_data = PageData()
    page_amount = page_data.get_pages_amount(city)
    ad_amount = 0
    for i in range(1, page_amount + 1):
        ad_data = page_data.get_page_data(city, i)
        duplicate_found = remove_duplicate(city, ad_data)  # remove duplicates to add only new data
        cities_controller.db_write_page_data(city, ad_data)
        ad_amount += len(ad_data)
        if ad_amount >= min(100, data_amount) or duplicate_found:  # break cycle if there is same data in DB
            break


def get_cities() -> List:
    """Returns only cities array"""
    city_data = dbcontrol.sort('cities', ['city'], 'city', order='ASC')
    return [each['city'] for each in city_data]


def get_demand_data(city: str, demand_data_part: int) -> List:
    """Returns demand from telegram data"""
    data_amount = bot_config.MAX_AD_AMOUNT
    if demand_data_part == 1:  # refresh data from web page only on first iteration
        # (because in DB it will be update after first iteration)
        update_db_data(city, data_amount)
    demand_data = cities_controller.db_get_cities_data(city, data_amount)
    part_size = 5  # amount of ad per one part
    return demand_data[demand_data_part * part_size - part_size:demand_data_part * part_size]


def write_cities_to_db():
    page_data = PageData()
    cities = page_data.get_cities()
    cities_controller.db_write_cities_data(cities)


if __name__ == '__main__':
    # write_cities_to_db()
    pass
