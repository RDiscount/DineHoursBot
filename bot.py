import datetime

import telebot
from sqlalchemy import null
from telebot import types
import config
import psycopg2

bot = telebot.TeleBot(config.TOKEN)
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1234")


def subscriptionc_check(Name):
    cur = conn.cursor()
    cur.execute(f"SELECT subscription FROM customers WHERE customers.uid = '{Name.id}'")
    customer = cur.fetchall()
    cur.closed
    if customer:
        res = list(customer[0])
        return res[0]
    else:
        return False


def insert_user(Name):
    try:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO customers (uid, name, subscription) VALUES ('{Name.id}','{Name.first_name}',False)")
        conn.commit()
        cur.closed
    except psycopg2.DatabaseError as error:
        print(error)


def sub_date_end(Name):
    cur = conn.cursor()
    cur.execute(f"SELECT end_date_sub FROM customers WHERE customers.uid = '{Name.id}'")
    date = cur.fetchall()
    cur.closed
    if date:
        res = list(date[0])
        return res[0]
    else:
        return null


def count_sub_days(Name):
    date_sub = sub_date_end(Name)
    today = datetime.date.today()
    # d2 = datetime.strptime(today, "%Y.%m.%d")
    # d1 = datetime.strptime(date_sub, "%Y.%m.%d")
    res = (date_sub - today).days
    return res


def user_is_exist(Name):
    cur = conn.cursor()
    cur.execute(f"SELECT uid FROM customers WHERE customers.uid = '{Name.id}'")
    customer = cur.fetchall()
    cur.closed
    if customer:
        res = True
    else:
        res = False
    return res


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    print("Подписка " + str(subscriptionc_check(message.from_user)))
    if not user_is_exist(message.from_user):
        insert_user(message.from_user)
    else:
        if subscriptionc_check(message.from_user):
            # Keys----------------------------------------------------------
            markup_guide = types.InlineKeyboardMarkup(row_width=1)
            guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
            markup_guide.add(guide)

            markup_start_sub = types.ReplyKeyboardMarkup(row_width=4)
            channel = types.KeyboardButton("Выбрать ресторан")
            support = types.KeyboardButton("Поддержка")
            get_subscribe = types.KeyboardButton("Оформить Подписку")
            my_subscription = types.KeyboardButton("Моя подписка")
            cancel = types.KeyboardButton("Назад")
            to_main = types.KeyboardButton("На главную")
            change_rest = types.KeyboardButton("Поменять ресторан")
            markup_start_sub.add(support, to_main, channel, guide, my_subscription)
            # Keys----------------------------------------------------------

            bot.send_message(message.chat.id,
                             "Привет, {0.first_name}, это DineHours бот. Я даю возможность получить скидки от 10% в любимые рестораны "
                             "Москвы по подписке. Стоимость подписки: 249 рублей в месяц. Посмотрите гайд, "
                             "чтобы узнать, как это работает".format(
                                 message.from_user), parse_mode='html', reply_markup=markup_start_sub)
        else:
            # Keys----------------------------------------------------------
            markup_start_no_sub = types.ReplyKeyboardMarkup(row_width=4)
            channel = types.KeyboardButton("Выбрать ресторан")
            support = types.KeyboardButton("Поддержка")
            get_subscribe = types.KeyboardButton("Оформить Подписку")
            my_subscription = types.KeyboardButton("Моя подписка")
            cancel = types.KeyboardButton("Назад")
            to_main = types.KeyboardButton("На главную")
            guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
            markup_start_no_sub.add(support, to_main, channel, guide, get_subscribe)
            # Keys----------------------------------------------------------

            bot.send_message(message.chat.id,
                             "Привет, {0.first_name}, это DineHours бот. Я даю возможность получить скидки от 10% в любимые рестораны "
                             "Москвы по подписке. Стоимость подписки: 249 рублей в месяц. Посмотрите гайд, "
                             "чтобы узнать, как это работает".format(
                                 message.from_user), parse_mode='html', reply_markup=markup_start_no_sub)


