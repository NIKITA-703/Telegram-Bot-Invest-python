import asyncio

import aioschedule
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import hlink, link
from aiogram.dispatcher.filters import Command, state
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from binance import AsyncClient
from binance.exceptions import BinanceAPIException

from datetime import datetime, date, timedelta

from config import Token_Telegram_bot
from graphics import main
from currency_parser import actual_curse
from metal_parser import get_metals_now, get_metals_weeks


# TODO: обработать все возможные ошибки пользователя  (22.11.2023)

# TODO: настроить команды для пользователя: /help

# TODO: Сделать кнопки для выбора периода (Неделя, месяц, 3 месяца, 6 месяцев, год, свой вариант)


"""
/start
/help 
/actual_currency
/actual_crypto
"""

bot = Bot(token=Token_Telegram_bot, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
binance_client = AsyncClient()


class DataInput(StatesGroup):
    choice = State()
    send_photo = State()

    # Металлы
    metal_type = State()
    metal_type_now = State()
    date_1 = State()
    date_2 = State()

    # Валюта
    currency_type = State()
    currency_type_now = State()
    date_1_currency = State()
    date_2_currency = State()

    # Крипта
    crypto_type = State()
    crypto_type_now = State()
    date_1_crypto = State()
    date_2_crypto = State()


#######################commands#######################################

# Ваш обработчик команды /start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    # Создание кнопок для выбора
    btn1 = InlineKeyboardButton(text="Металлы", callback_data="choice_metal")
    btn2 = InlineKeyboardButton(text="Валюты", callback_data="choice_currency")
    keyboard.row(btn1, btn2)

    btn3 = InlineKeyboardButton(text="Криптовалюты", callback_data="choice_crypto")
    keyboard.row(btn3)

    await message.answer("Привет! Это бот для отслеживания различных курсов")
    await message.answer("Что вы хотите посмотреть?", reply_markup=keyboard)


@dp.message_handler(commands="actual_crypto")  # крипта
async def handle_crypto_price(message: types.Message):
    # await message.answer("Напиши имя валюту, чтобы узнать актуальный курс")

    keyboard_crypto = types.InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="BTC", callback_data="BTC_now")
    btn2 = InlineKeyboardButton(text="ETH", callback_data="ETH_now")
    keyboard_crypto.row(btn1, btn2)

    btn3 = InlineKeyboardButton(text="BNB", callback_data="BNB_now")
    btn4 = InlineKeyboardButton(text="DOGE", callback_data="DOGE_now")
    keyboard_crypto.row(btn3, btn4)

    btn5 = InlineKeyboardButton(text="Вести свою валюту", callback_data="another_now_crypto")
    keyboard_crypto.row(btn5)

    await message.answer("Какую валюту вы хотите просмотреть?", reply_markup=keyboard_crypto)


@dp.message_handler(commands="actual_currency")  # валюта
async def handle_currency_price(message: types.Message):
    # await message.answer("Напиши имя валюту, чтобы узнать актуальный курс")
    keyboard_crypto = types.InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="Доллар", callback_data="Dollar_now")
    btn2 = InlineKeyboardButton(text="Евро", callback_data="Euro_now")
    btn3 = InlineKeyboardButton(text="Юань", callback_data="Yuan_now")
    keyboard_crypto.row(btn1, btn2, btn3)

    btn5 = InlineKeyboardButton(text="Вести свою валюту", callback_data="another_now_currency")
    keyboard_crypto.row(btn5)

    await message.answer("Какую валюту вы хотите просмотреть?", reply_markup=keyboard_crypto)


#  actual metals
@dp.message_handler(commands="actual_metals")
async def handle_metals_price(message: types.Message):
    keyboard_metal = types.InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text="Золото", callback_data="metal_gold_now")
    btn2 = InlineKeyboardButton(text="Серебро", callback_data="metal_silver_now")
    keyboard_metal.row(btn1, btn2)

    btn3 = InlineKeyboardButton(text="Платина", callback_data="metal_platinum_now")
    btn4 = InlineKeyboardButton(text="Палладий", callback_data="metal_palladium_now")
    keyboard_metal.row(btn3, btn4)

    # btn5 = InlineKeyboardButton(text="Вести свою валюту", callback_data="metals_now_another")
    # keyboard_metal.row(btn5)

    await message.answer("Какой металл вы хотите просмотреть?", reply_markup=keyboard_metal)


