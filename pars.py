import requests
from bs4 import BeautifulSoup
import json
from time import sleep
import random

# persons_url_list = []   #пустой список для наших ссылок

# #проходимся по странице и собираем
# for i in range(0, 740, 12):
#     url = f'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}'
#
#     q = requests.get(url)   #генерируем GET запрос на нужной странице и собираем все ссылки
#     result = q.content      #забираем контент
#
#     soup = BeautifulSoup(result, 'lxml')                      #передаем в обьект наш контент и тип парсера
#     persons = soup.find_all('a')        #извлекаем данные из получаемых старниц
#
#     for person in persons:
#         person_page_url = person.get('href')
#         persons_url_list.append(person_page_url)
#
# with open('persons_url_list.txt', 'a') as file:
#     for line in persons_url_list:
#         file.write(f'{line}\n')

with open('persons_url_list.txt') as file:

    lines = [line.strip() for line in file.readlines()] #strip - обрезаем строки с двух концов от пробелов

    data_dict = []               #список для данных всех наших людей
    count = 0

    for line in lines:
        q = requests.get(line)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        person = soup.find(class_='col-xs-8 col-md-9 bt-biografie-name').find('h3').text    #извлекаем данные из получаемых старниц
        person_name_company = person.strip().split(',')
        person_name = person_name_company[0]
        person_company = person_name_company[1].strip()

        #забираем ссылки на соцсети
        social_networks = soup.find_all(class_='bt-link-extern')

        social_networks_urls = []       #список для соцсетей
        for item in social_networks:
            social_networks_urls.append(item.get('href'))

        data = {
            'person_name': person_name,
            'company_name': person_company,
            'social_networks': social_networks_urls
        }
        count += 1


        print(f'#{count}: {line} is done!')

        data_dict.append(data)  #сохраняем информацию в список

        with open('data.json', 'w') as json_file:   #откроем файл на запись
            json.dump(data_dict, json_file, indent=4)

