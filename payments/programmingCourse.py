import logging

import telebot
import json
from telebot import types
from telebot.asyncio_filters import StateFilter
from telebot.types import PreCheckoutQuery

from config import TOKEN, TEST_PROVIDER_TOKEN, CURRENCY
from database import save_payment


bot = telebot.TeleBot(TOKEN)

def send_by_programming_course(callback):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Оплатить", callback_data="buy_programming_course"))
    bot.send_message(callback.message.chat.id, "Ого, какие люди! В Голливуде. А ты, что здесь забыл?\nНу ладно, раз зашел, значит есть деньги.\nТут драгоценные знания всех веков, оплати и пользуйся.", reply_markup=markup)

def bot_send_invoice_buy_programming_course(call, amount):
    prices = [types.LabeledPrice(label=CURRENCY, amount=amount*100)]
    provider_data = {
        "receipt": {
            "items": [
                {
                    "description": "Курс по программированию",
                    "quantity": "1.00",
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency": CURRENCY
                    },
                    "vat_code": 1
                }
            ]
        }
    }
    provider_data = json.dumps(provider_data)

    bot.send_invoice(
        call.message.chat.id,
        title="Курс по программированию",
        description="Курс по программированию на всех языках мира. Покупай, не пожалеешь!",
        invoice_payload="programming_course_purchase_payload",
        provider_token=TEST_PROVIDER_TOKEN,
        currency=CURRENCY,
        prices=prices,
        reply_markup=payment_keyboard(amount),
        need_phone_number = True,
        send_phone_number_to_provider = True,
        provider_data = provider_data
    )


def payment_keyboard(amount):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"Оплатить {amount} RUB" , pay=True))
    return markup