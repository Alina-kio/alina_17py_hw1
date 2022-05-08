from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
import logging
from decouple import config
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

token = config("token")


bot = Bot(token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Hi, {message.from_user.full_name}")


@dp.message_handler(commands=['mem'])
async def pic(message: types.Message):
    photo = open("media/mem.jpg", 'rb')
    await bot.send_photo(message.from_user.id, photo=photo)


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data="button_call_1")
    markup.add(button_call_1)
    question = 'Когда появился термин «информационные технологии» в современном значении?'
    answers = ['В 1893 году', 'В 1990 году', 'В 1958 году']
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Да, это не так легко",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup
    )

@dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton("NEXT", callback_data="button_call_2")
    markup.add(button_call_2)
    question = "Какая поисковая система была самой популярной в 2011 году?"
    answers = ['Yahoo!', 'Google', 'Bing']
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Это же легко",
        explanation_parse_mode=ParseMode.MARKDOWN_V2,
    )



@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)
    await bot.send_message(message.from_user.id, int(message.text) ** 2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)