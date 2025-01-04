import logging

import telebot
from telebot import types
from telebot.types import PreCheckoutQuery
import tracemalloc

from config import TOKEN
import webbrowser
from database import *
from payments.donation import send_donation, bot_send_invoice_donation
from payments.programmingCourse import *
from payments.designerCourse import *

bot = telebot.TeleBot(TOKEN)

name_operation_sale = ""

tracemalloc.start()

init_db()

@bot.message_handler(commands=['start'])
def send_command_start(message):

    add_user(message.from_user.id, message.from_user.first_name, message.from_user.last_name)

    username = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Программист!", callback_data="programmer_me"))
    markup.add(types.InlineKeyboardButton("Дизайнер...", callback_data="designer_me"))
    markup.add(types.InlineKeyboardButton("Офисный жополиз", callback_data="office_ass_me"))
    markup.add(types.InlineKeyboardButton("Работяга", callback_data="worker_me"))
    pretty_boy_btn = types.InlineKeyboardButton("Красавчик", callback_data="pretty_boy_me")
    good_man_btn = types.InlineKeyboardButton("Хороший человек", callback_data="good_man_me")
    markup.row(pretty_boy_btn, good_man_btn)
    bot.reply_to(message, f"Ты еще не устал нажимать на эти кнопки...?\nЛадно...\n{username}, ты кто по жизни?", reply_markup=markup)

@bot.message_handler(commands=['paysupport'])
def handle_pay_support(message):
    bot.send_message(
        message.chat.id,
        "Денег не возвращаем.\nМатериться можно тут: @Olezhka_TG. 😭😂"
    )

@bot.message_handler(commands=['help'])
def send_command_help(message):
    bot.reply_to(message, 'Напиши "Привет"')

@bot.message_handler(commands=['site', 'web'])
def send_command_site(message):
    webbrowser.open("https://music.yandex.ru/home")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    username = message.from_user.first_name
    if message.text == "Привет" or message.text == "/hi":
        bot.send_message(message.from_user.id, f"Привет, {username}\nДавай начнем работу!")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=['audio'])