@bot.message_handler(content_types='text')
def inp(message):
    # Keys----------------------------------------------------------
    markup_guide = types.InlineKeyboardMarkup(row_width=1)
    guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
    markup_guide.add(guide)

    markup_sub = types.InlineKeyboardMarkup(row_width=1)
    delete_sub = types.InlineKeyboardButton("Отменить", callback_data='delete_sub')
    extend = types.InlineKeyboardButton("Продлить", callback_data='extend')
    markup_sub.add(extend, delete_sub)

    markup_guide2 = types.InlineKeyboardMarkup(row_width=1)
    to_main = types.InlineKeyboardButton("На главную", callback_data='tomain')
    cancel = types.InlineKeyboardButton("Назад", callback_data='cancel')
    go = types.InlineKeyboardButton("Вперед", callback_data='go')
    markup_guide2.add(to_main, cancel, go)

    markup_start_no_sub = types.ReplyKeyboardMarkup(row_width=4)
    channel = types.KeyboardButton("Выбрать ресторан")
    support = types.KeyboardButton("Поддержка")
    get_subscribe = types.KeyboardButton("Оформить Подписку")
    my_subscription = types.KeyboardButton("Моя подписка")
    cancel = types.KeyboardButton("Назад")
    to_main = types.KeyboardButton("На главную")
    guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
    markup_start_no_sub.add(support, to_main, channel, guide, get_subscribe)

    markup_start_sub = types.ReplyKeyboardMarkup(row_width=4)
    channel = types.KeyboardButton("Выбрать ресторан")
    support = types.KeyboardButton("Поддержка")
    get_subscribe = types.KeyboardButton("Оформить Подписку")
    my_subscription = types.KeyboardButton("Моя подписка")
    cancel = types.KeyboardButton("Назад")
    to_main = types.KeyboardButton("На главную")
    change_rest = types.KeyboardButton("Поменять ресторан")
    markup_start_sub.add(support, to_main, channel, guide, my_subscription)
    # Keys----------------------------------------------------------

    if message.chat.type == 'private':
        if message.text == "Поддержка":
            bot.send_message(message.chat.id, "Перейдите в чат с поддердкой\n@DineHours_support")
        if message.text == "Выбрать ресторан":
            bot.send_message(message.chat.id, "Выберите ресторан, в который хотите пойти")
            bot.send_message(message.chat.id, "Cписок ресторанов\n"
                                              "<a href = 'https://t.me/DineHours/21'> Ресторан 1 </a>"
                                              "\n<a href = 'https://t.me/DineHours/25'> Ресторан 2 </a>"
                                              "\n<a href = 'https://t.me/DineHours/29'> Ресторан 3 </a>",
                             parse_mode='html')
        if message.text == "На главную":
            bot.send_message(message.chat.id,
                             "Привет, {0.first_name}, это DineHours бот. Я даю возможность получить скидки от 10% в любимые рестораны "
                             "Москвы по подписке. Стоимость подписки: 249 рублей в месяц. Посмотрите гайд, "
                             "чтобы узнать, как это работает".format(
                                 message.from_user), parse_mode='html', reply_markup=markup_guide)
        if message.text == "Гайд":
            bot.send_message(message.chat.id, "1 экран: Нажмите на кнопку «Оформить подписку». Оплати ее с помощью "
                                              "банковской картой прямо внутри бота 2 экран: Выберите среди "
                                              "ресторанов-партнеров тот, в который хотите пойти. Также Вы можете "
                                              "прочитать в нашем телеграм-канале @DineHours, когда предоставляется "
                                              "скидка и другую информацию о ресторане. Для этого просто нажмите на "
                                              "название ресторана в сообщении. 3 экран: Теперь Вы получили  "
                                              "web-ссылку на карточку, которую необходимо будет показать официанту в "
                                              "ресторане. Приятного аппетита!  Важно: у некоторых ресторанах есть "
                                              "особые условия предоставления скидки: необходимо забронировать стол "
                                              "или заранее сообщить ресторану, что Вы придете с нашей картой. Об этой "
                                              "информации пишется в телеграм-канале @DineHours 4 экран: Всю "
                                              "информацию о подписке: стоимость, срок окончания, продление и отмена "
                                              "можно увидеть по кнопке «Моя подписка»", reply_markup=markup_guide2)
        if message.text == "Моя подписка":
            if subscriptionc_check(message.from_user):
                bot.send_message(message.chat.id,
                                 f"Информация о подписке\nСтоимость: 250 рублей\nСрок окончания: {sub_date_end(message.from_user)} (осталось {count_sub_days(message.from_user)} дней)",
                                 reply_markup=markup_sub)
            else:
                bot.send_message(message.chat.id,
                                 "Ваша подписка закончилась(",
                                 reply_markup=markup_start_no_sub)
        if message.text == "Оформить Подписку":
            if subscriptionc_check(message.from_user):
                bot.send_message(message.chat.id, "У вас уже есть подписка", reply_markup=markup_start_sub)
            else:
                bot.send_message(message.chat.id,
                                 "У вас нет подписки",
                                 reply_markup=markup_start_no_sub)
                bot.send_message(message.chat.id, "Эквайринг")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Keys----------------------------------------------------------
    markup_guide2 = types.InlineKeyboardMarkup(row_width=1)
    to_main = types.InlineKeyboardButton("На главную", callback_data='tomain')
    cancel = types.InlineKeyboardButton("Назад", callback_data='cancel')
    go = types.InlineKeyboardButton("Вперед", callback_data='go')
    markup_guide2.add(to_main, cancel, go)

    markup_guide = types.InlineKeyboardMarkup(row_width=1)
    guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
    markup_guide.add(guide)
    # Keys----------------------------------------------------------
    try:
        if call.message:
            if call.data == 'guide':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="1 экран: Нажмите на кнопку «Оформить подписку». Оплати ее с помощью "
                                           "банковской картой прямо внутри бота 2 экран: Выберите среди "
                                           "ресторанов-партнеров тот, в который хотите пойти. Также Вы можете "
                                           "прочитать в нашем телеграм-канале @DineHours, когда предоставляется "
                                           "скидка и другую информацию о ресторане. Для этого просто нажмите на "
                                           "название ресторана в сообщении. 3 экран: Теперь Вы получили  "
                                           "web-ссылку на карточку, которую необходимо будет показать официанту в "
                                           "ресторане. Приятного аппетита!  Важно: у некоторых ресторанах есть "
                                           "особые условия предоставления скидки: необходимо забронировать стол "
                                           "или заранее сообщить ресторану, что Вы придете с нашей картой. Об этой "
                                           "информации пишется в телеграм-канале @DineHours 4 экран: Всю "
                                           "информацию о подписке: стоимость, срок окончания, продление и отмена "
                                           "можно увидеть по кнопке «Моя подписка»", reply_markup=markup_guide2)
            if call.data == 'tomain':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Привет, {0.first_name}, это DineHours бот. Я даю возможность получить "
                                           "скидки от 10% в любимые рестораны "
                                           "Москвы по подписке. Стоимость подписки: 249 рублей в месяц. Посмотрите "
                                           "гайд, "
                                           "чтобы узнать, как это работает".format(
                                          call.from_user, bot.get_me()),
                                      parse_mode='html', reply_markup=markup_guide)
            if call.data == 'cancel':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="text1".format(
                                          call.from_user, bot.get_me()), parse_mode='html', reply_markup=markup_guide2)
            if call.data == 'go':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="text2".format(
                                          call.from_user, bot.get_me()), parse_mode='html', reply_markup=markup_guide2)
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
