import requests
import re
import bs4


class Interract_with_wiki:
    # инициализируем объект класса
    def __init__(self,message): # при инициализации необходимо указать сообщение для поиска на вики
        self.message = 'https://ru.wikipedia.org/wiki/' + message # конечный урл запроса
        self.r = self.send_request() # в переменную сохраняет результат запроса
        self.soup = bs4.BeautifulSoup(''.join(self.r.text), "html.parser") # в переменную сохраняем текст страницы
        self.mas_result_text = [] # пустой массив, в коотром будут параграфы текста

    # посылаем реквест в вики и получаем ответ
    def send_request(self):
        try:
            return requests.get(self.message) # отправляем гет запрос и получаем ответ
        except:
            return 'I am sorry, but something wrong. Please try later' # если что-то пошло не так
    # получаем массив из параграфов
    def get_mass_of_text(self):
        # удалеям таблицу инфобоксов и прочие ненужные элементы
        for table in self.soup.findAll('table', "infobox"):
            table.extract()
        for div in self.soup.findAll('div', "toctittle"):
            div.extract()
        for div in self.soup.findAll('div', id="toc"):
            div.extract()
        for div in self.soup.findAll('div', id="footer"):
            div.extract()
        for table in self.soup.findAll('table'):
            table.extract()

        # идем по всем тегам в диве с контентом
        for tag in self.soup.find('div', id='content').findAll(True):
            # если название тега р или ul(параграф или перечисление), то
            if tag.name == 'p' or tag.name == 'ul':
                # удаляем все теги из блока текста
                pattern = '(\<(/?[^>]+)>)' # шаблон, по которому удалять теги
                result = re.sub(pattern, '', str(tag)) # замена шаблона на пустоту
                result = ''.join(result) # пересохраняем результат
                # print(result)

                # удаляем корявые символы, которые есть на странице
                pattern = '&#160;'
                result = re.sub(pattern, '', result)
                result = ''.join(result)
                # print(result)

                # добавляем кусок текста в массив
                self.mas_result_text.append(result)

                # удаляем пустые элементы и переходы
                for el in self.mas_result_text:
                    if not el:
                        self.mas_result_text.remove(el)
                    elif el == '\n':
                        self.mas_result_text.remove(el)
        # возращаем массив параграфов
        return self.mas_result_text








