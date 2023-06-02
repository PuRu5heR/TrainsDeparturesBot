import os

from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import dotenv
import parser


def main():
    dotenv.load_dotenv()
    token = os.getenv("TOKEN")
    bot = Bot(token)
    disp = Dispatcher(bot, storage=MemoryStorage())

    class States(StatesGroup):
        StateReadyToSearch = State()
        StateInputDepartureCountry = State()
        StateInputDepartureCity = State()
        StateInputArrivalCountry = State()
        StateInputDateFrom = State()
        StateInputDateTo = State()
        StateInputNightsFrom = State()
        StateInputNightsTo = State()
        StateInputAdultsCount = State()
        StateInputChildremChoosing = State()
        StateInputHotelQuality = State()
        StateSearching = State()

    @disp.message_handler(commands=['start'])
    async def starting(sms: types.Message):
        keyboard = types.ReplyKeyboardRemove()
        message = "Добро пожаловать!\n" \
                  "Вы попали в телеграм-бот, который умеет только искать информацию про курорты.\nХотите начать поиск?" \
                  "Команда: /search"
        await sms.answer(message, reply_markup=keyboard)

    @disp.message_handler(commands=['search'])
    async def search_start(sms: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Поиск"))
        await bot.send_message(sms.from_user.id, "Начать поиск?", reply_markup=keyboard)
        await States.StateReadyToSearch.set()

    @disp.message_handler(state=States.StateReadyToSearch)
    async def ready_do_search(sms: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Россия"), types.KeyboardButton(text="Беларусь"),
                     types.KeyboardButton(text="Казахстан"), types.KeyboardButton(text="Пропустить"))
        if sms.text == "Поиск":
            await sms.answer("Из какой страны собираетесь вылетать?\n"
                             "(если ввести некорректную информацию, то будет выбран параметр по умолчанию)",
                             reply_markup=keyboard)
            await States.next()
        else:
            await sms.answer("Не знаю такого! Попробуйте ещё раз")

    @disp.message_handler(state=States.StateInputDepartureCountry)
    async def input_departure_country(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['departure_country'] = sms.text
            else:
                data['departure_country'] = ""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Пропустить"))
        await sms.answer("Введите город вылета:", reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputDepartureCity)
    async def input_departure_city(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['departure_city'] = sms.text
            else:
                data['departure_city'] = ""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Абхазия"), types.KeyboardButton(text="Азербайджан"),
                     types.KeyboardButton(text="Венесуэла"), types.KeyboardButton(text="Вьетнам"))
        keyboard.row(types.KeyboardButton(text="Египет"), types.KeyboardButton(text="Израиль"),
                     types.KeyboardButton(text="Индия"), types.KeyboardButton(text="Индонезия"))
        keyboard.row(types.KeyboardButton(text="Киргизия"), types.KeyboardButton(text="Куба"),
                     types.KeyboardButton(text="Мальдивы"), types.KeyboardButton(text="ОАЭ"))
        keyboard.row(types.KeyboardButton(text="Россия"), types.KeyboardButton(text="Сейшелы"),
                     types.KeyboardButton(text="Таиланд"), types.KeyboardButton(text="Танзания"))
        keyboard.row(types.KeyboardButton(text="Тунис"), types.KeyboardButton(text="Турция"),
                     types.KeyboardButton(text="Шри-Ланка"), types.KeyboardButton(text="Пропустить"))
        await sms.answer("Куда хотите отправиться?\n"
                         "(если ввести некорректную информацию, то будет выбран параметр по умолчанию):",
                         reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputArrivalCountry)
    async def input_arrival_country(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['arrival_country'] = sms.text
            else:
                data['arrival_country'] = ""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Пропустить"))
        await sms.answer("Введите, с какого числа начинать поиск туров, в формате ДД.ММ.ГГГГ\n"
                         "(некорректный ввод сделает параметр по умолчанию", reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputDateFrom)
    async def input_date_from(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['date_from'] = sms.text
            else:
                data['date_from'] = ""
                data['date_to'] = ""
        if sms.text != "Пропустить":
            keyboard = types.ReplyKeyboardRemove()
            await sms.answer("Введите крайнюю дату тоже в формате ДД.ММ.ГГГГ (пропускать нельзя)",
                             reply_markup=keyboard)
            await States.next()
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
            keyboard.row(types.KeyboardButton(text="Пропустить"))
            await sms.answer("Введите минимальное количество ночей для тура:\n(минимальное - 1)", reply_markup=keyboard)
            await States.StateInputNightsFrom.set()

    @disp.message_handler(state=States.StateInputDateTo)
    async def input_date_to(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['date_to'] = sms.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Пропустить"))
        await sms.answer("Введите минимальное количество ночей для тура:\n(минимальное - 1)", reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputNightsFrom)
    async def input_nights_count_from(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['nights_count_from'] = sms.text
            else:
                data['nights_count_from'] = ""
                data['nights_count_to'] = ""
            if sms.text != "Пропустить":
                keyboard = types.ReplyKeyboardRemove()
                await sms.answer("Введите максимальное количество ночей для тура:\n(максимальное - 28)",
                                 reply_markup=keyboard)
                await States.next()
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
                keyboard.row(types.KeyboardButton(text="Пропустить"))
                await sms.answer("Введите количество взрослых\n(минимально - 1, максимально - 6", reply_markup=keyboard)
                await States.StateInputAdultsCount.set()

    @disp.message_handler(state=States.StateInputNightsTo)
    async def input_nights_count_to(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['nights_count_to'] = sms.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Пропустить"))
        await sms.answer("Введите количество взрослых\n(минимально - 1, максимально - 6", reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputAdultsCount)
    async def input_adults(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['adults'] = sms.text
            else:
                data['adults'] = ""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Пропустить"))
        await sms.answer("Введите через запятую возраст каждого ребёнка, если они есть\n"
                         "(максимальное количество детей - 3, дети не старше 15 лет)\n"
                         "Пример: '2, 10, 15'", reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputChildremChoosing)
    async def input_children(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['children'] = sms.text
            else:
                data['children'] = ""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="1"), types.KeyboardButton(text="2"),
                     types.KeyboardButton(text="3"))
        keyboard.row(types.KeyboardButton(text="4"), types.KeyboardButton(text="5"),
                     types.KeyboardButton(text="Пропустить"))
        await sms.answer("Выберите сколько минимум звёзд должно быть у отеля:", reply_markup=keyboard)
        await States.next()

    @disp.message_handler(state=States.StateInputHotelQuality)
    async def input_stars(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            if sms.text != "Пропустить":
                data['stars'] = sms.text
            else:
                data['stars'] = ""
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="Buttons!")
        keyboard.row(types.KeyboardButton(text="Поиск"))
        await sms.answer("Параметры внесены", reply_markup=keyboard)
        await States.StateSearching.set()

    @disp.message_handler(state=States.StateSearching)
    async def searching(sms: types.Message, state: FSMContext):
        async with state.proxy() as data:
            pass
        await bot.send_message(sms.from_user.id, "Загрузка... Подождите немного")
        texts = []
        run = True
        while run:
            try:
                pars = parser.Parser(data['departure_country'], data['departure_city'], data['arrival_country'],
                                     data['date_from'], data['date_to'], data['nights_count_from'],
                                     data['nights_count_to'], data['adults'], data['children'], data['stars'])
                texts = pars.parsing()
                run = False
            except Exception:
                pass
        for text in texts:
            await bot.send_message(sms.from_user.id, text)
        await state.finish()

    executor.start_polling(disp)


if __name__ == "__main__":
    main()
