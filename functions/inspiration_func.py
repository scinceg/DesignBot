from telebot import types
from bs4 import BeautifulSoup
import requests
import random

 # Парсинг сайта awwwards.com
def parsing():
    url = "https://www.awwwards.com/awwwards/collections/freelance-portfolio/"
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    # Список элементов с сайта
    list = soup.find('ul', class_='list-items').find_all('li')
    items_list = []
    for i in list:
        item = i.find('div', class_='box-item')
        # Если вознакает ошибка при получение данных item, то пропускаем его
        try:
            aauthor_link = "https://www.awwwards.com" + item.find('figure').find('a').get("href")
            aauthor = item.find('div', class_='by').find('strong').find('a').text
            # photo = item.find('div', class_='box-photo').find('img').get('data-srcset')
            # photo = photo[:photo.find(' ')]
            items_list.append([aauthor, aauthor_link])
        except AttributeError:
            pass
    # Возвращается случайный элемент из спика items_list
    # return items_list[random.randint(0, len(items_list)-1)]
    return items_list[random.randint(0, len(items_list)-1)]

def inspiration(callback_query, bot):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn = types.InlineKeyboardButton("Удивить меня! ✨", callback_data="handler")
    keyboard.add(btn)
    bot.send_message(callback_query.from_user.id, "Нажми на кнопку чтоб получить сайт для вдохновения.", reply_markup=keyboard)

    # Нужно оптивизировать

    @bot.callback_query_handler(func=lambda c: c.data == "handler")
    def func(callback_query: types.CallbackQuery):
        item = parsing()
        # bot.send_photo(callback_query.from_user.id, item[2])
        bot.send_message(callback_query.from_user.id, f"Дизайн на awwwards: {item[1]}\n\n Автор: {item[0]}", reply_markup=keyboard)