def print_resume(candidate_info):
    first_name = candidate_info['first_name']
    desired_job_position = candidate_info['desired_job_position']
    main_skill = candidate_info['main_skill']
    last_name = candidate_info['last_name']
    email = candidate_info['email']
    salary = candidate_info['salary']
    experience = candidate_info['experience']
    user_skills = candidate_info.get('skills', [])

    all_skills_user = ""
    for skill_dict in user_skills:
        skill_name = skill_dict.get('skill_name', '')
        all_skills_user += '\t\t• ' + skill_name + '\n'

    message = (
        "📝 Resume 📝\n\n"
        f"👤 Name: {first_name} {last_name}\n"
        f"🎯 Desired Position: {desired_job_position}\n"
        f"⏳ Work Experience: {experience}\n"
        f"💰 Desired Salary: {salary}\n"
        f"📧 Email: {email}\n"
        f"💡 Main Skill: {main_skill}\n"
        f"🛠 Skills:\n{all_skills_user}"
    )
    return message


def print_vacancy(vacancy_info):
    title = vacancy_info['title']
    description = vacancy_info['description']
    salary = vacancy_info['salary']
    requirements_for_job = vacancy_info.get('requirements', [])

    all_requirements = ""
    for requirement_dict in requirements_for_job:
        requirement_name = requirement_dict.get('requirement_name', '')
        all_requirements += '\t\t• ' + requirement_name + '\n'

    message = (
        "💼 Job Vacancy 💼\n\n"
        f"👤 Position: {title}\n"
        f"🎯 Description: {description}\n"
        f"💰 Salary: {salary}\n"
        f"🛠 Requirements:\n{all_requirements}"
    )
    return message
