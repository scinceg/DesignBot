import telebot
from telebot import types
import Data, Package
from functions import color_func, contrast_func, font_func, inspiration_func

bot = telebot.TeleBot(Package.TOKEN)

@bot.message_handler(commands=["start", "help"])
def welcome(message):
    welcome_str = "Привет! Я - бот, который поможет сделать твой дизайн красивым! Я могу: \n <b>--Выбирать подходящие цвета для сайта; 🟢 \n--Выбирать подходящие шрифты ; 🆎 \n--Вдохновлять дизайнеров; ✨  \n--Определить контраст между цветами ☑️.</b>"

    global keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_color = types.KeyboardButton("Цвета для сайта 🟢")
    btn_type = types.KeyboardButton("Шрифт для сайта 🆎")
    btn_brend = types.KeyboardButton("Вдохновить! ✨")
    btn_logo = types.KeyboardButton("Контраст между цветами ☑️")
    keyboard.add(btn_color, btn_type, btn_brend, btn_logo)

    bot.send_message(message.chat.id, welcome_str, reply_markup=keyboard, parse_mode="html")

@bot.message_handler(content_types=['text'])
def welcome(message):
    if message.text == "Цвета для сайта 🟢":
        color_func.color(message, bot, keyboard)
    elif message.text == "Шрифт для сайта 🆎":
        font_func.font(message, bot, keyboard)
    elif message.text == "Вдохновить! ✨":
        inspiration_func.inspiration(message, bot)
    elif message.text == "Контраст между цветами ☑️":
        contrast_func.contrast(message, bot)
    else:
        bot.send_message(message.chat.id, "Не могу вас понять. Пожалуйста, выбрите один из четырёх инструментов ниже.", reply_markup=keyboard)

bot.polling(none_stop=True)