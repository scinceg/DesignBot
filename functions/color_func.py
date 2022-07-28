from telebot import types
import random
from functions.color_data import assoc_data, questions_data

global color_arr, assoc, questions, count, past_quest
color_arr = ["красный🔴", "жёлтый🟡", "синий🔵", "зелёный🟢", "фиолетовый🟣", "оранжевый🟠"]

assoc = assoc_data
questions = list()
for i in questions_data:
    questions.append(i)

# Собирает ассоциации с вопросов на которые ответили ДА
count = list()
# Массив с использованными вопросами
past_quest = list()

def color(callback_query, bot, welcome_keyboard):
    # Создание клавиатуры
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_yes = types.InlineKeyboardButton("Да", callback_data="color_yes")
    btn_no = types.InlineKeyboardButton("Нет", callback_data="color_no")
    keyboard.add(btn_yes, btn_no)
    
    # Отправка сообщения
    bot.send_message(callback_query.from_user.id, "Начнём выбор цветов! Вы отвечаете на вопросы, а я подбираю цвет. Погнали!")
    # Задаём первый вопрос
    bot.send_message(callback_query.from_user.id, questions[0][0], reply_markup=keyboard)
    # Добавляем его в массив использованных
    past_quest.append(0)

    # Если ответ ДА
    @bot.callback_query_handler(func=lambda c: c.data == "color_yes")
    def yes_handler(callback_query: types.CallbackQuery):
        # Добавляем ассоциации с прошлого вопроса на который пользователь ответил ДА
        count.extend(questions[past_quest[-1]][1])
        # Удаяляем прошлый вопрос из массива
        questions.pop(past_quest[-1])
        # Try/exept нужно для случая если вопросов в массиве не осталось. Выбираем новый вопрос
        try:
            quest_index = questionAsk()
        except Exception:
            final()
            # Если вопросов нет в массиве, завершаем программу
            return

        bot.send_message(callback_query.from_user.id, questions[quest_index][0], reply_markup=keyboard)

    # Если ответ НЕТ
    @bot.callback_query_handler(func=lambda c: c.data == "color_no")
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
            past_quest.append(quest_index) # Добавляем выбранный вопрос в массив с использовнными
        # в противном случае выбрасывает исключение
        else:
            raise Exception("The end of the function")

        return quest_index

    # Финальная функция
    def final():
        counter = [0]*len(color_arr)

        # Пробегаемся по всем элементам assoc и находим цвет у которого больше совпадений с count по ассоциациям
        for i in range(0, len(assoc)):
            for j in range(0, len(assoc[i])):
                for k in range(0, len(count)):
                    if count[k] == assoc[i][j]:
                       counter[i]+=1

        # Достаём индекс этого цвета (индекс совпадает с color_arr)
        win_color_index = counter.index(max(counter))
        # Final str
        final_str = f"Наиболее подходящий цвет для вашего сайта - <b>{color_arr[win_color_index]}</b>.\n\n Не забывайте о правиле 10:30:60. Этот цвет должен занимать не более 30% вашего сайта!\n\n Я предлагаю также: 👇"
        # Финальное сообщение
        bot.send_message(callback_query.from_user.id, final_str, reply_markup=welcome_keyboard, parse_mode="html")
        # Восстанавливаем данные для следующих игр
        for i in questions_data:
            questions.append(i)
        count.clear()
        # Завершаем работу функции
        return

# Нужно доработать полное завершение функции color в конце
# Нужно доработать полное завершение функции color в конце
# Нужно доработать полное завершение функции color в конце
# Нужно доработать полное завершение функции color в конце
# Нужно доработать полное завершение функции color в конце