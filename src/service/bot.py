import json

import requests
import telebot
from telebot import types

TELEGRAM_TOKEN = "7763328084:AAEXDAEBaUkTsB3wEmAwTI4Lc4r8-ekNrrU"

START_MESSAGE = "Привет, мой дорогой друг! Я твой чат-бот, ассистент команды Gaiki. Можешь задавать вопросы о нашей команде, и я буду рад помочь!"
HELP_MESSAGE = "/start - запуск бота с приветственным сообщением\n/help - список команд"


bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["help"])
def help_(message: types.Message) -> None:
    """Отправляет пользователю сообщение помощи."""
    bot.send_message(message.from_user.id, HELP_MESSAGE)


@bot.message_handler(commands=["start"])
def start(message: types.Message) -> None:
    """Отправляет пользователю приветственное сообщение."""
    bot.send_message(message.from_user.id, START_MESSAGE)


def get_answer_from_api(user_message: str) -> str:
    """
    Отправляет запрос к API и получает ответ.

    :param user_message: Сообщение пользователя.
    :return: Ответ от API или сообщение об ошибке.
    """
    text_url = "http://5.182.86.183:27361/api/v1/get_answer"  # Укажите URL вашего API

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    payload = {
    "history": [
        {
        "role": "user",
        "content": "Отвечай кратко и по делу, но учитывая всю специфику вопроса" + user_message
        }
    ]
    }

    response = requests.post(text_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("qa_answer", "Извините, ответ не найден.")
    else:
        return "Произошла ошибка при обращении к API."


@bot.message_handler(content_types=["text"])
def handle_text(message: types.Message) -> None:
    """
    Обрабатывает текстовые сообщения от пользователей.

    :param message: Сообщение от пользователя.
    """
    user_message = message.text
    bot_response = get_answer_from_api(user_message)
    bot.send_message(message.chat.id, bot_response)


try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Ошибка при запуске бота: {str(e)}")
