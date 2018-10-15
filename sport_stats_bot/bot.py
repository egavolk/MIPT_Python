import requests  
import datetime
from sport_stats import Stats
import time

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=20000):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json().get('result')
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            return get_result[-1]
        else:
            return None


sport_bot = BotHandler('608454253:AAHrkHPsh33JjmaDByIeTe4zkgfcHNdYquA')  


def main():  
    new_offset = None
    data = Stats()
    mode = dict()
    cur_date = dict()
    cur_sport = dict()
    cur_tournament = dict()

    while True:
        time.sleep(1)
        for last_update in sport_bot.get_updates(new_offset):
            
            last_update_id = last_update['update_id']
            
            if not last_update['message'].get('text'):
                continue
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            chat_id = last_chat_id
            new_offset = last_update_id + 1

            if not mode.get(chat_id):
                mode[chat_id] = 0
                cur_date[chat_id] = ''
                cur_sport[chat_id] = ''
                cur_tournament[chat_id] = ''
            
            try:
                if last_chat_text.lower() == '/start':
                    mode[chat_id] = 0
                    sport_bot.send_message(chat_id, 'Введите дату. ГГГГ-ММ-ДД')
                    continue

                if last_chat_text.lower() == 'заново':
                    mode[chat_id] = 0
                    sport_bot.send_message(chat_id, 'Введите дату. ГГГГ-ММ-ДД')
                    continue

                if last_chat_text.lower() == 'назад':
                    mode[chat_id] = max(0, mode[chat_id] - 1)
                    if mode[chat_id] == 0:
                        sport_bot.send_message(chat_id, 'Введите дату. ГГГГ-ММ-ДД')
                    elif mode[chat_id] == 1:
                        i = 1
                        for sport in data.stats[cur_date[chat_id]].keys():
                            sport_bot.send_message(chat_id, str(i) + ') ' + sport)
                            i += 1
                    elif mode[chat_id] == 2:
                        i = 1
                        for sport in data.stats[cur_date[chat_id]][cur_sport[chat_id]].keys():
                            sport_bot.send_message(chat_id, str(i) + ') ' + sport)
                            i += 1
                    continue
            

                if mode[chat_id] == 0:
                    requests.post('https://news.sportbox.ru/stats/' + cur_date[chat_id])
                    response = requests.get('https://news.sportbox.ru/stats/' + cur_date[chat_id])
                    x = last_chat_text
                    if not (len(x) == 10 and x[0:4].isdigit() and x[5:7].isdigit() and int(x[5:7]) <= 12 and x[8:].isdigit() and int(x[8:]) <= 30):
                        sport_bot.send_message(chat_id, 'Некорректный ввод. Повторите попытку. Введите дату. ГГГГ-ММ-ДД')
                        continue
                    data.UpdateStatsDict(last_chat_text)

                    cur_date[chat_id] = last_chat_text
                    i = 1
                    for sport in data.stats[cur_date[chat_id]].keys():
                        sport_bot.send_message(last_chat_id, str(i) + ') ' + sport)
                        i += 1
                    mode[chat_id] = 1
                    continue

                if mode[chat_id] == 1:
                    i = 1
                    last_chat_text.strip()
                    if not last_chat_text.isdigit() or not 1 <= int(last_chat_text) <= len(data.stats[cur_date[chat_id]].keys()):
                        sport_bot.send_message(last_chat_id, 'Некорректный ввод. Повторите попытку. Введите номер вида спорта, \'назад\' или \'заново\'')
                        continue
                    cur_sport[chat_id] = list(data.stats[cur_date[chat_id]].keys())[int(last_chat_text) - 1]
                    for tournament in data.stats[cur_date[chat_id]][cur_sport[chat_id]].keys():
                        sport_bot.send_message(last_chat_id, str(i) + ') ' + tournament)
                        i += 1
                    mode[chat_id] = 2
                    continue

                if mode[chat_id] == 2:
                    i = 1
                    last_chat_text.strip()
                    if not last_chat_text.isdigit() or not 1 <= int(last_chat_text) <= len(data.stats[cur_date[chat_id]][cur_sport[chat_id]].keys()):
                        sport_bot.send_message(last_chat_id, 'Некорректный ввод. Повторите попытку. Введите номер соревнования, \'назад\' или \'заново\'')
                        continue
                    cur_tournament[chat_id] = list(data.stats[cur_date[chat_id]][cur_sport[chat_id]].keys())[int(last_chat_text) - 1]
                    for game in data.stats[cur_date[chat_id]][cur_sport[chat_id]][cur_tournament[chat_id]].keys():
                        sport_bot.send_message(last_chat_id, str(i) + ') ' + game)
                        i += 1
                    sport_bot.send_message(last_chat_id, 'Введите \'назад\' или \'заново\'')
                    mode[chat_id] = 3
                    continue

                if mode[chat_id] == 3:
                    sport_bot.send_message(last_chat_id, 'Некорректный ввод. Повторите попытку. Введите \'назад\' или \'заново\'')
                    continue
                
            except Exception as e:
                sport_bot.send_message(chat_id, e)
                        

if __name__ == '__main__':  
    main()
