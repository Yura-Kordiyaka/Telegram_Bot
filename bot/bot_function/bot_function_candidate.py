from db.utilits import *
from db.schemas_models import *
from db.validation import validate_email
from telebot import types
from .bot_print_message import *


def candidate_handler(bot):
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # but1 = types.KeyboardButton("Створити резюме")
    # but2 = types.KeyboardButton("я вже маю резюме")
    # markup.add(but1, but2)
    #
    keyboard = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(text="do you want to  create a resume?", callback_data="create_resume")
    button2 = types.InlineKeyboardButton(text="do you have a resume?", callback_data="have_resume")
    keyboard.add(button1, button2)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "Hello",
                         reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        chat_id = call.message.chat.id

        if call.data == "create_resume":
            if get_candidate_resume(chat_id):
                bot.send_message(chat_id, f'you already have  a resume ,select another button')
            else:
                create_candidate(call.message)
        elif call.data == "have_resume":
            if get_candidate_resume(chat_id):
                show_candidate_resume(call.message)
            else:
                bot.send_message(chat_id, f'you haven\'t had a resume yet,select another button')

    def create_candidate(message):
        try:
            chat_id = message.chat.id
            bot.send_message(chat_id, "Hi! Please enter your first name.")
            bot.register_next_step_handler(message, input_info, candidate_info={})
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

    def input_info(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['first_name'] = message.text

            msg = bot.send_message(chat_id, f"Thank you, {candidate_info['first_name']}! Now, enter your last name.")
            bot.register_next_step_handler(msg, input_info_last_name, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

    def input_info_last_name(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['last_name'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Thanks, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your email.")
            bot.register_next_step_handler(msg, input_info_email, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

    def input_info_email(message, candidate_info):
        try:
            chat_id = message.chat.id
            if validate_email(message.text):
                candidate_info['email'] = message.text

                msg = bot.send_message(chat_id,
                                       f"Thank you, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your desired salary.")
                bot.register_next_step_handler(msg, input_info_salary, candidate_info)
            else:
                msg = bot.send_message(chat_id,
                                       f"Input valid email, please try again")
                bot.register_next_step_handler(msg, input_info_email, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

    def input_info_salary(message, candidate_info):
        chat_id = message.chat.id
        try:
            candidate_info['salary'] = int(message.text)
            if candidate_info['salary'] > 0:
                msg = bot.send_message(chat_id,
                                       f"Thank you, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your experience.")
                bot.register_next_step_handler(msg, input_info_experience, candidate_info)
            else:
                msg = bot.send_message(chat_id,
                                       f"Input valid salary,salary must be grater then 0, please try again")
                bot.register_next_step_handler(msg, input_info_salary, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

    def input_info_experience(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['experience'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Thank you, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your skills.")
            bot.register_next_step_handler(msg, input_info_skills, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

    def input_info_skills(message, candidate_info):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'done':
                save_data(message, candidate_info)
            else:
                if 'skills' not in candidate_info:
                    candidate_info['skills'] = []

                candidate_info['skills'].append({'skill_name': message.text})

                msg = bot.send_message(chat_id,
                                       "Enter another skill, or type 'done' if you've finished entering your skills.")
                bot.register_next_step_handler(msg, input_info_skills, candidate_info)
        except Exception as e:
            bot.reply_to(message, 'Error. Please try again.')

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
            skills_to_add = [SkillsCreate(name=skill_dict.get('skill_name', '')) for skill_dict in user_skills]
            candidate = add_candidate(new_candidate, skills_to_add)

            bot.send_message(chat_id,print_resume(candidate_info))

            candidate_resume_data = CandidateResumeCreate(
                candidate_id=candidate.id,
                chat_id=chat_id
            )
            add_candidate_resume(candidate_resume_data)
        except Exception as e:
            bot.reply_to(message, f'Error. Please try again {e}')

    def show_candidate_resume(message):
        chat_id = message.chat.id
        candidate_resume = get_candidate_resume(chat_id)
        try:

            bot.send_message(chat_id,
                             f'{print_resume(candidate_resume)}')
            # bot.send_message(chat_id, f'{candidate_resume}')
        except Exception as e:
            bot.reply_to(message, f'Error. Please try again {e}')
