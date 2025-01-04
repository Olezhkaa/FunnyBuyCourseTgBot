import telebot
from telebot import types
from config import TOKEN
from database import save_payment


bot = telebot.TeleBot(TOKEN)

def send_donation(callback):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Пожертвовать 1 ⭐", callback_data="donation_1"))
    markup.add(types.InlineKeyboardButton("Пожертвовать 10 ⭐", callback_data="donation_2"))
    markup.add(types.InlineKeyboardButton("Пожертвовать 100 ⭐", callback_data="donation_3"))
    markup.add(types.InlineKeyboardButton("Пожертвовать 1000 ⭐", callback_data="donation_4"))

    bot.send_message(callback.message.chat.id,
                     f"О, Привет!\n{callback.message.chat.first_name}, у тебя появились деньги? Поздравляю.\nПользуешься ботом? Можешь не отвечать :)\nЖертвуй своей почкой.",
                     reply_markup=markup)



def bot_send_invoice_donation(call, amount):
    prices = [types.LabeledPrice(label="XTR", amount=amount)]
    bot.send_invoice(
        call.message.chat.id,
        title="Пожертвование",
        description="Пожертвуйте разработчкику на кофе ☕🥺",
        invoice_payload="donation_purchase_payload",
        provider_token="",  # For XTR, this token can be empty
        currency="XTR",
        prices=prices,
        reply_markup=payment_keyboard(amount)
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    user_id = message.from_user.id
    payment_id = message.successful_payment.provider_payment_charge_id
    amount = message.successful_payment.total_amount
    currency = message.successful_payment.currency

    bot.send_message(message.chat.id, "✅ Оплата принята\nСпасибо тебе, за пожертвования, я очень благодарен\nХа-ха-ха, думал я так скажу? Я конечно благодарен, но иди дворами, дважды! 😈")

    save_payment(user_id, payment_id, amount, currency)

def payment_keyboard(amount):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"Преподнести {amount} XTR" , pay=True))
    return markup