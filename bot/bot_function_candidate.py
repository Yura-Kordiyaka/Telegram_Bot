from utilits import *
from schemas_models import *
from telebot import types
import telebot


def candidate_handler(bot):
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

    @bot.message_handler(commands=["start"])
    def start_message(message):
        d=get_all_candidates_with_skills()
        try:
            bot.send_message(message.chat.id, f"{d}")
        except Exception as e:
            bot.reply_to(message, f'{e}')

    @bot.message_handler(commands=['create_candidate'])
    def create_candidate(message):
        try:
            chat_id = message.chat.id
            bot.send_message(chat_id, "Привіт! Введи своє ім'я.")
            bot.register_next_step_handler(message, input_info, candidate_info={})
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')


    def input_info(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['first_name'] = message.text

            msg = bot.send_message(chat_id, f"Дякую, {candidate_info['first_name']}! Тепер введи своє прізвище")
            bot.register_next_step_handler(msg, input_info_last_name, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_last_name(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['last_name'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Дякую, {candidate_info['first_name']} {candidate_info['last_name']}! Тепер введіть свою пошту")
            bot.register_next_step_handler(msg, input_info_email, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_email(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['email'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Дякую, {candidate_info['first_name']} {candidate_info['last_name']}! Тепер введіть бажану зарплату")
            bot.register_next_step_handler(msg, input_info_salary, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_salary(message, candidate_info):
        chat_id = message.chat.id
        try:

            candidate_info['salary'] = int(message.text)

            msg = bot.send_message(chat_id,
                                   f"Дякую, {candidate_info['first_name']} {candidate_info['last_name']}! Тепер введіть свій досвід")
            bot.register_next_step_handler(msg, input_info_experience, candidate_info)
        except ValueError as ve:
            bot.send_message(chat_id, 'Помилка: зарплата повинна бути більша від 0')
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_experience(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['experience'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Дякую, {candidate_info['first_name']} {candidate_info['last_name']}! Тепер введіть свої навички")
            bot.register_next_step_handler(msg, input_info_skills, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_skills(message, candidate_info):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'готово':
                save_data(message, candidate_info)
            else:
                if 'skills' not in candidate_info:
                    candidate_info['skills'] = []

                candidate_info['skills'].append(message.text)

                msg = bot.send_message(chat_id,"Напиши ще одну навичку, або напиши 'готово', якщо завершив введення своїх навичок.")
                bot.register_next_step_handler(msg, input_info_skills, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def save_data(message, candidate_info):
        try:

            first_name = candidate_info['first_name']
            last_name = candidate_info['last_name']
            email = candidate_info['email']
            salary = candidate_info['salary']
            experience = candidate_info['experience']
            user_skills = candidate_info.get('skills', [])

            chat_id = message.chat.id
            new_candidate = CandidatesCreate(
                email=email,
                first_name=first_name,
                last_name=last_name,
                experience=experience,
                desired_salary=salary
            )
            all_skills_user = "\n"
            for i in user_skills:
                all_skills_user += '\t\t' + i + '\n'
            skills_to_add = [SkillsCreate(name=i) for i in user_skills]
            add_candidate(new_candidate, skills_to_add)
            bot.send_message(chat_id, f"Дякую, {first_name} {last_name}!\n"
                                      f"ваш досвід роботи : {experience}\n"
                                      f"зарплата яку ви бажаєте : {salary}\n"
                                      f"ваша пошта : {email}\n"
                                      f"Ваші навички : {all_skills_user}")
        except ValueError as ve:
            bot.send_message(message.chat.id, f'Помилка: зарплата повинна бути більша від 0')
        except Exception as e:
            bot.reply_to(message, f'Помилка. Спробуйте ще раз {e}')
