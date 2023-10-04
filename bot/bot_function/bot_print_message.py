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
        all_skills_user += '\t\t' + skill_name + '\n'

    message = f"Name: {first_name} {last_name}\n"
    message += f"Desired position: {desired_job_position}\n"
    message += f"Work Experience: {experience}\n"
    message += f"Desired Salary: {salary}\n"
    message += f"Email: {email}\n"
    message += f"Main skill: {main_skill}\n"
    message += f"Skills:\n{all_skills_user}"
    return message
