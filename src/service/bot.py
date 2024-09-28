import telebot
from telebot import types
import requests
import json

from src.service.config import TELEGRAM_TOKEN, START_MESSAGE, HELP_MESSAGE

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['help'])
def help_(message):
    
    bot.send_message(message.from_user.id, HELP_MESSAGE)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, START_MESSAGE)

def get_answer_from_api(user_message):
    url = ''
    
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    
    data = {
        "history": [
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data.get('qa_answer', 'Извините, ответ не найден.')
    else:
        return 'Произошла ошибка при обращении к API.'

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_message = message.text
    
    bot_response = get_answer_from_api(user_message)
    
    bot.send_message(message.chat.id, bot_response)

try:
    bot.polling(none_stop=True, interval=0)
except Exception as e:
    print(f"Ошибка при запуске бота: {str(e)}")