def get_audio_messages(message):
    username = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Слушать музыку", url="https://music.yandex.ru/home"))
    bot.send_message(message.from_user.id, f"{username}, я еще не научился слушать аудио ;(", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def get_photo_messages(message):
    username = message.from_user.first_name
    bot.send_message(message.from_user.id, f"{username}, классная фотография!\nЖаль я еще не научился оценивать фото ;(")

@bot.callback_query_handler(func=lambda call: call.data == "donation_1")
def handle_buy_donation(call):
    global name_operation_sale
    name_operation_sale = "donation"

    amount = 1
    bot_send_invoice_donation(call, amount)
@bot.callback_query_handler(func=lambda call: call.data == "donation_2")
def handle_buy_donation(call):
    global name_operation_sale
    name_operation_sale = "donation"

    amount = 10
    bot_send_invoice_donation(call, amount)
@bot.callback_query_handler(func=lambda call: call.data == "donation_3")
def handle_buy_donation(call):
    global name_operation_sale
    name_operation_sale = "donation"

    amount = 100
    bot_send_invoice_donation(call, amount)
@bot.callback_query_handler(func=lambda call: call.data == "donation_4")
def handle_buy_donation(call):
    global name_operation_sale
    name_operation_sale = "donation"

    amount = 1000
    bot_send_invoice_donation(call, amount)


@bot.callback_query_handler(func=lambda call: call.data == "send_by_programing_course")
def handle_buy_programming_course(call):
    send_by_programming_course(call)
@bot.callback_query_handler(func=lambda call: call.data == "buy_programming_course")
def handle_buy_programming_course(call):
    global name_operation_sale
    name_operation_sale = "programingCourse"

    amount = 1000
    bot_send_invoice_buy_programming_course(call, amount)

@bot.callback_query_handler(func=lambda call: call.data == "send_by_designer_course")
def handle_buy_designer_course(call):
    send_by_designer_course(call)
@bot.callback_query_handler(func=lambda call: call.data == "buy_designer_course")
def handle_buy_designer_course(call):
    global name_operation_sale
    name_operation_sale = "designerCourse"

    amount = 2500
    bot_send_invoice_buy_designer_course(call, amount)

@bot.callback_query_handler(func=lambda call: call.data == "my_courses")
def my_course_callback(call):
    markup = types.InlineKeyboardMarkup()
    bot.delete_message(call.message.chat.id, call.message.message_id)
    courses_list = get_all_courses_by_user_id(call.message.chat.id)
    if courses_list.__len__() != 0:
        for i in courses_list:
            markup.add(types.InlineKeyboardButton(f"{i[2]}", "https://sun9-80.userapi.com/8zqyhREWsi1TzpRPrJpYMJaqFU4LyXWHqBje_Q/eZnYICLEW_U.jpg"))
        bot.send_message(call.message.chat.id,"Красавчик! Вижу, что деньги и стремления имеются.\nВот, твои курсы: ", reply_markup=markup)
    else: bot.send_message(call.message.chat.id, "У тебя нет купленых курсов.\nНищеброд!")


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    username = callback.message.chat.first_name
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if callback.data == "programmer_me": send_btn_programmer_me(callback)
    elif callback.data == "designer_me": send_btn_designer_me(callback)
    elif callback.data == "office_ass_me":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Инструкция", url="https://life.ru/p/1640928?ysclid=m570z51f6e464129509"))
        bot.send_message(callback.message.chat.id, f"{username}...\nИ как на вкус?\nЕсли еще не начал, то вот инструкция.\nНо знай, ты упал в моих глазах.", reply_markup=markup)
    elif callback.data == "worker_me":
        file_image = open('image/worker_girl.jpg', 'rb')
        file_audio_dora = open('audio/dora_Loverboy.mp3', 'rb')
        file_audio_neksyusha = open('audio/neksyusha_Zavodskaya.mp3', 'rb')
        bot.send_photo(callback.message.chat.id, file_image)
        bot.send_message(callback.message.chat.id, f"{username}, что ты тут делаешь?\nХочу сказать, что ты красавчик!\nНи какие инструкции тебе не нужны.\nПослушай эти треки и радуйся жизни.")
        bot.send_audio(callback.message.chat.id, file_audio_dora)
        bot.send_audio(callback.message.chat.id, file_audio_neksyusha)
    elif callback.data == "good_man_me": send_good_man_me(callback)
    elif callback.data == "pretty_boy_me": send_pretty_boy_me(callback)
    elif callback.data == "all_users_list": all_users_view(callback)
    elif callback.data == "delete_me": delete_user(callback.message.chat.id)
    else: bot.send_message(callback.message.chat.id, f"Дурной?\nФункция еще не сделана. Отдыхай!")

def send_btn_programmer_me(callback):
    username = callback.message.chat.first_name
    markup = types.InlineKeyboardMarkup()
    c_plus_btn = types.InlineKeyboardButton("С++", "https://metanit.com/cpp/tutorial/?ysclid=m56xkq8ebe923014352")
    c_sharp_btn = types.InlineKeyboardButton("С#", "https://metanit.com/sharp/tutorial/?ysclid=m56xlhy3ln754950314")
    java_btn = types.InlineKeyboardButton("Java", "https://metanit.com/java/tutorial/1.1.php?ysclid=m56xm80fmg22768205")
    python_btn = types.InlineKeyboardButton("Python", "https://metanit.com/python/tutorial/1.1.php?ysclid=m56xq31e9e466155012")
    markup.row(python_btn, c_plus_btn)
    markup.row(java_btn, c_sharp_btn)
    if purchase_verification_by_user_id_and_title(callback.message.chat.id, "programingCourse").__len__() == 0:
        markup.add(types.InlineKeyboardButton("Платный курс", callback_data="send_by_programing_course"))
    bot.send_message(callback.message.chat.id, f"{username}, ты еще здесь?\nНу... Выбирай язык и проходи обучение.\nДенег видетели у него нет... Вот, бесплатно!", reply_markup=markup)

def send_btn_designer_me(callback):
    username = callback.message.chat.first_name
    markup = types.InlineKeyboardMarkup()
    web_btn = types.InlineKeyboardButton("Web-Дизайнер", "https://habr.com/ru/companies/lanit/articles/713708/")
    graphic_btn = types.InlineKeyboardButton("Графический дизайнер", "https://practicum.yandex.ru/blog/graphic-designer/")
    brand_btn = types.InlineKeyboardButton("Брэнд-дизайнер", "https://media.contented.ru/znaniya/professions/kto-takoj-brend-dizajner/?ysclid=m570bed9c0949571042")
    ui_ux_btn = types.InlineKeyboardButton("UI/UX Дизайнер", "https://www.uprock.ru/courses")
    markup.row(graphic_btn, web_btn)
    markup.row(ui_ux_btn, brand_btn)
    if purchase_verification_by_user_id_and_title(callback.message.chat.id, "designerCourse").__len__() == 0:
        markup.add(types.InlineKeyboardButton("Платный курс", callback_data="send_by_designer_course"))
    bot.send_message(callback.message.chat.id, f"{username}, реально?\nОкей. Бесплатных куросов почти нет, прости ;(.\nЛучше попробовать и не сделать, чем даже не начать!", reply_markup=markup)

def send_pretty_boy_me(callback):
    send_donation(callback)


def send_good_man_me(callback):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Список пользователей", callback_data="all_users_list"))
    markup.add(types.InlineKeyboardButton("Мои курсы", callback_data="my_courses"))
    bot.send_message(callback.message.chat.id, f"Доброго времени суток, мой хозяин.\nТы думал, я так скажу? Создал меня... Иди дворами!\nДа-да-да, это Питерский слэнг.\nЧто тебе надо? Выбирай и проваливай!", reply_markup=markup)

def all_users_view(callback):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Удалить себя", callback_data="delete_me"))

    message_all_users = ""
    for i in get_all_users():
        message_all_users += f"{i[0]} {i[1]} {i[2]} {i[3]}\n"
    bot.send_message(callback.message.chat.id, f"Всего пользователей: {get_all_users().__len__()}.\nСписок всех пользователей:\n{message_all_users}", reply_markup=markup)

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # всегда отвечаем утвердительно
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    user_id = message.from_user.id
    payment_id = message.successful_payment.provider_payment_charge_id
    amount = message.successful_payment.total_amount
    currency = message.successful_payment.currency

    bot.send_message(message.chat.id, "✅ Оплата принята!")

    global name_operation_sale
    if name_operation_sale == "programingCourse":
        insert_course(user_id,"Курс по программированию", payment_id)
    elif name_operation_sale == "designerCourse":
        insert_course(user_id,"Курс по дизайну", payment_id)

    save_payment(user_id, payment_id, amount, currency)

bot.polling(none_stop=True, interval=0)