##################################################################################################


# ##############actual_metals###################
# Обработчики нажатий кнопок | ВАЛЮТА # ISO 4217
@dp.callback_query_handler(lambda c: c.data in ["metal_gold_now", "metal_silver_now", "metal_platinum_now", "metal_palladium_now"])
async def process_choice_currency(callback_query: types.CallbackQuery, state: FSMContext):
    metal_type = {
        "metal_gold_now": "Золото",
        "metal_silver_now": "Серебро",
        "metal_platinum_now": "Платина",
        "metal_palladium_now": "Палладий"
        # "another_now_currency": "Другая"
    }.get(callback_query.data)

    currency = metal_type
    result = get_metals_now(currency, "now")

    try:
        await callback_query.message.answer(f"Вы выбрали: {currency}")
        await callback_query.message.answer(f"{result}")
        await state.finish()
    except Exception as e:
        print(f"ОШИКБА ПРИ ПОЛУЧЕНИИ МЕТАЛЛОВ АКУТАЛ {e}")
        await callback_query.message.answer(f"Ошибка при получении данных")
        await state.finish()


# ##############actual_currency###################
# Обработчики нажатий кнопок | ВАЛЮТА # ISO 4217
@dp.callback_query_handler(lambda c: c.data in ["Dollar_now", "Euro_now", "Yuan_now", "another_now_currency"])
async def process_choice_currency(callback_query: types.CallbackQuery, state: FSMContext):
    currency_type = {
        "Dollar_now": "USD",
        "Euro_now": "EUR",
        "Yuan_now": "CNY",
        "another_now_currency": "Другая"
    }.get(callback_query.data)

    if currency_type == "Другая":
        iso = hlink("ISO 4217", "https://www.iban.ru/currency-codes")
        await callback_query.message.answer(f"Напишите какую валюту вы хотите посмотреть. К примеру: USD или EUR.\n"
                                            f"Так же можете воспользоваться {iso}", disable_web_page_preview=True)
        await state.set_state(DataInput.currency_type_now)
    else:
        currency = currency_type
        result = actual_curse(currency)

        if result == "Ошибка при получении данных":
            await callback_query.message.answer("Ошибка при получении данных")
            await state.finish()
        else:
            # print(f"BIM BIM BAM BAM {result}")
            result = float(result)
            await callback_query.message.answer(f"Цена {result:.2f} на {currency}")


# Хендлер для выбора обычной валюты на данный момент
@dp.message_handler(state=DataInput.currency_type_now)
async def process_currency_choice_now(message: types.Message, state: FSMContext):
    base_currency = message.text
    base_currency.upper()

    result = actual_curse(base_currency)
    if result == "Ошибка при получении данных":
        await message.answer("Ошибка при получении данных или некорректный ввод.")
        await state.finish()
    else:
        result = float(result)
        await message.answer(f"Цена {result:.2f} на {base_currency}")
        await state.finish()


# ##############actual_crypto###################
# Обработчики нажатий кнопок | крипта
@dp.callback_query_handler(lambda c: c.data in ["BTC_now", "ETH_now", "BNB_now", "DOGE_now", "another_now_crypto"])
async def process_choice_crypto(callback_query: types.CallbackQuery, state: FSMContext):
    choice = callback_query.data
    # await bot.answer_callback_query(callback_query.id)

    crypto_type = {
        "BTC_now": "BTCUSDT",
        "ETH_now": "ETHUSDT",
        "BNB_now": "BNBUSDT",
        "DOGE_now": "DOGEUSDT",
        "another_now_crypto": "Другая"
    }.get(callback_query.data)

    print(crypto_type)

    if crypto_type == "Другая":
        await callback_query.message.answer("Напишите какую валюту вы хотите посмотреть. Пример ввода: BTCUSDT. \n"
                                            "Данные берутся с Binance")  # make hlink ?
        await state.set_state(DataInput.crypto_type_now)
    else:
        coin = crypto_type
        try:
            ticker_date = await binance_client.get_ticker(symbol=coin)
        except BinanceAPIException as e:
            await callback_query.message.reply("Не найдено. Проверьте написание валюту")
            print(e)
            # return e
            await state.finish()

        print(ticker_date)

        price_coin = ticker_date["lastPrice"]
        # formatted_price = "{:.3f}".format(price_coin)

        price_coin = float(price_coin)
        await callback_query.message.answer(f"Цена {coin}: {price_coin:.5f}$")
        await state.finish()


