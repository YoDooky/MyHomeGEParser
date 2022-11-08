from database.models.createdb import DbCreator

HEADER = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/106.0.0.0 Safari/537.36'
}


def get_url(city='Kobuleti', page=1):
    city = city.title()
    database = DbCreator()
    cursor = database.cursor
    cursor.execute(f"SELECT id FROM cities WHERE city='{city}'")
    osm_id = cursor.fetchone()[0]
    city = '+'.join(city.split(' '))
    return f'https://www.myhome.ge/en/s/?Keyword={city}&AdTypeID=3&PrTypeID%5B%5D=1&PrTypeID%5B%5D=2' \
           f'&PrTypeID%5B%5D=7&Page={page}&cities={osm_id}&GID={osm_id}'
