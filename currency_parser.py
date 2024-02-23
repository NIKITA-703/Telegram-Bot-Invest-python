import requests
from datetime import datetime, date
from bs4 import BeautifulSoup



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


def get_currency_data(date1, date2, user_currency):
    validated_date1 = validate_date(date1)
    validated_date2 = validate_date(date2)

    if validated_date1 and validated_date2:

        currency_dict = {
            'Австралийский доллар': 'R01010',
            'Австрийский шиллинг': 'R01015',
            'Азербайджанский манат': 'R01020',
            'Албанский лек': 'R01025',
            'Алжирский динар': 'R01030',
            'Ангольская новая кванза': 'R01040',
            'Аргентинское песо': 'R01055',
            'Армянский драм': 'R01060',
            'Афганский афгани': 'R01065',
            'Бахрейнский динар': 'R01080',
            'Белорусский рубль': 'R01090',
            'Бельгийский франк': 'R01095',
            'Болгарский лев': 'R01100',
            'Боливийский боливиано': 'R01105',
            'Ботсванская пула': 'R01110',
            'Бразильский реал': 'R01115',
            'Брунейский доллар': 'R01111',
            'Бурундийский франк': 'R01120',
            'Венгерский форинт': 'R01135',
            'Венесуэльский боливар фу': 'R01140',
            'Вон Республики Корея': 'R01815',
            'Вона КНДР': 'R01145',
            'Вьетнамский донг': 'R01150',
            'Гамбийский даласи': 'R01160',
            'Ганский седи': 'R01165',
            'Гвинейский франк': 'R01175',
            'Гонконгский доллар': 'R01200',
            'Греческая драхма': 'R01205',
            'Грузинский лари': 'R01210',
            'Датская крона': 'R01215',
            'Дирхам ОАЭ': 'R01230',
            'Доллар Зимбабве': 'R01233',
            'Доллар Намибии': 'R02004',
            'Доллар США': 'R01235',
            'Евро': 'R01239',
            'Египетский фунт': 'R01240',
            'Заир ДРК': 'R01245',
            'Замбийская квача': 'R01250',
            'Израильский новый шекель': 'R01265',
            'Индийская рупия': 'R01270',
            'Индонезийская рупия': 'R01280',
            'Иорданский динар': 'R01285',
            'Иракский динар': 'R01290',
            'Иранский риал': 'R01300',
            'Ирландский фунт': 'R01305',
            'Исландская крона': 'R01310',
            'Испанская песета': 'R01315',
            'Итальянская лира': 'R01325',
            'Йеменский риал': 'R01330',
            'Казахстанский тенге': 'R01335',
            'Канадский доллар': 'R01350',
            'Катарский риал': 'R01355',
            'Кенийский шиллинг': 'R01360',
            'Кипрский фунт': 'R01365',
            'Киргизский сом': 'R01370',
            'Китайский юань': 'R01375',
            'Колумбийский песо': 'R01380',
            'Конголезский франк': 'R01383',
            'Костариканский колон': 'R01385',
            'Кубинское песо': 'R01395',
            'Кувейтский динар': 'R01390',
            'Лаосский кип': 'R01400',
            'Латвийский лат': 'R01405',
            'Леоне Сьерра-Леоне': 'R01410',
            'Ливанский фунт': 'R01420',
            'Ливийский динар': 'R01425',
            'Лилангени Свазиленда': 'R01430',
            'Литовский лит': 'R01435',
            'Литовский талон': 'R01435',
            'Маврикийская рупия': 'R01445',
            'Мавританская угия': 'R01450',
            'Македонский динар': 'R01460',
            'Малавийская квача': 'R01465',
            'Малагасийский ариари': 'R01470',
            'Малайзийский ринггит': 'R01475',
            'Мальтийская лира': 'R01480',
            'Марокканский дирхам': 'R01485',
            'Мексиканский песо': 'R01495',
            'Мозамбикский метикал': 'R01498',
            'Молдавский лей': 'R01500',
            'Монгольский тугрик': 'R01503',
            'Немецкая марка': 'R01510',
            'Непальская рупия': 'R01515',
            'Нигерийский найр': 'R01520',
            'Нидерландский гульден': 'R01523',
            'Никарагуанская золотая к': 'R01525',
            'Новозеландский доллар': 'R01530',
            'Новый туркменский манат': 'R01710',
            'Норвежская крона': 'R01535',
            'Оманский риал': 'R01540',
            'Пакистанская рупия': 'R01545',
            'Парагвайская гуарани': 'R01555',
            'Перуанский новый соль': 'R01560',
            'Польский злотый': 'R01565',
            'Португальский эскудо': 'R01570',
            'Риель Камбоджи': 'R01575',
            'Риял Саудовской Аравии': 'R01580',
            'Румынский лей': 'R01585',
            'СДР (специальные права з': 'R01589',
            'Сейшельская рупия': 'R01595',
            'Сербский динар': 'R01804',
            'Сингапурский доллар': 'R01625',
            'Сирийский фунт': 'R01630',
            'Словацкая крона': 'R01635',
            'Словенский толар': 'R01640',
            'Сомалийский шиллинг': 'R01650',
            'Суданский фунт': 'R01660',
            'Суринамский доллар': 'R01665',
            'Таджикский сомони': 'R01670',
            'Таиландский бат': 'R01675',
            'Тайваньский новый доллар': 'R01680',
            'Так Бангладеш': 'R01685',
            'Танзанийский шиллинг': 'R01690',
            'Тунисский динар': 'R01695',
            'Турецкая лира': 'R01700',
            'Туркменский манат': 'R01710',
            'Угандийский шиллинг': 'R01714',
            'Узбекский сум': 'R01717',
            'Украинская гривна': 'R01720',
            'Украинский карбованец': 'R01720',
            'Уругвайское песо': 'R01725',
            'Филиппинское песо': 'R01743',
            'Финляндская марка': 'R01740',
            'Франк Джибути': 'R01746',
            'Франк КФА ВЕАС': 'R01748',
            'Франк КФА ВСЕАО': 'R01749',
            'Французский франк': 'R01750',
            'Фунт стерлингов Соединен': 'R01035',
            'Хорватская куна': 'R01755',
            'Чехословацкая крона': 'R01761',
            'Чешская крона': 'R01760',
            'Чилийское песо': 'R01765',
            'Шведская крона': 'R01770',
            'Швейцарский франк': 'R01775',
            'Шри-Ланкийская рупия': 'R01780',
            'Эквадорский сукре': 'R01785',
            'ЭКЮ': 'R01790',
            'Эстонская крона': 'R01795',
            'Эфиопский быр': 'R01800',
            'Югославский новый динар': 'R01804',
            'Южноафриканский рэнд': 'R01810',
            'Японская иена': 'R01820'
        }

        data_dict = {
            "Дата": [],
            user_currency: []  # Инициализируем пустым списком
        }

        # Замена пробелов на символ подчеркивания и нижний регистр
        user_currency = user_currency.lower()
        currency_dict = {key.lower(): value for key, value in currency_dict.items()}

        currency_dict_new = {key.replace(' ', '_'): value for key, value in currency_dict.items()}
        user_currency_new = user_currency.replace(' ', '_')

        print(f"userr {user_currency}")
        print(f"userr {currency_dict} \n")


        # found_currency = None
        # for currency in currency_dict.keys():
        #     # Удалить пробелы из названия валюты для сравнения
        #     clean_currency_dict = currency.replace(" ", "_")
        #     user_currency_rep = user_currency.replace(" ", "_")
        #     #print(f"FORRR {user_currency_rep}")
        #     #print(f"FORRR {clean_currency_dict}")
        #
        #     if user_currency_rep.lower() in clean_currency_dict.lower():
        #         found_currency = currency
        #         print(f"IFFF {found_currency}")
        #         break

        if user_currency_new in currency_dict_new:
            # Получение кода валюты из словаря
            currency_code = currency_dict.get(user_currency)
            #print(f"USER INP{user_currency}")
            #print(f"ABOIA{currency_code}")

            # if currency_code:
            #     print(f"Код валюты {user_currency}: {currency_code}")
            # else:
            #     print(f"Валюта {user_currency} не найдена.")


            try:
                url_metals_data = (
                    f'https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1'
                    f'&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ={currency_code}&UniDbQuery.From={validated_date1}'
                    f'&UniDbQuery.To={validated_date2}')

                print(url_metals_data)
                print(validated_date1 + " " + validated_date2)

                req = requests.get(url_metals_data)

                soup = BeautifulSoup(req.text, "lxml")

                # данные таблицы
                table_info = soup.find(class_="table-wrapper").find("table").find_all("td")  # содержание таблицы

                # Удалить элементы, содержащие теги <h3>
                table_info = list(filter(lambda element: not element.find("h3"), table_info))  #

                amount_element = len(table_info)

                print(amount_element)

                data_rows = []  # Создаем список для хранения каждой строки данных

                current_row = []  # Создаем пустой список для текущей строки данных

                for item in range(amount_element):
                    values = table_info[item].text
                    if item % 3 == 0 and item != 0:
                        # Если достигли конца текущей строки, добавляем ее в список data_rows
                        data_rows.append(current_row)
                        # И создаем новую пустую строку
                        current_row = []

                    # Добавляем текущее значение к текущей строке
                    current_row.append(values)
                    #print(item)
                    item += 1

                # Если осталась неполная строка данных (например, если таблица не закончилась полностью), добавляем ее
                if current_row:
                    data_rows.append(current_row)

                print(f"СПИСОК {data_rows} ")

                if validated_date1 and validated_date2:
                    data_dict = {
                        "Дата": [],
                        "Единиц": [],
                        "Курс": []
                    }

                for row in data_rows:
                    data_dict["Дата"].append(row[0])
                    data_dict["Единиц"].append(row[1])
                    data_dict["Курс"].append(row[2])

                # print(f"Словарь {data_dict}")

                return {
                    "Дата": data_dict["Дата"],
                    user_currency: data_dict["Курс"]
                }

            except Exception:
                print("За выбранный вами период нет информации. ")
        else:
            # print(f" what is {user_currency}")
            # print(f"List of available currencies: {list(currency_dict.keys())}")
            return "Не верно введена валюта"

    else:
        print(
            "Некорректная дата. Пожалуйста, введите даты в формате DD.MM.YYYY, не ранее 01.07.2008 и не позже текущей "
            "даты.")


