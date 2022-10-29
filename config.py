def get_url(city='Batumi', page=1):
    return f'https://www.myhome.ge/en/s/?Keyword={city}&Word=&AdTypeID=3' \
           f'&PrTypeID%5B%5D=1&PrTypeID%5B%5D=2&PrTypeID%5B%5D=7&Page={page}'


header = {
    'accept': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/106.0.0.0 Safari/537.36'
}
