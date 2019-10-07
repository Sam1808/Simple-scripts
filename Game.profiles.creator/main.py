import file_operations
import os
import random
from faker import Faker

def replace_to_old_alfabet(skill):
    skill_with_runic_letters = ''
    for letter in skill:
        if letter.isalpha():
            letter = letter.replace(letter, old_english_alfabet.get(letter))
        skill_with_runic_letters += letter
    return skill_with_runic_letters

def get_hero_description():
    first_name = fake.first_name()
    last_name = fake.last_name()
    city = fake.city()
    specialization = fake.job()
    return first_name, last_name, city, specialization


if __name__ == '__main__':

    fake = Faker()

    skills = [
        'Rapid jump', 'Electric shot', 'Ice strike', 'Rapid strike', 'Acid look',
        'Secret escape', 'Ice shot', 'Fiery bomb',
    ]

    old_english_alfabet = {            # use english old alfabet
        'A': '𝔄', 'B': '𝔅', 'C': 'ℭ',
        'D': '𝔇', 'E': '𝔈', 'F': '𝔉',
        'G': '𝔊', 'H': 'ℌ', 'I': 'ℑ',
        'J': '𝔍', 'K': '𝔎', 'L': '𝔏',
        'M': '𝔐', 'N': '𝔑', 'O': '𝔒',
        'P': '𝔓', 'Q': '𝔔', 'R': 'ℜ',
        'S': '𝔖', 'T': '𝔗', 'U': '𝔘',
        'V': '𝔙', 'W': '𝔚', 'X': '𝔛',
        'Y': '𝔜', 'Z': 'ℨ', 'a': '𝔞',
        'b': '𝔟', 'c': '𝔠', 'd': '𝔡',
        'e': '𝔢', 'f': '𝔣', 'g': '𝔤',
        'h': '𝔥', 'i': '𝔦', 'j': '𝔧',
        'k': '𝔨', 'l': '𝔩', 'm': '𝔪',
        'n': '𝔫', 'o': '𝔬', 'p': '𝔭',
        'q': '𝔮', 'r': '𝔯', 's': '𝔰',
        't': '𝔱', 'u': '𝔲', 'v': '𝔳',
        'w': '𝔴', 'x': '𝔵', 'y': '𝔶',
        'z': '𝔷'
    }

    path = 'Profiles'
    os.makedirs(path, exist_ok = True)
    abspath = os.path.abspath(path)

    count_of_profiles = 10
    number_of_random_skills = 3
    power_from = 8
    power_to = 14

    for profile in range(count_of_profiles):

        first_name, last_name, city, specialization = get_hero_description()

        random_skills = random.sample(skills, number_of_random_skills)

        runic_skills = []

        for skill in random_skills:
            runic_skill = replace_to_old_alfabet(skill)
            runic_skills.append(runic_skill)

        context = {
            "name": first_name,
            "surname": last_name,
            "city": city,
            "specialization": specialization,
            "strength": random.randint(power_from,power_to),
            "dexterity": random.randint(power_from,power_to),
            "precision": random.randint(power_from,power_to),
            "endurance": random.randint(power_from,power_to),
            "mana": random.randint(power_from,power_to),
            "luck": random.randint(power_from,power_to),
            "oratory": random.randint(power_from,power_to),
            "first_skill": runic_skills[0], # index uses due to random choice
            "second_skill": runic_skills[1],
            "third_skill": runic_skills[2],
        }

        filename = f'charsheet-{profile}.txt'
        filename = os.path.join(abspath,filename)
        file_operations.render_template("template.txt", filename, context)