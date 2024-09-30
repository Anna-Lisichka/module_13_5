from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# kb = ReplyKeyboardMarkup()
buttons = [['Рассчитать', 'Информация']]
kb = ReplyKeyboardMarkup(buttons, resize_keyboard=True)


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=kb)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте пока отсутствует, выбери другую кнопку')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст (в годах):")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f'Если Вы мужчина, то Ваша норма колорий: '
                         f'{10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5}')
    await message.answer(f'Если Вы женщина, то Ваша норма колорий: '
                         f'{10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161}')

    await state.finish()


@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start чтобы начать общение")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
