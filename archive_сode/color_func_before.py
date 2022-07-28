from telebot import types
import random

# *** Кол-во вопросов должно быть равно кол-во цветов

global color_arr
color_arr = ["красный", "фиолетовый", "синий", "зелёный", "желтый", "оранжевый", "чёрно-белый", "розовый", "коричневый"]
global full_answers_if_true
full_answers_if_true = [
    ["синий", "чёрно-белый", "коричневый"],
    ["красный", "оранжевый", "желтый", "коричневый",],
    ["коричневый", "желтый", "чёрно-белый"],
    ["зелёный", "синий"],
    ["синий", "фиолетовый", "желтый", "оранжевый"],
    ["фиолетовый", "красный", "оранжевый", "розовый", "желтый"],
    ["чёрно-белый", "синий", "фиолетовый", "оранжевый", "желтый"],
    ["желтый", "синий", "зелёный", "оранжевый", "красный"],
    ["чёрно-белый", "синий", "фиолетовый", "красный"]
]

global questions
questions = [
    ["Ваш сайт - деловой?", 70, True, 0],
    ["Ваш сайт связан с едой?", 40, False, 0],
    ["Ваш сайт связан с роскошью?", 50, False, 0],
    ["Ваш сайт связан с деньгами?", 70, True, 0],
    ["Ваш сайт связан с образованием?", 10, False, 0],
    ["Ваш сайт про креативность?", 40, False, 0],
    ["Ваш сайт про технологии?", 10, False, 0],
    ["Ваш сайт связан с природой?", 10, False, 0],
    ["Ваш сайт про спорт?", 40, False, 0]
]

global count
count = list()

global past_quest
past_quest = list()

global is_end
is_end = False

def color(callback_query, bot, welcome_keyboard):
    
    # Making keeybaord
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_yes = types.InlineKeyboardButton("Да", callback_data="yes")
    btn_no = types.InlineKeyboardButton("Нет", callback_data="no")
    keyboard.add(btn_yes, btn_no)
    
    # Sending the message
    bot.send_message(callback_query.from_user.id, "Начнём выбор идеального цвета! \nВы отвечаете на вопросы, а я подбираю цвет. Погнали?", reply_markup=keyboard)

    # If answer is YES
    @bot.callback_query_handler(func=lambda c: c.data == "yes")
    def func(callback_query: types.CallbackQuery):
        # Receive the question
        # Try/exept construction is to exit the function if there is the Exception
        try:
            answer_index = questionAsk()
        except Exception:
            return

        bot.send_message(callback_query.from_user.id, questions[answer_index][0], reply_markup=keyboard)
        if_true(answer_index)

    # If answer is NO
    @bot.callback_query_handler(func=lambda c: c.data == "no")
    def func(callback_query: types.CallbackQuery):
        # Receive the question
        # Try/exept construction is to exit the function if there is the Exception
        try:
            answer_index = questionAsk()
        except Exception:
            return

        bot.send_message(callback_query.from_user.id, questions[answer_index][0], reply_markup=keyboard)
        if_false(answer_index)

    # Choosing the question
    def questionAsk():
        answer_index = random.randint(0, len(questions)-1)
        counter = 0
        while answer_index in past_quest:
            answer_index = random.randint(0, len(questions)-1)
            counter +=1
            # For the case of infinite cycle
            if counter > len(questions):
                final()
                raise Exception("The end of the funcs")
        
        past_quest.append(answer_index)
        return answer_index

    # Function for '+' answer
    def if_true(answer_index):
        for i in range(len(full_answers_if_true[answer_index])):
            for k in range(len(color_arr)):
                if full_answers_if_true[answer_index][i] == color_arr[k]:
                    count[k] += questions[k][1] 
                    questions[k][3] += 1 # Приорететность
                    print(count)
                    print(questions[k])

    # Function for '-' answer                
    def if_false(answer_index):
        for i in range(len(full_answers_if_true[answer_index])):
            for k in range(len(color_arr)):
                count[k] *= 0.5
                if questions[k][2]: 
                    count[k] *= 0.1
                    print(count)
                    print(questions[k])

    # Final
    def final():
        first = count.index(max(count))
        count.pop(first)
        second = count.index(max(count))
        count.pop(second)
        third = count.index(max(count))
        bot.send_message(callback_query.from_user.id, f"Ваши цвета - {color_arr[first]} или {color_arr[second]} или {color_arr[third]}!", 
            reply_markup=welcome_keyboard)

# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!
# Нужно исправить баг с кол-во вопросами в консоле!