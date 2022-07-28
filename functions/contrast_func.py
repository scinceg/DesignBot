from telebot import types

# Подробнее про контрастность цветов
# https://ru.hexlet.io/blog/posts/chto-nuzhno-znat-o-kontraste-teksta-i-kak-kontrolirovat-kontrast-s-pomoschyu-sass

global colors, rate
colors = str()
rate = str()

# Принемает 2 параметра цвета: у одного из них больше относительная яркость
def color_contrast(c1, c2):
    # относительная яркость самого светлого цвета
    l1 = color_brightness(c1[0], c1[1], c1[2])
    # относительная яркость самого тёмного цвета
    l2 = color_brightness(c2[0], c2[1], c2[2])
    if l1 > l2:
        pass
    else:
        l1, l2 = l2, l1
    # Самый светлый делится на самый тёмный цвет
    return (l1 + 0.05) / (l2 + 0.05)

# Вычисление относительной яркости для цвета. Принемает r g b цвета
def color_brightness(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255

    color = [r, g, b]

    # Тело цикла применяяется для r, g, b
    for i in range(0, len(color)):
            if color[i] <= 0.03928:
                color[i] = color[i] / 12.92
            else:
                color[i] = ((color[i]+0.055)/1.055)**2.4

    l = 0.2126*color[0]+0.7152*color[1]+0.0722*color[2]
    return l

# Перевод цвета из hex формата в rgb
def hex_to_rgb(color):
    # Делим строку цвета на пары и добавляем их в массив rgb
    rgb = [color[0:2], color[2:4], color[4:6]]
    # Каждую пару из массива переводим из 16-ричной системы в 10-ричную
    for i in range(0, len(rgb)):
        rgb[i] = int(rgb[i], 16)
    # Возвращаем цвет в rgb формате
    return rgb

def contrast(message, bot):
    def func(message):
        # Записываем два цвета которые получили от пользователя
        colors = message.text
        # Делаем проверку на стоп функции
        if colors == "стоп":
            bot.send_message(message.from_user.id, "Вы на главной. Выберите нужный вам инструмент из клавиатуры.")
            return
        # Получаем раздельно каждый цвет. Делаем срез с 1 элемента строки с1 и срез colors.find(' ')+2: для того чтобы избавиться от # в начале
        c1 = colors[1:colors.find(' ')]
        c2 = colors[colors.find(' ')+2:]

        try:
            contrast_index = color_contrast(hex_to_rgb(c1), hex_to_rgb(c2))
        except:
            bot.send_message(message.from_user.id, 'Что-то не очень похоже на цвета. 🤔\n Попробуйте снова. Если вы хотите закончить, отправте <b>"cтоп"</b>', parse_mode="html")
            return contrast(message, bot)

        if contrast_index > 12:
            rate = "cупер! 🔥"
        elif contrast_index > 7:
            rate = "хороший 👍"
        elif contrast_index > 4.5:
            rate = "не очень 🤔"
        elif contrast_index > 3:
            rate = "плохой 👎"
        else:
            rate = "плохой 👎"

        bot.send_message(message.from_user.id, f"Коэффициент контраста данных цветов: <b>{round(contrast_index, 2)} из 21.</b> \n А значить контраст между вашими цветами - <b>{rate}.</b> \n\n Нажми на <b>'Контраст между цветами'</b> чтобы продолжить.", parse_mode="html")
    
    mesg = bot.send_message(message.from_user.id, "Проверка контраста. Отправте два цвета в hex формате через пробел и я вам скажу на сколько хороший контраст. \n\n <b>Например, черный и белый: ⚫#000000 ⚪#FFFFFF</b>", parse_mode="html")
    bot.register_next_step_handler(mesg, func)