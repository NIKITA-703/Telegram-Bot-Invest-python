from datetime import datetime, date
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt


def validate_date(input_date):
    try:
        date_obj = datetime.strptime(input_date, '%d.%m.%Y').date()
        min_date = date(2017, 7, 1)
        max_date = date.today()

        if min_date <= date_obj <= max_date:
            return date_obj.strftime('%d.%m.%Y')
        else:
            return None
    except ValueError:
        return None


def get_bars(symbol, interval='1d', start_date=None, end_date=None):
    root_url = 'https://api.binance.com/api/v1/klines'
    url = f'{root_url}?symbol={symbol}&interval={interval}'
    if start_date:
        url += f'&startTime={int(start_date.timestamp()) * 1000}'
    if end_date:
        url += f'&endTime={int(end_date.timestamp()) * 1000}'
    data = json.loads(requests.get(url).text)
    df = pd.DataFrame(data)
    df.columns = ['open_time', 'o', 'h', 'l', 'c', 'v', 'close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore']
    df.index = [datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
    #print(df)
    return df


def get_currency_data_for_graph(date1, date2, user_currency):
    valid_date1 = validate_date(date1)
    valid_date2 = validate_date(date2)

    if not valid_date1 or not valid_date2:
        error_date = ("Некорректные даты. Пожалуйста, введите даты в формате DD.MM.YYYY и убедитесь, что они находятся "
                      "в диапазоне с 01.07.2017 по текущую дату.")
        print(error_date)
        #return None
        return "Ошибка в дате"

    start_date = datetime.strptime(valid_date1, "%d.%m.%Y")
    end_date = datetime.strptime(valid_date2, "%d.%m.%Y")

    delta = end_date - start_date
    if delta.days > 365:
        print(end_date)
        print("Вы выбрали временной интервал более 1 года. Программа сможет отобразить данные только за 1 год.")
        end_date = start_date + pd.DateOffset(years=1)
        print(end_date)

    user_currency = user_currency.upper()
    try:
        currency_data = get_bars(user_currency + 'USDT', start_date=start_date, end_date=end_date)
        print(type(currency_data))
        return currency_data
    except Exception:
        print("Введено неверное название валюты.")
        return "Введено неверное название валюты."


def main():
    date1 = input("Введите первую дату в формате DD.MM.YYYY: ")
    date2 = input("Введите вторую дату в формате DD.MM.YYYY: ")

    # Проверка корректности введенных дат
    valid_date1 = validate_date(date1)
    valid_date2 = validate_date(date2)

    if not valid_date1 or not valid_date2:
        print("Некорректные даты. Пожалуйста, введите даты в формате DD.MM.YYYY и убедитесь, что они находятся в "
              "диапазоне с 01.07.2017 по текущую дату.")
        return

    start_date = datetime.strptime(valid_date1, "%d.%m.%Y")
    end_date = datetime.strptime(valid_date2, "%d.%m.%Y")

    # Проверка продолжительности временного интервала
    delta = end_date - start_date
    if delta.days > 365:
        print("Вы выбрали временной интервал более 1 года. Программа сможет отобразить данные только за 1 год.")
        end_date = start_date + pd.DateOffset(years=1)

    user_currency = input("Введите название валюты: ")
    user_currency = user_currency.upper()

    # Получение исторических данных для введенной валюты и дат
    currency_data = get_bars(user_currency + 'USDT', start_date=start_date, end_date=end_date)

    # Построение графика цен для введенной валюты
    plt.figure(figsize=(12, 6))
    plt.plot(currency_data.index, currency_data['c'].astype(float), label=f'{user_currency}/USDT')
    plt.title(f'Historical {user_currency}/USDT Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()




# from binance.client import Client
# from pybit import spot_margin_trade, spot_leverage_token
# import matplotlib.pyplot as plt
# import pandas as pd
#
# symbol = 'ETHUSDT'
#
# client = Client()
# binance_df = pd.DataFrame(client.get_historical_klines(symbol, "1d",))
# binance_df = binance_df.iloc[:,:6]
# binance_df.columns = ["Time", "Open", "High", "Low", "Close", "Volume"]
# binance_df = binance_df.set_index("Time")
# binance_df.index = pd.to_datetime(binance_df.index, unit="ms")
# binance_df = binance_df.astype(float)
#
# print(binance_df)




# from pycoingecko import CoinGeckoAPI
# cg = CoinGeckoAPI()
# print(cg.get_price(ids='bitcoin', vs_currencies='usd'))