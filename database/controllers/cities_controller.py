from typing import List, Dict
from database.models.utils import dbcontrol
from database.models.utils import format_data


def db_write_page_data(city: str, data: List):
    """Write city data to DB"""
    city = format_data.mod_string(city)  # replace spaces with underscore
    for each in data:
        dbcontrol.insert_db(city, each)


def db_write_cities_data(cities: Dict):
    """Write cities to DB"""
    data = {}
    for key, value in cities.items():
        data['id'] = key
        data['city'] = value
        dbcontrol.insert_db('cities', data)


def db_get_cities_data(city: str, data_amount: int) -> List[Dict]:
    """Get demanded city data"""
    data = dbcontrol.sort(city, [
        'id',
        'url',
        'title',
        'address',
        'floor',
        'room',
        'bedroom',
        'size',
        'price',
        'date',
        'img_url'
    ], 'date')
    return data[0:data_amount]
