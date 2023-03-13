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
    params = {}
    while True:
            try:
                response = requests.get(long_polling_url,headers=headers,params=params, timeout=90)
                homework = response.json()
                if homework.get('status') == 'timeout':
                    params = {
                        'timestamp': homework.get('timestamp_to_request')
                        }
                if homework.get('status') =='found':
                    params = {
                        'timestamp': homework.get('last_attempt_timestamp')
                        }
                if response.ok:
                    new_attempts = homework.get('new_attempts')
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
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(5)


def main():
    load_dotenv()
    tg_bot_token= os.environ['TG_BOT_TOKEN']
    tg_chat_id= os.environ['TG_CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']
    bot = telegram.Bot(token=tg_bot_token)
    
    get_homework_notification(bot, dvmn_token, tg_chat_id)

    
if __name__ == '__main__':
    main()
