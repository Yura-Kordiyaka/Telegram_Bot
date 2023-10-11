from telebot import types


from db.utilits_candidate import *
from db.validation import validate_email

from .bot_print_message import *


def candidate_handler(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        keyboard = types.InlineKeyboardMarkup()
        candidate = types.InlineKeyboardButton(text="👤 candidate", callback_data="candidate")
        employer = types.InlineKeyboardButton(text="👔 recruiter", callback_data="recruiter")
        keyboard.row(candidate)
        keyboard.row(employer)
        bot.send_message(message.chat.id, "Hello 👋, choose who you are, a candidate 👤 or a recruiter 👔",
                         reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data == "candidate")
    def handle_candidate(call):
        chat_id = call.message.chat.id

        keyboard = types.InlineKeyboardMarkup()
        create_resume = types.InlineKeyboardButton(text="do you want to  create a resume? ✨",
                                                   callback_data="create_resume")
        have_resume = types.InlineKeyboardButton(text="do you have a resume? 🗒", callback_data="have_resume")
        keyboard.row(create_resume)
        keyboard.row(have_resume)
        bot.send_message(chat_id, "Hello", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data == 'create_resume')
    def handle_create_resume(call):
        chat_id = call.message.chat.id
        if get_candidate_resume(chat_id):
            bot.send_message(chat_id, f'you already have  a resume ,select another button')
        else:
            create_candidate(call.message)

    @bot.callback_query_handler(func=lambda call: call.data == 'have_resume')
    def handle_have_resume(call):
        chat_id = call.message.chat.id
        if get_candidate_resume(chat_id):
            show_candidate_resume(call.message)
        else:
            bot.send_message(chat_id, f'❗❗❗you haven\'t had a resume yet,select another button❗❗❗')

    def create_candidate(message):
        try:
            chat_id = message.chat.id
            bot.send_message(chat_id, "Hi! Please, enter the desired position 🎯🎯🎯")
            bot.register_next_step_handler(message, input_info_job_position, candidate_info={})
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_job_position(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['desired_job_position'] = message.text
            msg = bot.send_message(chat_id, f"Thank you,😊now enter your first name")
            bot.register_next_step_handler(msg, input_info, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['first_name'] = message.text

            msg = bot.send_message(chat_id, f"Thank you 😊, {candidate_info['first_name']}! Now, enter your last name.")
            bot.register_next_step_handler(msg, input_info_last_name, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_last_name(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['last_name'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Thank you 😊, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your email 📧")
            bot.register_next_step_handler(msg, input_info_email, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_email(message, candidate_info):
        try:
            chat_id = message.chat.id
            if validate_email(message.text):
                candidate_info['email'] = message.text

                msg = bot.send_message(chat_id,
                                       f"Thank you 😊, {candidate_info['first_name']} {candidate_info['last_name']}! Now,"
                                       f" enter "
                                       f"your main skill 💡💡💡 like Python🐍 or JS💻")
                bot.register_next_step_handler(msg, input_main_skill, candidate_info)
            else:
                msg = bot.send_message(chat_id,
                                       f"❗❗❗Input valid email, please try again")
                bot.register_next_step_handler(msg, input_info_email, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_main_skill(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['main_skill'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Thank you 😊, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your desired salary 💸💸💸")
            bot.register_next_step_handler(msg, input_info_salary, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_salary(message, candidate_info):
        chat_id = message.chat.id
        try:
            if message.text.isdigit():
                candidate_info['salary'] = int(message.text)
                if candidate_info['salary'] > 0:
                    msg = bot.send_message(chat_id,
                                           f"Thank you 😊, {candidate_info['first_name']} {candidate_info['last_name']}! Now enter your work experience in years and month format 🗓, if you haven't already, just write 0 years ")
                    bot.register_next_step_handler(msg, input_info_experience, candidate_info)
                else:
                    msg = bot.send_message(chat_id,
                                           f"❗❗❗Input valid salary,salary must be grater then 0, please try again")
                    bot.register_next_step_handler(msg, input_info_salary, candidate_info)
            else:
                msg = bot.send_message(chat_id,
                                       f"❗❗❗Input valid salary,salary must contain only digit 🔢")
                bot.register_next_step_handler(msg, input_info_salary, candidate_info)

        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_experience(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['experience'] = message.text

            msg = bot.send_message(chat_id,
                                   f"Thank you 😊, {candidate_info['first_name']} {candidate_info['last_name']}! Now, enter your skills 🛠 like SQL 📊 or C++ 🌐")
            bot.register_next_step_handler(msg, input_info_skills, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_skills(message, candidate_info):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'done':
                save_data(message, candidate_info)
            else:
                if 'skills' not in candidate_info:
                    candidate_info['skills'] = []
                if any(skill['skill_name'].lower() == message.text.lower() for skill in candidate_info['skills']):

                    msg = bot.send_message(chat_id,
                                           "❗you have already entered this skills ❗, please enter another 😊,"
                                           "or type 'done' if you've finished entering your skills 🛠🛠🛠😊")
                    bot.register_next_step_handler(msg, input_info_skills, candidate_info)
                else:
                    candidate_info['skills'].append({'skill_name': message.text})

                    msg = bot.send_message(chat_id,
                                           " Enter another skill 🛠, or type 'done' if you've finished"
                                           " entering your skills 😊")
                    bot.register_next_step_handler(msg, input_info_skills, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def save_data(message, candidate_info):
        try:
            first_name = candidate_info['first_name']
            last_name = candidate_info['last_name']
            main_skill = candidate_info['main_skill']
            email = candidate_info['email']
            salary = candidate_info['salary']
            experience = candidate_info['experience']
            desired_job_position = candidate_info['desired_job_position']
            user_skills = candidate_info.get('skills', [])
            chat_id = message.chat.id

            new_candidate = CandidatesCreate(
                desired_job_position=desired_job_position,
                email=email,
                first_name=first_name,
                last_name=last_name,
                main_skill=main_skill,
                experience=experience,
                desired_salary=salary,
            )
            skills_to_add = [SkillsCreate(name=skill_dict.get('skill_name', '')) for skill_dict in user_skills]
            candidate = add_candidate(new_candidate, skills_to_add)

            bot.send_message(chat_id, print_resume(candidate_info))

            candidate_resume_data = CandidateResumeCreate(
                candidate_id=candidate.id,
                chat_id=chat_id
            )
            add_candidate_resume(candidate_resume_data)
        except Exception as e:
            bot.reply_to(message, f'❗❗❗Error. Please try again {e}')

    def show_candidate_resume(message):
        chat_id = message.chat.id
        candidate_resume = get_candidate_resume(chat_id)
        try:
            bot.send_message(chat_id,
                             f'{print_resume(candidate_resume)}')
        except Exception as e:
            bot.reply_to(message, f'❗❗❗Error. Please try again {e}')