# Хендлер для выбора крипты на данный момент
@dp.message_handler(state=DataInput.crypto_type_now)
async def process_crypto_choice_now(message: types.Message, state: FSMContext):
    coin = message.text
    coin.upper()

    try:
        ticker_date = await binance_client.get_ticker(symbol=coin)
    except BinanceAPIException as e:
        await message.reply("Не найдено. Проверьте написание валюту")
        print(e)
        # return e
        await state.finish()

    print(ticker_date)

    price_coin = ticker_date["lastPrice"]
    # formatted_price = "{:.3f}".format(price_coin)

    price_coin = float(price_coin)
    await message.answer(f"Цена {coin}: {price_coin:.5f}$")

    await state.finish()


##########################################################

# Обработчики нажатий кнопок
@dp.callback_query_handler(lambda c: c.data in ["choice_metal", "choice_currency", "choice_crypto"])
async def process_choice(callback_query: types.CallbackQuery, state: FSMContext):
    choice = callback_query.data
    await bot.answer_callback_query(callback_query.id)

    choice_type = {
        "choice_metal": "Металлы",
        "choice_currency": "Валюта",
        "choice_crypto": "Криптовалюта"
    }.get(callback_query.data)

    print(choice)

    await state.update_data(choice=choice_type)

    print(choice_type)

    # Далее можете продолжить логику обработки в зависимости от выбора
    if choice == "choice_metal":
        # Обработка выбора металлов
        await callback_query.message.answer("Вы выбрали Металлы.")

        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="Золото", callback_data="metal_gold"))
        keyboard.add(InlineKeyboardButton(text="Серебро", callback_data="metal_silver"))
        keyboard.add(InlineKeyboardButton(text="Платина", callback_data="metal_platinum"))
        keyboard.add(InlineKeyboardButton(text="Палладий", callback_data="metal_palladium"))

        await callback_query.message.answer("Какой металл вы хотите просмотреть?", reply_markup=keyboard)

    # Здесь продолжите логику для обработки выбранного варианта
    elif choice == "choice_currency":
        # Обработка выбора валют
        await callback_query.message.answer("Вы выбрали Валюты.")

        # keyboard_currency = InlineKeyboardMarkup()
        # btn1_dollar = keyboard_currency.add(InlineKeyboardButton(text="Доллар", callback_data="dollar"))
        # btn2_euro = keyboard_currency.add(InlineKeyboardButton(text="Евро", callback_data="euro"))
        # btn3_yuan = keyboard_currency.add(InlineKeyboardButton(text="Юань", callback_data="yuan"))
        # keyboard_currency.row(btn1_dollar, btn2_euro, btn3_yuan)
        # keyboard.add(InlineKeyboardButton(text="Палладий", callback_data="metal_palladium"))

        # if (btn1_dollar or btn2_euro or btn3_yuan) == None:
        #     await state.set_state(DataInput.currency_type)
        #     print("В условии IF btn")
        #     print(f"bim bim{btn2_euro}")
        # else:
        #     await callback_query.message.answer("Какую валюту вы хотите просмотреть?", reply_markup=keyboard)
        #     print("else")
        # await process_currency_choice(message, state)

        keyboard_currency = InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton(text="Доллар", callback_data="dollar")
        btn2 = InlineKeyboardButton(text="Евро", callback_data="euro")
        btn3 = InlineKeyboardButton(text="Юань", callback_data="yuan")
        keyboard_currency.row(btn1, btn2, btn3)

        btn4 = InlineKeyboardButton(text="Вести свою валюту", callback_data="another")
        keyboard_currency.row(btn4)

        await callback_query.message.answer("Какую валюту вы хотите просмотреть?", reply_markup=keyboard_currency)

        # if callback_query.message.text != None:
        #     await state.set_state(DataInput.currency_type)
        #     print("В условии IF btn")

        # Здесь продолжите логику для обработки выбранного варианта
    elif choice == "choice_crypto":
        # Обработка выбора криптовалют
        await callback_query.message.answer("Вы выбрали Криптовалюты.")

        keyboard_crypto = types.InlineKeyboardMarkup(row_width=2)
        btn1 = InlineKeyboardButton(text="BTC", callback_data="BTC")
        btn2 = InlineKeyboardButton(text="ETH", callback_data="ETH")
        keyboard_crypto.row(btn1, btn2)

        btn3 = InlineKeyboardButton(text="BNB", callback_data="BNB")
        btn4 = InlineKeyboardButton(text="DOGE", callback_data="DOGE")
        keyboard_crypto.row(btn3, btn4)

        btn5 = InlineKeyboardButton(text="Вести свою валюту", callback_data="another")
        keyboard_crypto.row(btn5)

        await callback_query.message.answer("Какую валюту вы хотите просмотреть?", reply_markup=keyboard_crypto)