def actual_curse(base_currency):
    # Ваш API ключ
    # api_key = 'YOUR_API_KEY'

    # Базовый URL API
    base_url = 'https://open.er-api.com/v6/latest/'

    target_currency = "RUB"

    # Коды валюты для конвертации
    # base_currency = 'USD'  # Базовая валюта
    # target_currency = 'RUB'  # Целевая валюта

    # Сформируем URL запроса
    url = f'{base_url}{base_currency}'

    # Параметры запроса
    params = {'symbols': target_currency}

    # Отправляем GET запрос
    response = requests.get(url, params=params)

    # Проверяем успешность запроса
    if response.status_code == 200:
        data = response.json()
        print(data)
        # Получаем курс целевой валюты относительно базовой валюты
        exchange_rate = data['rates'][target_currency]
        print(f'Курс {base_currency} к {target_currency}: {exchange_rate}')
        return exchange_rate
    else:
        print('Ошибка при получении данных')
        return 'Ошибка при получении данных'


if __name__ == '__main__':
    # date1 = input("Введите первую дату в формате DD.MM.YYYY: ")
    # date2 = input("Введите вторую дату в формате DD.MM.YYYY: ")
    # user_currency = input("Введите название валюты: ")
    # user_currency = user_currency.title()
    # # date1 = "1.1.2020"
    # # date2 = "1.2.2020"
    # # user_currency = "Евро"
    #
    # get_currency_data(date1, date2, user_currency)

    base_currency = input("Какую валюту вы хотите посмотреть ")  # Базовая валюта
    base_currency.upper()

    actual_curse(base_currency)

# https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01115&UniDbQuery.From=19.10.2023&UniDbQuery.To=03.11.2023
# https://www.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From=19.10.2023&UniDbQuery.To=03.11.2023
