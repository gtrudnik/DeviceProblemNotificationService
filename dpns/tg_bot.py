from telebot.async_telebot import AsyncTeleBot
from dpns.config import settings
from dpns.db.connector import controller

bot = AsyncTeleBot(settings.token)
help_text = "test"


def check_permission(func):
    async def wrapper(message):
        user = await controller.get_user(tg_id=message.chat.id)
        if user is None:
            user = await controller.create_user(tg_id=message.chat.id)
        if user.role != "banned":
            return await func(message)
        else:
            return await bot.send_message(message.chat.id, "Вас заблокировали в этом сервисе")

    return wrapper


async def send_message(chat_id: int | list[int], message: str):
    """ Function for send message """
    if type(chat_id) == int:
        chat_id = [chat_id]
    for i in chat_id:
        await bot.send_message(i, message, timeout=5)


@bot.message_handler(commands=['start'])
@check_permission
async def start_message(message):
    await bot.send_message(message.chat.id, "Здравствуйте!" + help_text)


@bot.message_handler(commands=['help'])
@check_permission
async def help_message(message):
    await bot.send_message(message.chat.id, help_text)


@bot.message_handler(content_types=['text'])
@check_permission
async def new_message(message):
    # TODO: new problem
    print(message.chat.id)
    pass


async def start_bot():
    await bot.infinity_polling()