# *************************Крипта*********************************

# Обработчик нажатий кнопок выбора конкретного металла
@dp.callback_query_handler(lambda c: c.data in ["BTC", "ETH", "BNB", "DOGE", "another"])
async def process_crypto_choice_keyboard(callback_query: types.CallbackQuery, state: FSMContext):
    crypto_type = {
        "BTC": "BTC",
        "ETH": "ETH",
        "BNB": "BNB",
        "DOGE": "DOGE",
        "another": "Другая"
    }.get(callback_query.data)

    await callback_query.message.answer(f"Выбранная валюта: {crypto_type}")

    await bot.answer_callback_query(callback_query.id)

    if crypto_type == "Другая":
        await callback_query.message.answer("Напишите какую валюту вы хотите посмотреть ")
        await state.set_state(DataInput.crypto_type)
    else:
        await callback_query.message.answer("Бот сможет показать график не больше, чем за 1 год и не раньше, "
                                            "чем 01.07.2017 год")

        await callback_query.message.answer("Введите первую дату в формате ДД.ММ.ГГГГ:")
        # Сохранение выбранного типа металла в FSM (Finite State Machine) для последующего использования
        await state.update_data(crypto_type=crypto_type)
        await state.set_state(DataInput.date_1_crypto)


# Хендлер для выбора крипты |  скобочка отрывается тире точка скобочка закрывается
@dp.message_handler(state=DataInput.crypto_type)
async def process_crypto_choice(message: types.Message, state: FSMContext):
    crypto_type = message.text
    await state.update_data(crypto_type=crypto_type)
    # await DataInput.date_1.set()
    # await message.answer(f"aboba | bam bim  ur choice {crypto_type}")

    await message.answer("Бот сможет показать график не больше, чем за 1 год и не раньше, "
                         "чем 01.07.2017 год")

    await message.answer("Введите первую дату в формате ДД.ММ.ГГГГ:")

    await DataInput.date_1_crypto.set()


# Обработчик ввода даты после выбора крипты
@dp.message_handler(state=DataInput.date_1_crypto)
async def process_date_1_crypto(message: types.Message, state: FSMContext):
    # Получаем введенную пользователем дату
    date_1_crypto = message.text

    # Сохраняем введенную пользователем дату для последующего использования
    await message.answer("Введите вторую дату в формате ДД.ММ.ГГГГ:")

    await state.update_data(date_1_crypto=date_1_crypto)
    await DataInput.date_2_crypto.set()


