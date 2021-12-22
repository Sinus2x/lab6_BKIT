import telebot
from telebot import types
import config
import dbworker

# Создание бота
bot = telebot.TeleBot(config.TOKEN)


# Начало диалога
@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, 'Тут мы будем осуществлять перевод рублей в доллары')
    dbworker.set(dbworker.make_key(message.chat.id, config.CURRENT_STATE), config.States.STATE_RUBLE.value)
    bot.send_message(message.chat.id, 'Введите рубли:')


# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=['reset'])
def cmd_reset(message):
    bot.send_message(message.chat.id, 'Сброс результатов предыдущего ввода.')
    dbworker.set(dbworker.make_key(message.chat.id, config.CURRENT_STATE), config.States.STATE_RUBLE.value)
    bot.send_message(message.chat.id, 'Введите рубли:')


# Обработка первого числа
@bot.message_handler(func=lambda message: dbworker.get(
    dbworker.make_key(message.chat.id, config.CURRENT_STATE)) == config.States.STATE_RUBLE.value)
def first_num(message):
    text = message.text

    cond = False
    try:
        a = float(text)
    except ValueError:
        cond = True
    if not cond and a <= 0:
        cond = True

    if cond:
        # Состояние не изменяется, выводится сообщение об ошибке
        bot.send_message(message.chat.id, 'Проверка на дурака :) Введите положительное число:')
    else:
        bot.send_message(message.chat.id, f'Введено количество рублей - {text}')
        # Меняем текущее состояние
        dbworker.set(dbworker.make_key(message.chat.id, config.CURRENT_STATE), config.States.STATE_COURSE.value)
        # Сохраняем первое число
        dbworker.set(dbworker.make_key(message.chat.id, config.States.STATE_RUBLE.value), text)
        bot.send_message(message.chat.id, 'Теперь нужен курс доллара к рублю')


# Обработка второго числа
@bot.message_handler(func=lambda message: dbworker.get(
    dbworker.make_key(message.chat.id, config.CURRENT_STATE)) == config.States.STATE_COURSE.value)
def second_num(message):
    text = message.text

    cond = False
    try:
        a = float(text)
    except ValueError:
        cond = True
    if not cond and a <= 0:
        cond = True

    if cond:
        # Состояние не изменяется, выводится сообщение об ошибке
        bot.send_message(message.chat.id, 'Проверка на дурака :) Введите положительное число:')
    else:
        bot.send_message(message.chat.id, f'Вы ввели курс ({text})')
        # Меняем текущее состояние
        dbworker.set(dbworker.make_key(message.chat.id, config.CURRENT_STATE), config.States.STATE_CONV.value)
        # Сохраняем первое число
        dbworker.set(dbworker.make_key(message.chat.id, config.States.STATE_COURSE.value), text)
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Перевести')
        itembtn2 = types.KeyboardButton('Cтоимость электрогитары Gibson SG в рублях')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, 'Выберите, пожалуйста, действие', reply_markup=markup)

# Выбор действия
@bot.message_handler(func=lambda message: dbworker.get(
    dbworker.make_key(message.chat.id, config.CURRENT_STATE)) == config.States.STATE_CONV.value)
def operation(message):
    # Текущее действие
    op = message.text
    # Читаем операнды из базы данных
    val1 = dbworker.get(dbworker.make_key(message.chat.id, config.States.STATE_RUBLE.value))
    val2 = dbworker.get(dbworker.make_key(message.chat.id, config.States.STATE_COURSE.value))
    # Выполняем действие
    fv1 = float(val1)
    fv2 = float(val2)
    res = 0
    if op == 'Перевести':
        res = fv1*fv2
    elif op == 'Cтоимость электрогитары Gibson SG в рублях':
        res = 500.0/fv2
    # Выводим результат
    markup = types.ReplyKeyboardRemove(selective=False)
    if op == 'Перевести':
        bot.send_message(message.chat.id, f'{val1} р. = {res}$', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Гитара стоит примерно {int(res)} рублей', reply_markup=markup)
    # Меняем текущее состояние
    dbworker.set(dbworker.make_key(message.chat.id, config.CURRENT_STATE), config.States.STATE_RUBLE.value)
    # Выводим сообщение
    bot.send_message(message.chat.id, 'Введите рубли')


bot.polling()