# К сожалению, к заданию не был приложен пример итогового JSON, поэтому взята произвольная форма
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# Скрапер обёрнут в единый класс пригодный для импорта в другие проекты


class Scraper:
    def __init__(self) -> None:
        # список ИНН сохранен отдельным атрибутом
        self.inn_list = self.update_inn_list()
        # Результат парсинга можно хранить до востребования
        self.results = self.get_data(self.inn_list)

    # Метод преобразования файла inn_list
    def update_inn_list(self):
        with open('inn_list.txt', 'r') as file:
            inn_list = file.read().splitlines()
        return inn_list

    # Метод получения итоговой информации
    def get_data(self, inn_list):
        result = {}
        # Создание драйвера эмулирующего браузер Chrome
        driver = webdriver.Chrome()
        # Цикл для сбора данных по каждому ИНН
        for inn in inn_list:
            # Обращение к странице
            url = f'https://fedresurs.ru/search/entity?code={inn}&regionNumber=Все&onlyActive=false'
            driver.get(url)
            # Поскольку на загрузку данных на портале расходуется определённое время, данная процедура даёт время на загрузку
            time.sleep(1)
            # Парсинг по тегам класса и атрибута
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            name = soup.find('a', class_='td_company_name').text.strip()
            adress = soup.find('p', class_='td_comp_address')
            # Обработка разных вариантов отображения ИП и организаций
            if adress is not None:
                adress = adress.text.strip()
            else:
                adress = 'ИП'
            status = soup.find('td', attrs={'_ngcontent-nol-c16': ''}, class_='with_link').text
            # Формирование результатов по одной организации/ИП
            inn_result = {
                inn: {
                    'Имя': name,
                    'Адресс/Флаг ИП': adress,
                    'Статус юр. лица': status
                    }
            }

            # Добавление в результирующий список
            result.update(inn_result)
        # Отключение драйвера
        driver.quit()
        return result

    # Метод для сохранения JSON файла
    def save_json(self, result):
        with open('results.json', 'w') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)


# Запуск скрипта из текущего файла
scraper = Scraper()
scraper.save_json(scraper.results)