# Обработчик ввода даты2 после выбора валюты
@dp.message_handler(state=DataInput.date_2_crypto)
async def process_date_1_crypto(message: types.Message, state: FSMContext):
    # Получаем данные о типе металла из состояния FSM
    user_data = await state.get_data()
    crypto_type = user_data.get('crypto_type')
    date_1_crypto = user_data.get('date_1_crypto')
    choice = user_data.get('choice')

    # Получаем введенную пользователем дату
    date_2_crypto = message.text

    # Теперь у вас есть выбранный тип металла (metal_type) и введенная пользователем дата (date_1)
    # Можете продолжить логику обработки, например, запросить вторую дату
    print("КРИПТАА")
    # Сохраняем введенную пользователем дату для последующего использования

    user_id = message.from_user.id

    # await message.answer(f"Полученный ввод: {choice} || {crypto_type},|| {date_1_crypto}, || {date_2_crypto}")

    result = await main(choice, date_1_crypto, date_2_crypto, None, user_id, crypto_type)
    if result == "График готов":
        # await state.update_data(send_photo=True)

        start_date = datetime.strptime(date_1_crypto, "%d.%m.%Y")
        end_date = datetime.strptime(date_2_crypto, "%d.%m.%Y")

        delta = end_date - start_date
        if delta.days > 365:
            await message.answer("Вы выбрали временной интервал более 1 года. Бот сможет отобразить данные "
                                 "только за 1 год.")
            end_date = start_date + timedelta(days=365)

        end_date = end_date.strftime('%d.%m.%Y')
        start_date = start_date.strftime('%d.%m.%Y')

        await message.answer(f"Криптовалюта: {crypto_type} \n"
                             f"График построен с {start_date} по {end_date}")

        await state.set_state(DataInput.send_photo)
        await message.answer("Отправляю график:")
        await send_photo(message, state)

    elif result == "Введено неверное название валюты.":
        await message.answer("Введено неверное название валюты.")
        await state.finish()

    elif result == "Ошибка в дате":
        await message.answer(
            'Некорректные даты. Пожалуйста, введите даты в формате DD.MM.YYYY и убедитесь, что они находятся в '
            'диапазоне с 01.07.2017 по текущую дату.'
        )
        await state.finish()

    else:
        # print("BIM BIM BAM BAM")
        print(f" HERE {date_2_crypto}")
        await message.answer("Ошибка при создании графика.")
        await message.answer("Не удалось получить данные для построения графика.")
        await state.finish()


# *************************ВАЛЮТА*********************************

# Обработчик нажатий кнопок выбора конкретного металла
@dp.callback_query_handler(lambda c: c.data in ["dollar", "euro", "yuan", "another"])
async def process_currency_choice_keyboard(callback_query: types.CallbackQuery, state: FSMContext):
    currency_type = {
        "dollar": "Доллар США",
        "euro": "Евро",
        "yuan": "Китайский юань",
        "another": "Другая"
    }.get(callback_query.data)

    await callback_query.message.answer(f"Выбранная валюта: {currency_type}")

    await bot.answer_callback_query(callback_query.id)

    if currency_type == "Другая":
        await callback_query.message.answer("Напишите какую валюту вы хотите посмотреть ")
        await state.set_state(DataInput.currency_type)
    else:
        await callback_query.message.answer("Введите первую дату в формате ДД.ММ.ГГГГ:")
        # Сохранение выбранного типа металла в FSM (Finite State Machine) для последующего использования
        await state.update_data(currency_type=currency_type)
        await state.set_state(DataInput.date_1_currency)


# Хендлер для выбора валюты | Выбор валюты (доллары, рубли и т.д)
@dp.message_handler(state=DataInput.currency_type)
async def process_currency_choice(message: types.Message, state: FSMContext):
    currency_parser = message.text
    await state.update_data(currency_type=currency_parser)
    # await DataInput.date_1.set()

    print("ЗДЕСЬ ввода дата 1 валюта")

    await message.answer("Введите первую дату в формате ДД.ММ.ГГГГ:")

    await DataInput.date_1_currency.set()


# Обработчик ввода даты после выбора валюты
@dp.message_handler(state=DataInput.date_1_currency)
async def process_date_1_currency(message: types.Message, state: FSMContext):
    # Получаем введенную пользователем дату
    date_1_currency = message.text

    # Теперь у вас есть выбранный тип металла (metal_type) и введенная пользователем дата (date_1)
    # Можете продолжить логику обработки, например, запросить вторую дату
    print("ВВОД ДАТЫ В ВАЛЮТЕ1")
    # Сохраняем введенную пользователем дату для последующего использования
    await state.update_data(date_1_currency=date_1_currency)
    await DataInput.date_2_currency.set()
    await message.answer("Введите вторую дату в формате ДД.ММ.ГГГГ:")


