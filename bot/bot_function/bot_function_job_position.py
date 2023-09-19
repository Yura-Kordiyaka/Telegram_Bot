from db.utilits import *
from db.schemas_models import *


def vacancy_handler(bot):
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
            msg = bot.send_message(chat_id, f"Дякую,тепер напишіть навички  по однії які потрібні  для цієї роботи ")
            bot.register_next_step_handler(msg, input_info_requirements, vacancy_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_requirements(message, vacancy_info):
        try:
            chat_id = message.chat.id
            if message.text.lower() == 'готово':
                msg = bot.send_message(chat_id,
                                       f"Дякую,тепер опишіть більш детельно саму вакансію  ")
                bot.register_next_step_handler(msg, input_info_description, vacancy_info)
            else:
                if 'requirements' not in vacancy_info:
                    vacancy_info['requirements'] = []

                vacancy_info['requirements'].append(message.text)

                msg = bot.send_message(chat_id,
                                       "Напиши ще одну навичку, або напишить 'готово', якщо завершили введення навичок які потрібні для цієї роботи")
                bot.register_next_step_handler(msg, input_info_requirements, vacancy_info)

        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def input_info_description(message, vacancy_info):
        try:
            vacancy_info['description'] = message.text

            save_data(message, vacancy_info)
        except Exception as e:
            bot.reply_to(message, 'Помилка. Спробуйте ще раз.')

    def save_data(message, vacancy_info):
        try:
            title_vacancy = vacancy_info['title']
            description = vacancy_info['description']
            requirements = vacancy_info.get('requirements', [])
            chat_id = message.chat.id
            new_vacancy = JobPositionsCreate(
                title=title_vacancy,
                description=description
            )
            all_requirements = "\n"
            for i in requirements:
                all_requirements += '\t\t' + i + '\n'
            requirements_to_add = [RequirementsCreate(name=i) for i in requirements]
            add_vacancy(new_vacancy, requirements_to_add)
            bot.send_message(chat_id, f"назва посади : {title_vacancy}\n"
                                      f"обов'язки які потрібно мати :{all_requirements}"
                                      f"більш детально про роботу : {description}")
        except Exception as e:
            bot.reply_to(message, f'Помилка. Спробуйте ще раз {e}')
