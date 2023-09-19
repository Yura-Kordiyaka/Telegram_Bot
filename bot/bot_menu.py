
import telebot
from telebot import types

def menu_handler(bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Button1")
    but2 = types.KeyboardButton("Button2")
    markup.add(but1, but2)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "{0.first_name}, Welcome!".format(message.from_user), parse_mode='html',
                     reply_markup=markup)

    # @bot.message_handler(func=lambda message: message.text == "Button1")
    # def handle_button1(message):
    #     try:
    #         create_candidate
    #     except Exception as e:
    #         bot.send_message(message.chat.id, f"{e}")
    #
    #     # bot.send_message(message.chat.id, "Привіт! Введи своє ім'я.")