# Обработчик ввода даты после выбора валюты
@dp.message_handler(state=DataInput.date_2_currency)
async def process_date_1_currency(message: types.Message, state: FSMContext):
    # Получаем данные о типе металла из состояния FSM
    user_data = await state.get_data()
    currency_type = user_data.get('currency_type')
    date_1_currency = user_data.get('date_1_currency')
    choice = user_data.get('choice')

    # Получаем введенную пользователем дату
    date_2_currency = message.text

    # Теперь у вас есть выбранный тип металла (metal_type) и введенная пользователем дата (date_1)
    # Можете продолжить логику обработки, например, запросить вторую дату
    print("ВВОД ДАТЫ В ВАЛЮТЕ2")
    # Сохраняем введенную пользователем дату для последующего использования

    date_2_currency = message.text
    user_id = message.from_user.id

    await message.answer(f"Полученный ввод: {choice} || {currency_type},|| {date_1_currency}, || {date_2_currency}")

    result = await main(choice, date_1_currency, date_2_currency, None, user_id, currency_type)
    if result == "График готов":
        # await state.update_data(send_photo=True)

        await state.set_state(DataInput.send_photo)
        await message.answer("Отправляю график:")
        await send_photo(message, state)

        # await state.set_state(DataInput.send_photo)
    else:
        print("BIM BIM BAM BAM")
        await message.answer("Ошибка при создании графика.")
        await state.finish()

    # await state.update_data(date_1_currency=date_2_currency)
    # await DataInput.date_2_currency.set()
    # await message.answer("Введите вторую дату в формате ДД.ММ.ГГГГ:")


# *************************Металлы*********************************

# Обработчик нажатий кнопок выбора конкретного металла
@dp.callback_query_handler(lambda c: c.data in ["metal_gold", "metal_silver", "metal_platinum", "metal_palladium"])
async def process_metal_choice(callback_query: types.CallbackQuery, state: FSMContext):
    metal_type = {
        "metal_gold": "Золото",
        "metal_silver": "Серебро",
        "metal_platinum": "Платина",
        "metal_palladium": "Палладий"
    }.get(callback_query.data)

    await callback_query.message.answer(f"Выбранный металл: {metal_type}")

    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.answer("Введите первую дату в формате ДД.ММ.ГГГГ:")
    # Здесь сохраните выбранный тип металла, чтобы использовать его в обработчике ввода даты

    # Сохранение выбранного типа металла в FSM (Finite State Machine) для последующего использования
    await state.update_data(metal_type=metal_type)
    await DataInput.date_1.set()


# Обработчик ввода даты после выбора металла
@dp.message_handler(state=DataInput.date_1)
async def process_date_1(message: types.Message, state: FSMContext):
    # Получаем данные о типе металла из состояния FSM
    user_data = await state.get_data()
    metal_type = user_data.get('metal_type')

    # Получаем введенную пользователем дату
    date_1 = message.text

    # Теперь у вас есть выбранный тип металла (metal_type) и введенная пользователем дата (date_1)
    # Можете продолжить логику обработки, например, запросить вторую дату

    # Сохраняем введенную пользователем дату для последующего использования
    await state.update_data(date_1=date_1)
    await DataInput.date_2.set()
    await message.answer("Введите вторую дату в формате ДД.ММ.ГГГГ:")


# Обработчик второй введенной даты
@dp.message_handler(state=DataInput.date_2)
async def process_date_2(message: types.Message, state: FSMContext):
    # Получаем данные о типе металла из состояния FSM
    user_data = await state.get_data()
    metal_type = user_data.get('metal_type')
    date_1 = user_data.get('date_1')
    choice = user_data.get('choice')

    # Получаем вторую введенную пользователем дату
    date_2 = message.text

    # Теперь у вас есть выбранный тип металла (metal_type) и две введенные пользователем даты (date_1 и date_2)
    # Можете использовать их для дальнейшей обработки, например, для получения данных о металле

    await message.answer(f"Полученный ввод: {choice} || {metal_type},|| {date_1}, || {date_2}")

    # await main(choice, date_1, date_2, metal_type)

    user_id = message.from_user.id

    # Проверяем результат выполнения main и переходим к следующему состоянию
    result = await main(choice, date_1, date_2, metal_type, user_id)
    if result == "График готов":
        # await state.update_data(send_photo=True)
        await state.set_state(DataInput.send_photo)
        await message.answer("Отправляю график:")
        await send_photo(message, state)
        # await state.set_state(DataInput.send_photo)
    else:
        await message.answer("Ошибка при создании графика.")
        await state.finish()

    print(f"BIM BIM BAM BAM  ")
    # await DataInput.send_photo.set()
    # await state.set_state(DataInput.send_photo.state)

    # await message.answer("Отправляю график:")
    # await DataInput.send_photo.set()
    # await state.set_state(DataInput.send_photo)

    # print("\n BIM BIM BAM BAM")
    # await state.finish()  # Завершаем FSM для этого пользователя


