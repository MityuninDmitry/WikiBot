import requests
import http_module3 as wiki
import config
import json
import user


class My_telegram_bot:
    def __init__(self):
        self.offset = 0  # параметр необходим для подтверждения обновления
        self.URL = 'https://api.telegram.org/bot'  # URL на который отправляется запрос
        self.TOKEN = config.token  # токен вашего бота, полученный от @BotFather

        self.allUpdates = []
        self.allMyUpdates = []
        self.set_of_users_id = set() # уникальные значения id пользователей
        self.mas_of_users = [] # массив объектов пользователей
    # обновления, получаемые с телеграмма могут быть разного формата.
    # функция crete_my_updates все обновления приводит к единому "моему" виду для обработки
    def create_my_updates(self):
        updates = []
        for update in self.allUpdates:
            if 'callback_query' in update:
                data = {
                    'update_id': update['update_id'],
                    'message':
                        {
                       'message_id': update['callback_query']['message']['message_id'] ,
                       'from':
                           {
                           'id': update['callback_query']['message']['chat']['id'],
                           'first_name': update['callback_query']['message']['chat']['first_name'],
                           'last_name': update['callback_query']['message']['chat']['last_name'],
                           'language_code': 'ru-RU'
                           },
                       'chat':
                           {
                           'id': update['callback_query']['message']['chat']['id'],
                           'first_name': update['callback_query']['message']['chat']['first_name'],
                           'last_name': update['callback_query']['message']['chat']['last_name'],
                           'type': update['callback_query']['message']['chat']['type']
                           },
                        'date': update['callback_query']['message']['date'],
                        'text': update['callback_query']['data']
                        }
                }
            else:
                if 'text' in update['message']:
                    text = update['message']['text']
                else:
                    text = 'not text'
                data = {
                    'update_id': update['update_id'],
                    'message':
                        {
                            'message_id': update['message']['message_id'],
                            'from':
                                {
                                    'id': update['message']['chat']['id'],
                                    'first_name': update['message']['chat']['first_name'],
                                    'last_name': update['message']['chat']['last_name'],
                                    'language_code': 'ru-RU'
                                },
                            'chat':
                                {
                                    'id': update['message']['chat']['id'],
                                    'first_name': update['message']['chat']['first_name'],
                                    'last_name': update['message']['chat']['last_name'],
                                    'type': update['message']['chat']['type']
                                },
                            'date': update['message']['date'],
                            'text': text
                        }
                }
            updates.append(data)
        return updates
    def getUpdates(self):
        # получаем массив обновлений с помощью запроса
        request = requests.post(self.URL + self.TOKEN + '/getUpdates', {'offset': self.offset+1})

        # print(self.offset)
        self.allUpdates = request.json()['result'] # сохраняем все обновления в переменную
        # вид каждого обновления
        # {'update_id': 955948060,
        # 'message': {
        #       'message_id': 790,
        #       'from': {
        #           'id': 80192704,
        #           'first_name': 'Dmitry',
        #           'last_name': 'Mityunin',
        #           'language_code': 'ru-RU'},
    #           'chat': {
    #               'id': 80192704,
    #               'first_name': 'Dmitry',
    #               'last_name': 'Mityunin',
    #               'type': 'private'},
    #            'date': 1500552643,
    #            'text': 'ыва'}
        # }

        # для каждого обновления
        self.allMyUpdates = self.create_my_updates()
        for update in self.allMyUpdates:
            print(update)  # выводим джсон результата
            self.set_of_users_id.add(update['message']['from']['id']) # сохраняем новый уникальный id пользователя, если такой имеется

    # создаем нового пользователя
    def create_new_user(self):

        users_ids = set() # создаем пустой сет, куда будем складывать пользователей, которые уже есть

        for old_user in self.mas_of_users: # идем по всем пользователям
            users_ids.add(old_user.get_user_id()) # скаджываем id каждого пользоватлея в сет
        # в итоге у нас имеется сет из текущих пользователей

        # из сета всех ИД, которые были,  вычитаем те, по которым еще не было пользователя
        set_of_new_users = self.set_of_users_id - users_ids

        # идем по сету новых id
        for id in set_of_new_users:
            # добавляем нового пользователя
            self.mas_of_users.append(user.User_from_telegramm(id))
    # в результате переменная mas_of_users хранит массив объектов пользователей
    # обрабатываем текст пришедшего обновления пользователя
    def process_message_for_user(self,user_from_mass,update):
        # если обнволение следующая страница, то не обновляем сообщение, но обнволяем номер страницы
        if 'next_page' in update['message']['text']:
            user_from_mass.set_number_of_page(user_from_mass.get_number_of_page() + 1)
            user_from_mass.set_user_got_message(False)
            # если обнволение предыдущая страница, то не обновляем сообщение, но обнволяем номер страницы
        elif 'back_page' in update['message']['text']:
            user_from_mass.set_number_of_page(user_from_mass.get_number_of_page() - 1)
            user_from_mass.set_user_got_message(False)
            # если обнволение /help, то обновляем сообщение, но обнволяем номер страницы
        elif '/help' in update['message']['text']:
            user_from_mass.set_number_of_page(0)  # устанавливаем номер страницы
            user_from_mass.set_last_search_message(update['message']['text'])  # сохраняем новое сообщение
            user_from_mass.set_last_search_text(
                ['Send me what you want to search in Wikipedia and i will try to find it.'])
            user_from_mass.set_user_got_message(False)
            # если обнволение /start, то обновляем сообщение, но обнволяем номер страницы
        elif '/start' in update['message']['text']:
            user_from_mass.set_number_of_page(0)  # устанавливаем номер страницы
            user_from_mass.set_last_search_message(update['message']['text'])  # сохраняем новое сообщение
            user_from_mass.set_last_search_text(
                [
                    'Hello, ' + user_from_mass.get_user_name() + ', Send me what you want to search in Wikipedia and i will try to find it.'])
            user_from_mass.set_user_got_message(False)
            # если обнволение другое, то не обновляем сообщение и обнволяем номер страницы до 0
        else:
            user_from_mass.set_number_of_page(0)  # обнуляем номер параграфа
            user_from_mass.set_last_search_message(update['message']['text'])  # сохраняем новое сообщение
            # пользователю вызываем запрос на текст, который он хочет
            # сохраняем пользователю массив параграфов текста из вики
            mas_of_text_from_wiki = wiki.Interract_with_wiki(user_from_mass.get_last_search_message())
            text = mas_of_text_from_wiki.get_mass_of_text()
            user_from_mass.set_last_search_text(text)
            user_from_mass.set_user_got_message(False)

    # обновить данные каждого пользователя
    def update_every_user(self):
        # идем по всем обновлениям
        for update in self.allMyUpdates:
        # идем по всем пользователям
            for user_from_mass in self.mas_of_users:
        # сравниваем их id и находим совпадения соответствия обнволения пользователю
                if update['message']['from']['id'] == user_from_mass.get_user_id():
        # пользователю сохраняем обнволение
        # если у пользователя еще нет имени, то взять имя с чата
                    if user_from_mass.get_user_name() == '':
                        try:
                            user_from_mass.set_user_name(update['message']['from']['first_name'])
                        except:
                            user_from_mass.set_user_name('')
        # если в обнволении не текст, то сформировать пользователю варнинг
                    if 'not text' in update['message']['text']:
                        user_from_mass.set_number_of_page(0)  # обнуляем номер параграфа
                        # сохраняем пользователю массив параграфов текста
                        user_from_mass.set_last_search_text(
                            ['OOPS, but your last message was not text message. I can process just text messages for searching in Wikipedia.'])
                        user_from_mass.set_user_got_message(False)
        # иначе обработать текст в сообщении и сформировать ответ
                    else:
                        self.process_message_for_user(user_from_mass,update)
        # сохраняем пользователю оффсет
                    user_from_mass.set_last_offset(int(update['update_id']))
        # сохраняем пользователю ИД чата с которого он писал последнее сообщение
                    user_from_mass.set_chat_id(update['message']['chat']['id'])

    # послать свое сообщение для каждого пользователя
    def sendMessage(self):
        # идем по всем пользователям
        for user_from_mas in self.mas_of_users:
        # проверяем получил ли он ранее сообщение
            if user_from_mas.get_user_got_message() == False:
        # получаем данные и формируем сообщение

                data = {
                    'chat_id': user_from_mas.get_chat_id(),
                    'text': user_from_mas.get_last_search_text(),
                    'reply_markup': json.dumps(
                        {
                            'inline_keyboard':
                            [
                                [
                                    {
                                    'text': 'back_page',
                                    'callback_data': 'back_page'
                                    },
                                    {
                                    'text':'next_page',
                                    'callback_data': 'next_page'
                                    }
                                ]
                            ]

                        }
                    )
                }
            # посылаем сообщение
                requests.post(self.URL + self.TOKEN + '/sendMessage', data=data)
                user_from_mas.set_user_got_message(True)
            # обнвоить offset, чтобы следующее обновление прилетало
                self.offset = user_from_mas.get_last_offset()
                user_from_mas.print_user_info()
                # print(self.offset)
                # print('numbers of users: ', len(self.mas_of_users))



bot = My_telegram_bot() # создаем бота

while True: # запускаем его в цикле

    bot.getUpdates() # получаем обновления
    bot.create_new_user() # создаем нового пользователя
    bot.update_every_user() # обновляем данные каждого пользователя
    bot.sendMessage() # рассылаем сообщения
