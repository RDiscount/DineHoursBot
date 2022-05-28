import telebot
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


            bot.send_message(message.chat.id,
                             "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, созданный командой "
                             "DineHours.".format(
                                 message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup_start_sub)
        else:
            markup_start_no_sub = types.ReplyKeyboardMarkup(row_width=4)
            channel = types.KeyboardButton("Выбрать ресторан")
            support = types.KeyboardButton("Поддержка")
            get_subscribe = types.KeyboardButton("Оформить Подписку")
            my_subscription = types.KeyboardButton("Моя подписка")
            cancel = types.KeyboardButton("Назад")
            to_main = types.KeyboardButton("На главную")
            guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
            markup_start_no_sub.add(support, to_main, channel, guide, get_subscribe)

            bot.send_message(message.chat.id,
                             "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, созданный командой "
                             "DineHours.".format(
                                 message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup_start_no_sub)


@bot.message_handler(content_types='text')
def inp(message):
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

    if message.chat.type == 'private':
        if message.text == "Поддержка":
            bot.send_message(message.chat.id, "Перейдите в чат с поддердкой\n <a href=''>Чат Поддержка</a>")
        if message.text == "Выбрать ресторан":
            bot.send_message(message.chat.id, "Выберите ресторан, в который хотите пойти")
            bot.send_message(message.chat.id, "Cписок ресторанов\n"
                                              "<a href = 'https://t.me/DineHours/21'> Ресторан 1 </a>"
                                              "\n<a href = 'https://t.me/DineHours/25'> Ресторан 2 </a>"
                                              "\n<a href = 'https://t.me/DineHours/29'> Ресторан 3 </a>",
                             parse_mode='html')
        if message.text == "На главную":
            bot.send_message(message.chat.id,
                             "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, созданный командой "
                             "DineHours.".format(
                                 message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup_guide)
        if message.text == "Гайд":
            bot.send_message(message.chat.id, "тут будет текст гайда", reply_markup=markup_guide2)
        if message.text == "Моя подписка":
            bot.send_message(message.chat.id, "Информация о подписке", reply_markup=markup_sub)
        if message.text == "Оформить Подписку":
            bot.send_message(message.chat.id, "Эквайринг")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    markup_guide2 = types.InlineKeyboardMarkup(row_width=1)
    to_main = types.InlineKeyboardButton("На главную", callback_data='tomain')
    cancel = types.InlineKeyboardButton("Назад", callback_data='cancel')
    go = types.InlineKeyboardButton("Вперед", callback_data='go')
    markup_guide2.add(to_main, cancel, go)

    markup_guide = types.InlineKeyboardMarkup(row_width=1)
    guide = types.InlineKeyboardButton("Гайд", callback_data='guide')
    markup_guide.add(guide)
    try:
        if call.message:
            if call.data == 'guide':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="тут будет текст гайда", reply_markup=markup_guide2)
            if call.data == 'tomain':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, созданный командой "
                                           "DineHours.".format(
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