# ***************************************************************

# Отправка фото
@dp.message_handler(state=DataInput.send_photo)
async def send_photo(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    choice = user_data.get('choice')

    user_id = message.from_user.id

    print(f"sdff  {choice}")

    if choice == "Металлы":
        photo_path = open(f"data/graph_metal_user_{user_id}.png", "rb")
        # Отправка фотографии Send photo
        await bot.send_photo(message.chat.id, photo=photo_path)

        await message.answer("График отправлен!")
        print("Металлы")
        # Завершаем состояние FSM
        await state.finish()
    elif choice == "Валюта":
        photo_path = open(f"data/graph_currency_user_{user_id}.png", "rb")
        # Отправка фотографии
        await bot.send_photo(message.chat.id, photo=photo_path)
        print("Валюта")
        await message.answer("График отправлен!")
        # Завершаем состояние FSM
        await state.finish()
    elif choice == "Криптовалюта":
        photo_path = open(f"data/graph_cryptoCoin_user_{user_id}.png", "rb")
        # Отправка фотографии
        await bot.send_photo(message.chat.id, photo=photo_path)
        print("Валюта")
        await message.answer("График отправлен!")
        # Завершаем состояние FSM
        await state.finish()
    else:
        print("При отправке фото не было найдено совпадений")
        await state.finish()


@dp.message_handler(content_types="text")
async def process_text_message(message: types.Message):
    # Здесь вы можете обработать сообщение пользователя, которое не связано с выбором кнопок
    await message.reply("Пожалуйста, воспользуйтесь кнопками для выбора.")


# async def send_metal_price_time():
#     data_dict = get_metals_now(None, "now_time")
#     current_time = datetime.now().strftime("%H:%M")
#     #print(data_dict)
#
#     message = ""
#     try:
#         await bot.send_message(chat_id=792336120, text=f"Актуальные цена на данный момент: {current_time}")
#         #await bot.message.answer(f"{result}")
#         print("ЗДЕСЯ")
#         for i in range(1):
#             message += f"Дата: {data_dict['Дата'][i]} \n"
#             message += f"Золото: {data_dict['Золото'][i]} \n"
#             message += f"Серебро: {data_dict['Серебро'][i]} \n"
#             message += f"Платина: {data_dict['Платина'][i]} \n"
#             message += f"Палладий: {data_dict['Палладий'][i]} \n"
#         await bot.send_message(chat_id=792336120, text=f"Металлы: \n{message}")
#
#     except Exception as e:
#         print(f"ОШИКБА ПРИ ПОЛУЧЕНИИ МЕТАЛЛОВ АКУТАЛ отправка времени {e}")
#         await bot.send_message(chat_id=792336120, text=f"Ошибка при получении данных")

# {'Дата': ['02.12.2023'], 'Золото': ['5 874,1300'], 'Серебро': ['72,2100'], 'Платина': ['2 704,1000'], 'Палладий': ['2 958,0600']}


# Функция для запуска задачи в определенное время
# async def scheduler():
#     while True:
        # # Определите желаемое время выполнения задачи (время в формате HH:MM)
        # target_time = "21:27"  # Например, 9 утра
        #
        # # Получаем текущее время
        # current_time = datetime.now().strftime("%H:%M")
        #
        # # Если текущее время совпадает с желаемым временем
        # if current_time == target_time:
        #     # Вызываем функцию отправки сообщения с ценами металлов
        #     await send_metal_price_time()
        #
        # # Приостанавливаем выполнение на 1 минуту, чтобы избежать повторных запросов
        # print("scheduler")
        # await asyncio.sleep(60)

#
# async def main():
#     await scheduler()

# какая-то проблема, когда перезапускаешь он срабатывает
        # Создаем Task из корутины send_metal_price_time

        # Планируем выполнение задачи в определенное время (00:28)
        # aioschedule.every().day.at("01:18").do(send_metal_price_time)
        #
        # # Бесконечный цикл для проверки выполнения задачи
        # while True:
        #     await aioschedule.run_pending()
        #     await asyncio.sleep(5)


# async def on_startup(_):
#     asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(on_startup(None))
    # loop.run_forever()
    # loop.create_task(scheduler())
    # loop.run_forever()
