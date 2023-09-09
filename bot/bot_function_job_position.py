from utilits import *
from schemas_models import *
from telebot import types
import telebot


def vacancy_handler(bot):
    # @bot.message_handler(commands=['start'])
    # def handle_start(message):
    #     # Створюємо клавіатуру з кнопкою "Почати"
    #     markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     item = telebot.types.KeyboardButton("Почати")
    #     markup.add(item)
    #
    #     # Відправляємо повідомлення з клавіатурою кнопок
    #     bot.send_message(message.chat.id, "Вітаємо! Натисніть кнопку 'Почати', щоб розпочати використання бота.",
    #                      reply_markup=markup)
    #
    # @bot.message_handler(func=lambda message: True)
    # def echo_all(message):
    #     # Обробляємо всі інші повідомлення
    #     bot.reply_to(message, message.text)

    @bot.message_handler(commands=['create_vacancy'])
    def create_candidate(message):
        try:
            chat_id = message.chat.id
            bot.send_message(chat_id, "Привіт! Введи сюда назву вакансії.")
            bot.register_next_step_handler(message, input_info, vacancy_info={})
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info(message, vacancy_info):
        try:
            chat_id = message.chat.id
            vacancy_info['title'] = message.text
            msg = bot.send_message(chat_id, f"Дякую,тепер опишіть будьласка більш детально що це за вакансія")
            bot.register_next_step_handler(msg, input_info_description, vacancy_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_description(message, vacancy_info):
        try:
            chat_id = message.chat.id
            vacancy_info['description'] = message.text

            msg = bot.send_message(chat_id, f"Дякую,тепер введіть навички які потрібні для цієї роботи по одній будь ласка")
            bot.register_next_step_handler(msg, input_info_requirements, vacancy_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_requirements(message, vacancy_info):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'готово':
                save_data(message, vacancy_info)
            else:
                if 'requirements' not in vacancy_info:
                    vacancy_info['requirements'] = []

                vacancy_info['requirements'].append(message.text)

                msg = bot.send_message(chat_id,
                                       "Напиши ще одну навичку, або напишить 'готово', якщо завершили введення навичок які потрібні для цієї роботи")
                bot.register_next_step_handler(msg, input_info_requirements, vacancy_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def save_data(message, vacancy_info):
        try:

            # first_name = candidate_info['first_name']
            # last_name = candidate_info['last_name']
            # email = candidate_info['email']
            # salary = candidate_info['salary']
            # experience = candidate_info['experience']
            # user_skills = candidate_info.get('skills', [])
            #
            chat_id = message.chat.id
            # new_candidate = CandidatesCreate(
            #     email=email,
            #     first_name=first_name,
            #     last_name=last_name,
            #     experience=experience,
            #     desired_salary=salary
            # )
            # all_skills_user = "\n"
            # for i in user_skills:
            #     all_skills_user += '\t\t' + i + '\n'
            # skills_to_add = [SkillsCreate(name=i) for i in user_skills]
            # add_candidate(new_candidate, skills_to_add)
            bot.send_message(chat_id, f"{vacancy_info}")
        except ValueError as ve:
            bot.send_message(message.chat.id, f'Помилка: зарплата повинна бути більша від 0')
        except Exception as e:
            bot.reply_to(message, f'Помилка. Спробуйте ще раз {e}')
