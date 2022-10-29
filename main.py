import json
import requests
from bs4 import BeautifulSoup
from collectData import DataCollect
import config
import os.path


def update_json_file(page_data, filename='data.json'):
    new_data = {}
    if not os.path.isfile(filename):  # create new file if file doesn't exist
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(page_data, file)
    with open(filename, 'r', encoding='utf-8') as file:
        file_data = json.load(file)
        for key, value in page_data.items():
            if key in file_data:
                break
            new_data = {**{key: value}, **file_data}  # add new data to start of the dict
    if not new_data:
        return
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(new_data, file)


def run_full_scan():
    """Runs full scan for selected city"""


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
    with open('data.html', 'w', encoding='utf-8') as file:
        file.write(src)
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
    city = 'Batumi'  # test
    filename = f'./data/{city}.json'
    # pages_amount = int(get_pages_amount(city))
    # for page in range(1, pages_amount + 1):
    #     src = get_page_src(city, page)
    with open('data.html', encoding='utf-8') as file:  # test
        src = file.read()
    page_data = get_page_data(src)

    update_json_file(page_data, filename)


if __name__ == '__main__':
    main()
