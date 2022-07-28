from telebot import types
import random
from functions.font_data import questions_data, font_types_message_data, font_photos_data

# Переменые
global question_item, count, font_types, questions
# В count хранятся ответы на вопросы
count = list()
font_types = ["square", "round", "inclined", "handwritten", "stylized"]
# font types for adding in message
font_types_message = list()
font_photos = list()
questions = list()
past_quest = list()

# Пополняем списки
for i in questions_data:
    questions.append(i)
for i in font_types_message_data:
    font_types_message.append(i)
for i in font_photos_data:
    font_photos.append(i)

def font(callback_query, bot, welcome_keyboard):
    # Создание клавиатуры
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_yes = types.InlineKeyboardButton("Да", callback_data="font_yes")
    btn_no = types.InlineKeyboardButton("Нет", callback_data="font_no")
    keyboard.add(btn_yes, btn_no)

    # bot.register_next_step_handler(callback_query)

    # Отправка сообщения
    bot.send_message(callback_query.from_user.id, "Начнём выбор идеального шрифта для твоего брэнда!\n\n Вы отвечаете на вопросы, а я подбираю шрифт. Погнали!")
    # Задаём первый вопрос
    bot.send_message(callback_query.from_user.id, questions[0][0], reply_markup=keyboard)
    # Добавляем его в массив использованных
    past_quest.append(0)

    # Если ответ ДА
    @bot.callback_query_handler(func=lambda c: c.data == "font_yes")
    def yes_handler(callback_query: types.CallbackQuery):
        # Добавляем ассоциации с прошлого вопроса
        count.append(questions[past_quest[-1]][1])
        # Удаяляем прошлый вопрос из массива
        questions.pop(past_quest[-1])
        # Try/exept нужно для случая если вопросов в массиве не осталось
        try:
            quest_index = questionAsk()
        except Exception:
            final()
            # Если вопросов нет в массиве, завершаем программу
            return

        bot.send_message(callback_query.from_user.id, questions[quest_index][0], reply_markup=keyboard)

    # Если ответ НЕТ
    @bot.callback_query_handler(func=lambda c: c.data == "font_no")
    def no_handler(callback_query: types.CallbackQuery):
        # Удаяляем прошлый вопрос из массива
        questions.pop(past_quest[-1])
        # Try/exept нужно для случая если вопросов в массиве не осталось. Выбираем новый вопрос
        try:
            quest_index = questionAsk()
        except Exception:
            final()
            return

        # Пока ничего не делаем
        # Отправляем сообщение
        bot.send_message(callback_query.from_user.id, questions[quest_index][0], reply_markup=keyboard)

    # Выбор вопроса
    def questionAsk():
        # Здесь происходит условная проверка если есть вопросы в массиве то их задавать, 
        if len(questions) > 0:
            quest_index = random.randint(0, len(questions)-1)
            # Добавляем выбранный вопрос в массив с использовнными
            past_quest.append(quest_index)
        # в противном случае завершать программу
        else:
            raise Exception("The end of the function")

        return quest_index

    # Финальная функция
    def final():
        counter = [0]*len(font_types)

        for i in range(0, len(count)):
            for j in range(0, len(font_types)):
                if count[i] == font_types[j]:
                    counter[j]+=1

        # Достаём индекс этого цвета (индекс совпадает с font_types)
        win_index = counter.index(max(counter))
        # Фото
        photo = open(font_photos[win_index], 'rb')
        # Финальная строка
        final_str = f"Наиболее подходящий шрифт для вашего сайта или логотипа - <b>{font_types_message[win_index][0]}\n\nПримеры шрифтов: </b>{font_types_message[win_index][1]}\n\n Я предлагаю также: 👇"
        # Фото
        bot.send_photo(callback_query.from_user.id, photo)
        # Финальное сообщение
        bot.send_message(callback_query.from_user.id, final_str, reply_markup=welcome_keyboard, parse_mode="html")
        # Восстанавливаем данные для следующих игр
        for i in questions_data:
            questions.append(i)
        count.clear()