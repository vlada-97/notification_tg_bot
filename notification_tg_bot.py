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
    response = requests.get(long_polling_url, headers=headers, params=params, timeout=90)
    if response.json().get('status') == 'timeout':
        params = {
            'timestamp': datetime.datetime.now().timestamp()
            }
    if response.ok:
        new_attempts = response.json().get('new_attempts')
        for attempt in new_attempts:
            lesson_title = attempt['lesson_title']
            lesson_url = attempt['lesson_url']
            is_negative = attempt['is_negative']
            text = f'Преподаватель проверил работу: "{lesson_title}"!\nСсылка: {lesson_url}!\n'
            if is_negative:
                text += '\nК сожалению, в работе нашлись ошибки!'
            else:
                text += '\nРабота принята, ты молодец!'
            bot.send_message(text=text, chat_id= tg_chat_id)


def main():
    load_dotenv()
    tg_bot_token= os.environ['TG_BOT_TOKEN']
    tg_chat_id= os.environ['TG_CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)

    while True:
        try:
            get_homework_notification(bot, dvmn_token, tg_chat_id)
        except requests.exceptions.ReadTimeout:
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            continue

if __name__ == '__main__':
    main()
