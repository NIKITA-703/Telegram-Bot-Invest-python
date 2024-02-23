import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

import pandas as pd

from metal_parser import get_metals_data
from currency_parser import get_currency_data
from crypto import get_currency_data_for_graph


"""
команды бота:
/start
/metals
/currency
/crypt
/help
"""

"""
InvestTelegramBot
    data
    venv
    config.py
    graphics.py
    metal_parser.py
    currency_parser.py
    main.py
    telegramBot.py
"""


# Металлы
async def plot_metal_prices(data_dict, metal_type, date1, date2, user_id, y_step=100):  # металлы
    # Получите даты и цены here he looks at what type of metal
    dates = data_dict["Дата"]
    if metal_type == "Золото":
        metal_prices = data_dict["Золото"]
    elif metal_type == "Серебро":
        metal_prices = data_dict["Серебро"]
    elif metal_type == "Платина":
        metal_prices = data_dict["Платина"]
    elif metal_type == "Палладий":
        metal_prices = data_dict["Палладий"]
    else:
        # Обработка случая, если выбран неверный тип металла
        print("Выбран неверный тип металла.")
        return

    # Преобразуйте даты в объекты даты (datetime)
    formatted_dates = [datetime.strptime(date, "%d.%m.%Y") for date in dates]

    # Преобразуйте цены во float, удалив пробелы и заменив ',' на '.'
    metal_prices = [float(price.replace(' ', '').replace(',', '.')) for price in metal_prices]

    # Создайте список кортежей (дата, цена) и отсортируйте его по дате
    sorted_data = sorted(zip(formatted_dates, metal_prices))

    # Разделите отсортированные данные обратно на даты и цены
    sorted_dates, sorted_prices = zip(*sorted_data)

    print(sorted_dates)
    print(f"sorted_prices \n")
    #print("Перед постройкой графиков")

    try:
        plt.figure(figsize=(20, 6))  # Устанавливаем размер графика

        plt.plot(sorted_dates, sorted_prices, linestyle='-')  # Строим график marker='o',
        plt.title(f'Цены на {metal_type} c {date1} по {date2}')
        plt.xlabel('Дата')
        plt.ylabel('Цена (РУБ)')

        # Устанавливаем метки на оси Y точно так, как они есть в ваших данных
        y_ticks = range(int(min(sorted_prices)), int(max(sorted_prices)) + 1, y_step)
        plt.yticks(y_ticks)

        # x_locator = ticker.MultipleLocator(x_interval)
        # plt.gca().xaxis.set_major_locator(x_locator)

        #print("показ графика")
        plt.xticks(rotation=45)  # Поворачиваем надписи на оси X для лучшей читаемости | #plt.yticks(sorted_prices[::2])

        plt.grid(True)  # Включаем сетку

        plt.tight_layout()  # Улучшает компоновку графика

        plt.savefig(f"data/graph_metal_user_{user_id}.png")

        #plt.close()
        #print("v plot metal pered return")
        return "График готов"
        #plt.show()  # Отображаем график
        #return "График готов"

    except Exception as e:
        print(f"ОШИБКА {e}")


# Валюта
async def plot_currency_prices(data_dict, currency_type, date1, date2, user_id, y_step=1):  # валюта
    # Функция для построения графика цен на валюту
    dates = data_dict["Дата"]
    currency_prices = data_dict[currency_type]

    # Преобразуйте даты в объекты даты (datetime)
    formatted_dates = [datetime.strptime(date, "%d.%m.%Y") for date in dates]

    # Преобразуйте цены во float, удалив пробелы и заменив ',' на '.'
    currency_prices = [float(price.replace(' ', '').replace(',', '.')) for price in currency_prices]

    # Создайте список кортежей (дата, цена) и отсортируйте его по дате
    sorted_data = sorted(zip(formatted_dates, currency_prices))

    # Разделите отсортированные данные обратно на даты и цены
    sorted_dates, sorted_prices = zip(*sorted_data)

    print(sorted_dates)
    print(sorted_prices)

    plt.figure(figsize=(20, 6))  # Устанавливаем размер графика

    plt.plot(sorted_dates, sorted_prices, linestyle='-')  # Строим график marker='o',
    plt.title(f'Цены на {currency_type} c {date1} по {date2}')
    plt.xlabel('Дата')
    plt.ylabel('Цена (РУБ)')

    # Устанавливаем метки на оси Y точно так, как они есть в ваших данных
    y_ticks = range(int(min(sorted_prices)), int(max(sorted_prices)))  # , y_step
    plt.yticks(y_ticks)

    # x_locator = ticker.MultipleLocator(x_interval)
    # plt.gca().xaxis.set_major_locator(x_locator)

    plt.xticks(rotation=45)  # Поворачиваем надписи на оси X для лучшей читаемости | #plt.yticks(sorted_prices[::2])
    plt.grid(True)  # Включаем сетку
    plt.tight_layout()  # Улучшает компоновку графика
    plt.savefig(f"data/graph_currency_user_{user_id}.png")
    #plt.show()  # Отображаем график

    return "График готов"


