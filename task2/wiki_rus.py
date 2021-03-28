# В нашей школе мы не можем разглашать персональные данные пользователей, но чтобы преподаватель
# и ученик смогли объяснить нашей поддержке, кого они имеют в виду (у преподавателей,
# например, часто учится несколько Саш), мы генерируем пользователям уникальные и легко
# произносимые имена. Имя у нас состоит из прилагательного, имени животного и двузначной
# цифры. В итоге получается, например, "Перламутровый лосось 77". Для генерации таких имен
# мы и решали следующую задачу:
# Получить с русской википедии список всех животных (Категория:Животные по алфавиту)
# и вывести количество животных на каждую букву алфавита. Результат должен получиться в следующем виде:
#  А: 642
# Б: 412

import requests
import bs4
import time
import os
from settings import start_url, alphabet


class StatusCodeError(Exception):
    def __init__(self, text):
        self.text = text


class WikiParse:
    def __init__(self, start_url, alphabet):
        self.start_url = start_url
        self.alphabet = alphabet

    @staticmethod
    def _get_soup(url):
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = bs4.BeautifulSoup(response.text, 'lxml')
                    return soup
                raise StatusCodeError(f'{response.status_code}')
            except (requests.exceptions.HTTPError,
                    requests.exceptions.ConnectTimeout,
                    StatusCodeError):
                time.sleep(0.2)

    def create_next_url(self, pagination, up_letter):
        """генерация следующих страниц для парсинга"""
        if up_letter in alphabet:
            print('новая страница')
            next_url = f"https://ru.wikipedia.org{(pagination[1].attrs)['href']}"
            pagination_next, up_letter = self.get_parsing(next_url)
            self.create_next_url(pagination_next, up_letter)
        else:
            print('страницы закончились')
            for elem in self.alphabet:
                self.alphabet[elem] = len(self.alphabet[elem])
                print(f'{elem}:', self.alphabet[elem])
            animals = []
            for key, value in self.alphabet.items():
                animals.append(f'{key}: {value}')
            self.write_to_file('кол-во_животных', animals)

    @staticmethod
    def write_to_file(up_letter, animals):
        """запись списка животных в файл"""
        ROOT = os.getcwd()
        DIR_FILES = 'lists_animals'
        DIRECTORY = os.path.join(ROOT, DIR_FILES)
        if not os.path.exists(DIRECTORY):
            os.mkdir(DIRECTORY)
        file = os.path.join(DIRECTORY, f'{up_letter}.txt')
        with open(file, 'a+', encoding='utf-8') as f:
            for animal in animals:
                f.write(animal + '\n')

    def get_parsing(self, next_url):
        """создание списка животных"""
        soup_next = self._get_soup(next_url)
        pagination_next = soup_next.find_all('a', attrs={'title': 'Категория:Животные по алфавиту'})
        soup_page = soup_next.find_all('div', attrs={'class': 'mw-category-group'})
        up_letter = ''
        for teg_div in soup_page:
            up_letter = str(teg_div.find('h3').text).upper()
            if up_letter in self.alphabet:
                print(f'ищем на букву {up_letter}')
                animals = teg_div.ul.text.split('\n')
                self.alphabet[up_letter].extend(animals)
                self.write_to_file(up_letter, animals)
            else:
                print(f'игнорируем букву {up_letter}')

        return pagination_next, up_letter

    def run(self):
        pagination, up_letter = self.get_parsing(self.start_url)
        self.create_next_url(pagination, up_letter)


if __name__ == '__main__':
    parser = WikiParse(start_url, alphabet)
    parser.run()
