import requests
import csv
import time
from datetime import datetime, time, date
from aiogram import Bot, Dispatcher, types, executor
from bs4 import BeautifulSoup


# TODO: парсинг сбера (металлы), крипта yobit, курсы валюты Euro foreign (нет рубля, разны валюты. Библиотека)
# TODO: парсинг металлов с цетробанка : https://www.cbr.ru/hd_base/metall/metall_base_new/ ✔

# TODO: Возможная оптимизация: заносить данные в csv таблицу и если данные уже есть то не искать на сайте,
#  а просто найти в документе. Заносить данные в таблицу, а потом поиск

# TODO: сделать нормальный возврат об ошибке (return)




# ******Парсинг металлов  цетробанка******


def get_metals_now(actual_metal, choice):
    url_metals = "https://www.cbr.ru/hd_base/metall/metall_base_new/"


    req = requests.get(url_metals)

    soup = BeautifulSoup(req.text, "lxml")

    # заголовки таблицы

    #table_head = soup.find(class_="table-wrapper").find("tr").find_all("th")  # заголовоки

    # print(table_head)
    # пока не нужно
    # data = table_head[0].text
    # data = data[:-4]
    # gold = table_head[1].text
    # silver = table_head[2].text
    # platinum = table_head[3].text
    # palladium = table_head[4].text
    #
    # with open(f"data/tables.csv", "w", encoding="UTF-8-sig") as file:
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow(
    #         (
    #             data,
    #             data,
    #             gold,
    #             silver,
    #             platinum,
    #             palladium
    #         )
    #     )

    # данные таблицы

    table_info = soup.find(class_="table-wrapper").find("table").find_all("td")  # содержание таблицы

    data_rows = []  # Создаем список для хранения каждой строки данных

    current_row = []  # Создаем пустой список для текущей строки данных

    for item in range(5):
        values = table_info[item].text

        if item % 5 == 0 and item != 0:
            # Если достигли конца текущей строки, добавляем ее в список data_rows
            data_rows.append(current_row)
            # И создаем новую пустую строку
            current_row = []

        # Добавляем текущее значение к текущей строке
        current_row.append(values)

        item += 1

    # Если осталась неполная строка данных (например, если таблица не закончилась полностью), добавляем ее
    if current_row:
        data_rows.append(current_row)

    # Выводим каждую строку данных
    # for row in data_rows:
    #     print(row)

    data_dict = {
        "Дата": [],
        "Золото": [],
        "Серебро": [],
        "Платина": [],
        "Палладий": []
    }

    for row in data_rows:
        data_dict["Дата"].append(row[0])
        data_dict["Золото"].append(row[1])
        data_dict["Серебро"].append(row[2])
        data_dict["Платина"].append(row[3])
        data_dict["Палладий"].append(row[4])

    # for i in range(1):
    #     print(f"Дата: {data_dict['Дата'][i]}")
    #     print(f"Золото: {data_dict['Золото'][i]}")
    #     print(f"Серебро: {data_dict['Серебро'][i]}")
    #     print(f"Платина: {data_dict['Платина'][i]}")
    #     print(f"Палладий: {data_dict['Палладий'][i]}")
    #     print("\n")

    if choice == "now" and actual_metal is not None:
        return f"Цена за 1 грамм: {data_dict[actual_metal][0]} за {data_dict['Дата'][0]}: "
    elif choice == "now_time" and actual_metal is None:
        return data_dict


def get_metals_weeks():
    url_metals = "https://www.cbr.ru/hd_base/metall/metall_base_new/"

    # https://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.From=19.10.2023&UniDbQuery.To=28.10.2023&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.Platinum=true&UniDbQuery.Palladium=true&UniDbQuery.so=1

    # headers = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    #     "Connection":  "keep-alive",
    #     "Cookie":  "ASPNET_SessionID=0h4p0kedu15yl5a5ruqdofu4; __ddg1_=jYvMhM3K6a5n1jlLl7vM; accept=1",
    #     "Host":  "www.cbr.ru",
    #     "Referer":  "https://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.From=20.10.2023&UniDbQuery.To=26.10.2023&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.Platinum=true&UniDbQuery.Palladium=true&UniDbQuery.so=1",
    #     "Sec-Fetch-Dest":  "document",
    #     "Sec-Fetch-Mode":  "navigate",
    #     "Sec-Fetch-Site":  "same-origin",
    #     "Sec-Fetch-User":  "?1",
    #     "TE":  "trailers",
    #     "Upgrade-Insecure-Requests":  "1",
    #     "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"
    # }

    req = requests.get(url_metals)

    soup = BeautifulSoup(req.text, "lxml")

    # заголовки таблицы

    # table_head = soup.find(class_="table-wrapper").find("tr").find_all("th")  # заголовоки

    # print(table_head)
    # пока не нужно
    # data = table_head[0].text
    # data = data[:-4]
    # gold = table_head[1].text
    # silver = table_head[2].text
    # platinum = table_head[3].text
    # palladium = table_head[4].text
    #
    # with open(f"data/tables.csv", "w", encoding="UTF-8-sig") as file:
    #     writer = csv.writer(file, delimiter=';')
    #     writer.writerow(
    #         (
    #             data,
    #             data,
    #             gold,
    #             silver,
    #             platinum,
    #             palladium
    #         )
    #     )

    # данные таблицы

    table_info = soup.find(class_="table-wrapper").find("table").find_all("td")  # содержание таблицы

    # print(table_info)

    # print(table_info[0].text)
    # print(table_info[1].text)
    # print(table_info[2].text)
    # print(table_info[3].text)
    # print(table_info[4].text)
    # print(table_info[5].text)

    amount_element = len(table_info)

    data_rows = []  # Создаем список для хранения каждой строки данных

    current_row = []  # Создаем пустой список для текущей строки данных

    for item in range(amount_element):
        values = table_info[item].text

        if item % 5 == 0 and item != 0:
            # Если достигли конца текущей строки, добавляем ее в список data_rows
            data_rows.append(current_row)
            # И создаем новую пустую строку
            current_row = []

        # Добавляем текущее значение к текущей строке
        current_row.append(values)

        item += 1

    # Если осталась неполная строка данных (например, если таблица не закончилась полностью), добавляем ее
    if current_row:
        data_rows.append(current_row)

    # Выводим каждую строку данных
    # for row in data_rows:
    #     print(row)

    data_dict = {
        "Дата": [],
        "Золото": [],
        "Серебро": [],
        "Платина": [],
        "Палладий": []
    }

    for row in data_rows:
        data_dict["Дата"].append(row[0])
        data_dict["Золото"].append(row[1])
        data_dict["Серебро"].append(row[2])
        data_dict["Платина"].append(row[3])
        data_dict["Палладий"].append(row[4])

    # Теперь у вас есть словарь с данными
    # for i in range(len(data_dict["Дата"])):
    #     print(f"Дата: {data_dict['Дата'][i]}")
    #     print(f"Золото: {data_dict['Золото'][i]}")
    #     print(f"Серебро: {data_dict['Серебро'][i]}")
    #     print(f"Платина: {data_dict['Платина'][i]}")
    #     print(f"Палладий: {data_dict['Палладий'][i]}")
    #     print("\n")

    for i in range(1):
        print(f"Дата: {data_dict['Дата'][i]}")
        print(f"Золото: {data_dict['Золото'][i]}")
        print(f"Серебро: {data_dict['Серебро'][i]}")
        print(f"Платина: {data_dict['Платина'][i]}")
        print(f"Палладий: {data_dict['Палладий'][i]}")
        print("\n")


def validate_date(input_date):
    try:
        date_obj = datetime.strptime(input_date, '%d.%m.%Y').date()
        min_date = date(2008, 7, 1)
        max_date = date.today()

        if min_date <= date_obj <= max_date:
            return date_obj.strftime('%d.%m.%Y')
        else:
            return None
    except ValueError:
        return None


def get_metals_data(date1, date2, metal_type):
    validated_date1 = validate_date(date1)
    validated_date2 = validate_date(date2)

    if validated_date1 and validated_date2:
        url_metals_data = (
            f'https://www.cbr.ru/hd_base/metall/metall_base_new/?UniDbQuery.Posted=True&UniDbQuery.From={validated_date1}'
            f'&UniDbQuery.To={validated_date2}&UniDbQuery.Gold=true&UniDbQuery.Silver=true&UniDbQuery.Platinum'
            '=true&UniDbQuery.Palladium=true&UniDbQuery.so=1')

        print(url_metals_data)
        print(validated_date1 + " " + validated_date2)

        print(metal_type)

        req = requests.get(url_metals_data)

        soup = BeautifulSoup(req.text, "lxml")

        # заголовки таблицы

        # table_head = soup.find(class_="table-wrapper").find("tr").find_all("th")  # заголовоки
        #
        # #print(table_head)
        #
        # data_table = table_head[0].text
        # data_table = data_table[:-4]
        # gold = table_head[1].text
        # silver = table_head[2].text
        # platinum = table_head[3].text
        # palladium = table_head[4].text

        # данные таблицы
        try:
            table_info = soup.find(class_="table-wrapper").find("table").find_all("td")  # содержание таблицы

            amount_element = len(table_info)

            print(amount_element)

            data_rows = []  # Создаем список для хранения каждой строки данных

            current_row = []  # Создаем пустой список для текущей строки данных

            for item in range(amount_element):
                values = table_info[item].text

                if item % 5 == 0 and item != 0:
                    # Если достигли конца текущей строки, добавляем ее в список data_rows
                    data_rows.append(current_row)
                    # И создаем новую пустую строку
                    current_row = []

                # Добавляем текущее значение к текущей строке
                current_row.append(values)

                item += 1

            # Если осталась неполная строка данных (например, если таблица не закончилась полностью), добавляем ее
            if current_row:
                data_rows.append(current_row)

            # Выводим каждую строку данных
            # for row in data_rows:
            #     print(row)
            # else:
            #     print("Некорректная дата. Пожалуйста, введите даты в формате DD.MM.YYYY, не ранее 01.07.2008 и не позже текущей даты. ТУТ ?")

            if validated_date1 and validated_date2:
                data_dict = {
                    "Дата": [],
                    "Золото": [],
                    "Серебро": [],
                    "Платина": [],
                    "Палладий": []
                }

                for row in data_rows:
                    data_dict["Дата"].append(row[0])
                    data_dict["Золото"].append(row[1])
                    data_dict["Серебро"].append(row[2])
                    data_dict["Платина"].append(row[3])
                    data_dict["Палладий"].append(row[4])

                print(data_dict)

                if metal_type == "Золото":
                    metal_data = data_dict["Золото"]
                elif metal_type == "Серебро":
                    metal_data = data_dict["Серебро"]
                elif metal_type == "Платина":
                    metal_data = data_dict["Платина"]
                elif metal_type == "Палладий":
                    metal_data = data_dict["Палладий"]
                else:
                    # Обработка случая, если выбран неверный тип металла
                    print("Выбран неверный тип металла.")
                    return None

                # print(data_dict)

                return {
                    "Дата": data_dict["Дата"],
                    metal_type: metal_data
                }

                #     # Теперь у вас есть словарь с данными
                # for i in range(len(data_dict["Дата"])):
                #     print(f"Дата: {data_dict['Дата'][i]}")
                #     print(f"Золото: {data_dict['Золото'][i]}")
                #     print(f"Серебро: {data_dict['Серебро'][i]}")
                #     print(f"Платина: {data_dict['Платина'][i]}")
                #     print(f"Палладий: {data_dict['Палладий'][i]}")
                #     print("\n")

            # else:
            #     print("Некорректная дата. Пожалуйста, введите даты в формате DD.MM.YYYY, не ранее 01.07.2008 и не позже текущей даты. 00000")

        except Exception:
            print("За выбранный вами период нет информации. ")

    else:
        print(
            "Некорректная дата. Пожалуйста, введите даты в формате DD.MM.YYYY, не ранее 01.07.2008 и не позже текущей "
            "даты.")


def save_data_to_csv(data_dict):
    # Преобразование и сортировка уникальных дат
    unique_dates = set(data_dict["Дата"])
    sorted_dates = sorted(unique_dates)

    with open("data/metals_data.csv", "a", newline="", encoding="UTF-8-sig") as csvfile:
        fieldnames = ["Дата", "Золото", "Серебро", "Платина", "Палладий"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        if csvfile.tell() == 0:  # Если файл пустой, добавляем заголовок
            writer.writeheader()

        for date in sorted_dates:  # Перебираем отсортированные даты
            # Находим индекс даты в исходных данных
            index = data_dict["Дата"].index(date)
            writer.writerow({
                "Дата": data_dict["Дата"][index],
                "Золото": data_dict["Золото"][index],
                "Серебро": data_dict["Серебро"][index],
                "Платина": data_dict["Платина"][index],
                "Палладий": data_dict["Палладий"][index]
            })


if __name__ == '__main__':
    # date1 = input("Введите первую дату в формате DD.MM.YYYY: ")
    # date2 = input("Введите вторую дату в формате DD.MM.YYYY: ")
    # metal_type = input("Введите тип металла (Золото, Серебро, Платина, Палладий): ")
    # metal_type = metal_type.title()
    #
    # #get_metals_data(date1, date2)
    # #get_metals_weeks()
    #
    # data_dict = get_metals_data(date1, date2, metal_type)

    #get_metals_weeks()
    get_metals_now("Золото")

    # if data_dict:
    #     save_data_to_csv(data_dict)

# выводит неделю (начальная страница https://www.cbr.ru/hd_base/metall/metall_base_new/)
# выводит промежуток дат с обработкой
