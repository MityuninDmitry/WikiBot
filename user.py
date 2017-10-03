from timeit import default_timer


class User_from_telegramm:
    def __init__(self,id):
        self.id = id
        self.user_name = ''
        self.number_of_page = 0
        self.last_search_text = ''
        self.last_search_message = ''
        self.get_message = False
        self.start_life = default_timer()

    def set_user_name(self,name):
        self.user_name = name
    def get_user_name(self):
        return self.user_name

# установить флаг получения сообщения
    def set_user_got_message(self,option):
        self.get_message = option
    def get_user_got_message(self):
        return self.get_message
# устанавливаем последнее сообщение и получаем его
    def set_last_search_message(self,last_search_message):
        self.last_search_message = last_search_message

    def get_last_search_message(self):
        return self.last_search_message
# устанавливаем номер последней страницы и получаем его
    def set_number_of_page(self,number_of_page):
        if number_of_page >= 0:
            self.number_of_page = number_of_page
        else:
            self.number_of_page = 0

    def get_number_of_page(self):
        return self.number_of_page
# сохраняем и получаем массив параграфов текста
    def set_last_search_text(self,text):
        self.last_search_text = text

    def get_last_search_text(self):
        try:
            if 'Состояниеотпатрулирована' in self.last_search_text[self.number_of_page]:
                self.number_of_page += 1
            return self.last_search_text[self.number_of_page]
        except IndexError:
            self.number_of_page = len(self.last_search_text)
            return 'I am sorry, but your page is end. Try to find something new.'
# получаем ИД юзера
    def get_user_id(self):
        return  self.id
# устанавливаем оффсет и получаем его
    def set_last_offset(self,offset):
        self.last_offset = offset

    def get_last_offset(self):
        return self.last_offset

# устанавливаем чат ИД и получаем его
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def get_chat_id(self):
        return self.chat_id
# распечатать инфу о пользователе
    def print_user_info(self):
        print('last search message: ', self.last_search_message)
        print('Number of page: ', self.number_of_page)
        print('User id: ', self.id)
        # print('Chat id: ', self.chat_id)
        # print('Last offset: ', self.last_offset)
        # print('Get meessage? : ',self.get_message)