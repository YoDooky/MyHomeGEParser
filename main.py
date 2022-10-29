import json
import requests
from bs4 import BeautifulSoup
from collectData import DataCollect
import config
import os.path
from console_progressbar import ProgressBar


def update_json_file(page_data, filename='data.json'):
    new_data = {}
    if not os.path.isfile(filename):  # create new file if file doesn't exist
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(page_data, file)
    with open(filename, 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        current_data = {}
        for key, value in page_data.items():
            if key in file_data:
                break
            current_data[key] = value
        new_data = {**current_data, **file_data}  # add new data to start of the dict
    if not current_data:
        return 1
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(new_data, file)


def run_full_scan():
    """Runs full scan for selected city"""


def get_cities_json():
    """Save all cities to JSON"""
    url = 'https://www.myhome.ge/en/search/getCities'
    headers = config.header
    req = requests.post(url, headers=headers)
    src = req.text
    with open('cities_raw.json', 'w', encoding='utf-8') as file:
        file.write(src)
    with open('cities_raw.json', encoding='utf-8') as file:  # test
        python_src = json.load(file)
    cities_list = [each['name']['en'] for each in python_src['subLocs']]
    cities_json = json.dumps(cities_list)
    with open('cities.json', 'w', encoding='utf-8') as file:
        file.write(cities_json)


def get_cities():
    with open('cities.json', encoding='utf-8') as file:
        cities_list = json.load(file)
    return cities_list


def get_pages_amount(city):
    url = config.get_url(city)
    header = config.header
    req = requests.get(url, headers=header)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    return soup.find('li', {'class': 'space-item-last'}).text


def get_page_src(city, page_number=1):
    url = config.get_url(city, page_number)
    header = config.header
    req = requests.get(url, headers=header)
    src = req.text
    # with open('data.html', 'w', encoding='utf-8') as file:
    #     file.write(src)
    return src


def get_page_data(src):
    soup = BeautifulSoup(src, 'lxml')
    card_container = soup.find_all('a', {'class': 'card-container'})
    data_collect = DataCollect()
    data = {}
    for each in card_container:
        card_data = data_collect.get_card_data(each)
        data[card_data['id']] = card_data
    return data


def main():
    city = get_cities()[46]  # test Kobuleti
    filename = f'./data/{city}.json'
    pages_amount = int(get_pages_amount(city))
    pb = ProgressBar(total=pages_amount, prefix='Here', suffix='Now', decimals=0, length=50, fill='X', zfill='-')
    for page in range(pages_amount, 0, -1):
        src = get_page_src(city, page)
        page_data = get_page_data(src)
        if update_json_file(page_data, filename):
            break
        pb.print_progress_bar(pages_amount - page)


if __name__ == '__main__':
    get_cities()
    main()
