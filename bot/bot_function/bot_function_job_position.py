from datetime import timedelta

from db.utilits_vacancy import *
from db.utilits_candidate import *
from db.schemas_models import *
from .bot_print_message import *
from telebot import types
from programming_languages import programming_languages, experience_levels


def vacancy_handler(bot):
    @bot.callback_query_handler(func=lambda call: call.data == "recruiter")
    def handle_employer(call):
        try:
            chat_id = call.message.chat.id
            keyboard = types.InlineKeyboardMarkup()
            show_candidate = types.InlineKeyboardButton(text="Do you want to view candidates 👤?",
                                                        callback_data="show_candidate_by_parameters")
            add_vacancy = types.InlineKeyboardButton(text="Do you want to create a vacancy📝? ",
                                                     callback_data="create_vacancy")
            keyboard.row(show_candidate)
            keyboard.row(add_vacancy)
            bot.send_message(chat_id, "choose whether you want to view candidates 🔎👤 or create a job vacancy 💼?",
                             reply_markup=keyboard)
        except Exception as e:
            bot.reply_to(call.message, f'❗❗❗Error. Please try again {e}')

    @bot.callback_query_handler(func=lambda call: call.data == "show_candidate_by_parameters")
    def show_candidate_by_parameters(call):
        keyboard = types.InlineKeyboardMarkup()
        try:
            chat_id = call.message.chat.id
            for programming_language in programming_languages:
                selected_language = programming_language.split(" ")[0]
                add_programming_language = types.InlineKeyboardButton(text=f"{programming_language}",
                                                                      callback_data=f"add_programming_language:{selected_language}")
                keyboard.add(add_programming_language)
            bot.send_message(chat_id, f"select programming language", reply_markup=keyboard)
        except Exception as e:
            bot.reply_to(call.message, f'❗❗❗Error. Please try again {e}')

    employer_requirements = {}

    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_programming_language:"))
    def handle_programming_language(call):
        chat_id = call.message.chat.id
        keyboard = types.InlineKeyboardMarkup()
        try:
            programming_language = call.data.split(":")[1]
            employer_requirements['programming_language'] = programming_language
            for experience_level in experience_levels:
                selected_level = experience_level.split(' ')[0]
                add_experience_level = types.InlineKeyboardButton(text=f"{experience_level}",
                                                                  callback_data=f"add_experience_level:{selected_level}")
                keyboard.add(add_experience_level)
            bot.send_message(chat_id, f"select the level of experience you need",
                             reply_markup=keyboard)
        except Exception as e:
            bot.reply_to(call.message, f'❗❗❗Error. Please try again {e}')

    @bot.callback_query_handler(func=lambda call: call.data.startswith("add_experience_level:"))
    def handle_search_candidates(call):
        try:
            chat_id = call.message.chat.id
            experience_level = call.data.split(":")[1]
            employer_requirements['experience_level'] = experience_level
            programming_language = employer_requirements['programming_language']
            experience_level = employer_requirements['experience_level']
            all_candidates = search_candidates_by_language_and_level(programming_language, experience_level)
            if_candidates_exists = 0
            for candidate in all_candidates:
                candidate = print_resume(candidate)
                bot.send_message(chat_id, f"{candidate}")
                if_candidates_exists += 1
            if if_candidates_exists == 0:
                bot.send_message(chat_id, f"unfortunately, there are no candidates with such requirements 😢")
        except Exception as e:
            bot.reply_to(call.message, f'❗❗❗Error. Please try again {e}')

    @bot.callback_query_handler(func=lambda call: call.data == "create_vacancy")
    def create_vacancy(call):
        try:
            chat_id = call.message.chat.id
            recent_recruiters_dicts=check_recruiter_time(chat_id)
            current_time = datetime.utcnow()
            one_hour_ago = current_time - timedelta(hours=1)
            recent_recruiters_last_hour = [recruiter for recruiter in recent_recruiters_dicts if
                                           recruiter['created_at'] >= one_hour_ago]
            if len(recent_recruiters_last_hour) >= 3:
                bot.send_message(chat_id, 'the recruiter can add no more than 3 vacancies per hour')
            else:
                msg = bot.send_message(chat_id, f"Please, enter the name of job position 🎯🎯🎯 ")
                bot.register_next_step_handler(msg, input_info_job_position, vacancy_data={})
        except Exception as e:
            bot.reply_to(call.message, f'❗❗❗Error. Please try again.{e}')

    def input_info_job_position(message, vacancy_data):
        try:
            chat_id = message.chat.id
            vacancy_data['title'] = message.text
            msg = bot.send_message(chat_id, f"Thank you 😊 , now enter salary for this job 💸💸💸")
            bot.register_next_step_handler(msg, input_info_salary, vacancy_data)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_salary(message, vacancy_data):
        chat_id = message.chat.id
        try:
            if message.text.isdigit():
                vacancy_data['salary'] = int(message.text)
                if vacancy_data['salary'] > 0:
                    msg = bot.send_message(chat_id,
                                           f"Thank you 😊,! now describe in more detail what you need to do in this job")
                    bot.register_next_step_handler(msg, input_info_description, vacancy_data)
                else:
                    msg = bot.send_message(chat_id,
                                           f"❗❗❗Input valid salary,salary must be grater then 0, please try again")
                    bot.register_next_step_handler(msg, input_info_salary, vacancy_data)
            else:
                msg = bot.send_message(chat_id,
                                       f"❗❗❗Input valid salary,salary must contain only digit 🔢")
                bot.register_next_step_handler(msg, input_info_salary, vacancy_data)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_description(message, candidate_info):
        try:
            chat_id = message.chat.id
            candidate_info['description'] = message.text

            msg = bot.send_message(chat_id,
                                   f"thank you, now tell me the skills 🛠 you need to have to get this job like SQL📊 or JS 💻")
            bot.register_next_step_handler(msg, input_info_requirements, candidate_info)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def input_info_requirements(message, vacancy_data):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'done':
                save_data(message, vacancy_data)
            else:
                if 'requirements' not in vacancy_data:
                    vacancy_data['requirements'] = []
                if any(skill['requirement_name'].lower() == message.text.lower() for skill in
                       vacancy_data['requirements']):

                    msg = bot.send_message(chat_id,
                                           "❗you have already entered this skills ❗, please enter another 😊,"
                                           "or type 'done' if you've finished entering your skills 🛠🛠🛠😊")
                    bot.register_next_step_handler(msg, input_info_requirements, vacancy_data)
                else:
                    vacancy_data['requirements'].append({'requirement_name': message.text})

                    msg = bot.send_message(chat_id,
                                           " Enter another skill 🛠, or type 'done' if you've finished"
                                           " entering your skills 😊")
                    bot.register_next_step_handler(msg, input_info_requirements, vacancy_data)
        except Exception as e:
            bot.reply_to(message, '❗❗❗Error. Please try again.')

    def save_data(message, vacancy_data):
        try:
            chat_id = message.chat.id
            title = vacancy_data['title']
            description = vacancy_data['description']
            salary = vacancy_data['salary']
            requirements_for_job = vacancy_data.get('requirements', [])

            new_vacancy = JobPositionsCreate(
                title=title,
                description=description,
                salary=salary
            )
            requirements_to_add = [RequirementsCreate(name=requirement_dict.get('requirement_name', '')) for
                                   requirement_dict in
                                   requirements_for_job]

            added_vacancy = add_vacancy(new_vacancy, requirements_to_add)

            new_vacancy_for_recruiter = RecruiterCreate(
                job_position_id=added_vacancy.id,
                chat_id=chat_id,
            )
            new_recruiter = add_recruiter_vacancy(new_vacancy_for_recruiter)

            msg = bot.send_message(chat_id, print_vacancy(vacancy_data))
            vacancy_data['vacancy_id'] = added_vacancy.id
            send_message_to_candidates(message, vacancy_data)
        except Exception as e:
            bot.reply_to(message, f'❗❗❗Error. Please try again {e}')

    def send_message_to_candidates(message, vacancy_data):
        try:
            all_candidates_chat_id = get_all_candidates_by_requirements(int(vacancy_data['vacancy_id']))
            if len(all_candidates_chat_id):
                for candidate_id, chat_id in all_candidates_chat_id:
                    bot.send_message(chat_id, f"a vacancy that may interest you 🧐\n{print_vacancy(vacancy_data)}")
            else:
                pass
        except Exception as e:
            bot.reply_to(message, f'❗❗❗Error. Please try again {e}')