# Крипта
async def plot_cryptocoin_prices(data_dict, crypto_coin, date1, date2, user_id,y_step=3000):
    dates = data_dict.index
    coin_prices = data_dict['c'].astype(float)  # или другие колонки, в зависимости от структуры данных

    start_date = datetime.strptime(date1, "%d.%m.%Y")
    end_date = datetime.strptime(date2, "%d.%m.%Y")

    delta = end_date - start_date
    if delta.days > 365:
        end_date = start_date + timedelta(days=365)
        end_date = end_date.strftime('%d.%m.%Y')

    plt.figure(figsize=(20, 6))  # 12 6
    plt.plot(dates, coin_prices, label=f'{crypto_coin}/USDT')  # marker='o',
    plt.title(f'Цены на {crypto_coin.upper()}/USDT с {date1} по {end_date}')
    plt.xlabel('Дата')
    plt.ylabel('Цена (USDT)')

    # # Устанавливаем метки на оси Y с учетом y_step
    # y_ticks = range(int(min(coin_prices)), int(max(coin_prices)) + 1, y_step)
    # plt.yticks(y_ticks)

    print(f" ZDEC {date2}")

    #plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"data/graph_cryptoCoin_user_{user_id}.png")
    #plt.show()

    return "График готов"


async def main(choice, date1, date2, metal_type=None, user_id=None, user_currency=None):
    if choice == "Металлы":
        data_dict = get_metals_data(date1, date2, metal_type)  # Используйте введенные даты

        if data_dict:
            result = await plot_metal_prices(data_dict, metal_type, date1, date2, user_id)
            if result == "График готов":
                return "График готов"
        else:
            return "Не удалось получить данные о металле"

    elif choice == "Валюта":
        try:
            user_currency = user_currency.lower()
            data_dict = get_currency_data(date1, date2, user_currency)
            print(f"print || МЫ В ВАЛЮТЕ")
            if isinstance(data_dict, dict):
                result = await plot_currency_prices(data_dict, user_currency, date1, date2, user_id)
                if result == "График готов":
                    return "График готов"
            else:
                print("Была неверно указана валюта")
                return "Была неверно указана валюта"
        except ValueError as e:
            print(e)
        print("В графике валюта")

    elif choice == "Криптовалюта":
        try:
            user_currency = user_currency.lower()
            data_dict = get_currency_data_for_graph(date1, date2, user_currency)


           # if isinstance(data_dict, dict):
            if isinstance(data_dict, pd.core.frame.DataFrame):
                result = await plot_cryptocoin_prices(data_dict, user_currency, date1, date2, user_id)
                if result == "График готов":
                    return "График готов"

                print("график не готов")

            elif data_dict == "Введено неверное название валюты.":
                print("Введено неверное название валюты.")
                return "Введено неверное название валюты."

            elif data_dict == "Ошибка в дате":
                print("Ошибка в дате")
                return "Ошибка в дате"

            else:
                print("Не удалось получить данные для построения графика.")
                return "Не удалось получить данные для построения графика."

        except ValueError as e:
            print(e)

    else:
        print("такого нет в списке")


if __name__ == '__main__':
    choice = None  # Инициализируем переменную choice значением None

    while choice not in ["Металлы", "Валюта", "Криптовалюта"]:
        choice = input("Что вы хотели бы просмотреть: Металлы, Валюта, Криптовалюта? ")
        choice = choice.title()  # Преобразуем выбор пользователя в верхний регистр

        if choice not in ["Металлы", "Валюта", "Криптовалюта"]:
            print("Некорректный ввод. Введите 'Металлы', 'Валюта' или 'Криптовалюта'.")

    if choice == "Металлы":
        date1 = input("Введите первую дату в формате ДД.ММ.ГГГГ: ")
        date2 = input("Введите вторую дату в формате ДД.ММ.ГГГГ: ")
        metal_type = input("Введите тип металла (Золото, Серебро, Платина, Палладий): ")
        metal_type = metal_type.title()

        data_dict = get_metals_data(date1, date2, metal_type)  # Используйте введенные даты

        if data_dict:
            plot_metal_prices(data_dict, metal_type)

    elif choice == "Валюта":
        date1 = input("Введите первую дату в формате ДД.ММ.ГГГГ: ")
        date2 = input("Введите вторую дату в формате ДД.ММ.ГГГГ: ")
        user_currency = input("Введите название валюты: ")  # 1.1.2020

        try:
            user_currency = user_currency.lower()
            data_dict = get_currency_data(date1, date2, user_currency)
            print(f"print {data_dict}")
            if isinstance(data_dict, dict):
                plot_currency_prices(data_dict, user_currency)

            else:
                print("Была неверно указана валюта")

        except ValueError as e:
            print(e)

    elif choice == "Криптовалюта":
        date1 = input("Введите первую дату в формате ДД.ММ.ГГГГ: ")
        date2 = input("Введите вторую дату в формате ДД.ММ.ГГГГ: ")
        user_currency = input("Введите название криптовалюты: ")

        try:
            user_currency = user_currency.lower()
            data_dict = get_currency_data_for_graph(date1, date2, user_currency)

            if data_dict is not None:
                plot_cryptocoin_prices(data_dict, user_currency, date1, date2)
            else:
                print("Не удалось получить данные для построения графика.")

        except ValueError as e:
            print(e)