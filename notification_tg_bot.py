import os
import time
import requests
import telegram
from dotenv import load_dotenv

def get_homework_notification(dvmn_token, tg_chat_id):
    long_polling_url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {dvmn_token}'
    }
    params = {
        'timestamp': 'last_attempt_timestamp',
    }
    try:
        while True:
            response = requests.get(long_polling_url,headers=headers, params=params)
            new_attempts = response.json().get('new_attempts')
            for item in new_attempts:
                lesson_title = item['lesson_title']
                lesson_url = item['lesson_url']
                is_negative = item['is_negative']
            text = f'Преподаватель проверил работу: "{lesson_title}"!\nСсылка: {lesson_url}!\n'
            if is_negative:
                text += '\nК сожалению, в работе нашлись ошибки!'
            else:
                text += '\nРабота принята, ты молодец!'
            if response.ok:
                bot.send_message(text=text, chat_id= tg_chat_id)
    except requests.exceptions.ReadTimeout:
        requests.get(long_polling_url,headers=headers, params=params, timeout=0.5)


if __name__ == '__main__':
    load_dotenv()
    tg_bot_token= os.environ['TG_BOT_TOKEN']
    tg_chat_id= os.environ['TG_CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)

    try:
        get_homework_notification(dvmn_token,tg_chat_id)
    except requests.exceptions.ConnectionError:
        time.sleep(5)
    except TypeError as ex:
        time.sleep(5)