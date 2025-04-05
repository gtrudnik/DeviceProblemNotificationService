from telebot.async_telebot import AsyncTeleBot
from dpns.config import settings
from dpns.db.connector import controller
from telebot import types

bot = AsyncTeleBot(settings.token)
help_text = "test"


def add_buttons(text_buttons: list[str]):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for text in text_buttons:
        keyboard.add(types.KeyboardButton(text))
    return keyboard


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


async def start_problem(tg_id: int, device_id: int):
    await controller.update_tg_chat(tg_id=tg_id, stage="type_problem", device_id=device_id)
    problem_types = await controller.get_problem_types(device_id=device_id)
    problem_types = [problem.name_problem for problem in problem_types] + ["Другое", "Сбросить заявку❌"]
    menu_buttons = add_buttons(problem_types)
    ans = "Процесс создания заявки о проблеме на устройве запущен, выберите тип проблемы"
    return menu_buttons, ans


async def send_message(chat_id: int | list[int], message: str):
    """ Function for send message """
    if type(chat_id) == int:
        chat_id = [chat_id]
    for i in chat_id:
        await bot.send_message(i, message, timeout=5)


@bot.message_handler(commands=['start'])
@check_permission
async def start_message(message):
    args = message.text.split()[1:]  # Разделяем текст сообщения на части
    if args:
        print(args)
        try:
            menu_buttons, ans = await start_problem(message.chat.id, int(args[0]))
            await bot.send_message(message.chat.id, ans, timeout=5, reply_markup=menu_buttons)
        except:
            await bot.send_message(message.chat.id, "Возникла проблема, попробуйте ещё раз. "
                                                    "Если проблема не решится попробуйте через сайт.")
    else:
        response_message = "Привет! Как я могу помочь?"  # Сообщение по умолчанию
    await bot.send_message(message.chat.id, "Здравствуйте!" + help_text + " ")


@bot.message_handler(commands=['help'])
@check_permission
async def help_message(message):
    await bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['code'])
@check_permission
async def code_message(message):
    code = await controller.create_tg_code(tg_id=message.chat.id)
    await bot.send_message(message.chat.id,
                           f"Ваш телеграм id: {message.chat.id}\nКод: ||{str(code)}||",
                           parse_mode='MarkdownV2')


@bot.message_handler(content_types=['text'])
@check_permission
async def new_message(message):
    chat = await controller.get_tg_chat(tg_id=message.chat.id)
    menu_buttons = add_buttons(["Что умеет этот бот?"])
    tg_id = chat.tg_id
    stage = chat.stage
    msg: str = message.text
    ans = "Я не понял ваше сообщение, попробуйте ещё раз"

    if msg == "Что умеет этот бот?":
        await help_message(message=message)
        return
    elif msg == "Сбросить заявку❌":
        await controller.clear_tg_chat(tg_id=tg_id)
        ans = "Заявка сброшена"
    elif stage == "start":
        if msg.startswith("id="):
            device_id = int(msg.split("=")[-1].strip())
            menu_buttons, ans = await start_problem(tg_id, device_id)
    elif stage == "type_problem":
        ans = "Выберите тип проблемы"
        chat = await controller.get_tg_chat(tg_id=tg_id)
        problem_types = await controller.get_problem_types(device_id=chat.device_id)
        problem_types = [problem.name_problem for problem in problem_types] + ["Другое", "Сбросить заявку❌"]
        menu_buttons = add_buttons(problem_types)
        if msg in problem_types or msg == "Другое":
            ans = "Тип проблемы выбран, напишите описание вашей проблемы, в случае необходимости, не менее 10 символов или пропустите."
            menu_buttons = add_buttons(["Пропустить", "Сбросить заявку❌"])
            if msg == "Другое":
                msg = None
            await controller.update_tg_chat(tg_id=tg_id, stage="description", problem_type=msg)
    elif stage == "description":
        ans = "Напишите описание вашей проблемы, в случае необходимости, не менее 10 символов или пропустите."
        menu_buttons = add_buttons(["Пропустить", "Сбросить заявку❌"])
        if msg == "Пропустить" or len(msg) >= 10:
            if msg == "Пропустить":
                msg = None
            chat = await controller.get_tg_chat(tg_id=tg_id)
            user = await controller.get_user(tg_id=tg_id)
            await controller.create_problem(author_id=user.id,
                                            device_id=chat.device_id,
                                            description=msg,
                                            type_problem=chat.problem_type)
            await controller.clear_tg_chat(tg_id=tg_id)
            ans = "Заявка о проблеме успешно создана"

    await bot.send_message(chat.tg_id, ans, timeout=5, reply_markup=menu_buttons)


async def start_bot():
    await bot.infinity_polling()
