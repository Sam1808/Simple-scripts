import requests
import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

def predict_salary(starting_salary, final_salary):
    if not final_salary:
        average_salary = int(starting_salary) * 1.2
    elif not starting_salary:
        average_salary = int(final_salary) * 0.8
    else:
        average_salary = int(starting_salary + final_salary) / 2
    return average_salary


def predict_rub_salary_sj(vacancy):
    starting_salary = vacancy.get('payment_from')
    final_salary = vacancy.get('payment_to')
    average_salary = int(predict_salary(starting_salary, final_salary))
    return average_salary


def predict_rub_salary_hh(vacancy_salary):
    starting_salary = vacancy_salary.get('from')
    final_salary = vacancy_salary.get('to')
    average_salary = predict_salary(starting_salary, final_salary)
    if vacancy_salary.get('gross'): # take away tax 13%
        average_salary = average_salary/113*100
    average_salary = int(average_salary)
    return average_salary


def create_table(dictionary, title):
    table_data = [('Programming language', 'Vacancies found', 'Vacancies processed', 'Average salary')]
    for language in dictionary:
        description = dictionary.get(language)
        founded = description.get('Founded vacancies')
        processed = description.get('Vacancies processed')
        salary = description.get('Аverage salary')
        summury = (language, founded, processed, salary)
        table_data.append(summury)
    table_instance = AsciiTable(table_data, title)
    return table_instance.table

def checking_hh_ru(language):
    url = 'https://api.hh.ru/vacancies'
    print('HH.ru: Calculate for ', language)
    summury_info = {}
    text = f'Программист {language}'
    payload = {'text': text, 'area': 1, 'period': 30, 'only_with_salary': 'true', 'per_page': 100}
    response = requests.get(url, params=payload)
    founded_vacancies = response.json()['found']
    if founded_vacancies > 100:
        summury_info.update({'Founded vacancies': founded_vacancies})
        page_number = 0
        total_pages = 1
        vacancies_processed = 0
        salaries = 0
        while page_number < total_pages:
            payload.update({'page': page_number})
            response = requests.get(url, params=payload)
            total_pages = response.json()['pages']
            print('Reading page: ', page_number + 1, 'from total pages: ', total_pages)
            vacancies_catalog = response.json()['items']
            for vacancy in vacancies_catalog:
                vacancy_salary = vacancy.get('salary')
                if vacancy_salary.get('currency') != 'RUR':
                    continue
                vacancies_processed += 1
                salaries = salaries + predict_rub_salary_hh(vacancy_salary)
            page_number += 1
        average_salary = int(salaries / vacancies_processed)
        summury_info.update({'Vacancies processed': vacancies_processed})
        summury_info.update({'Аverage salary': average_salary})
        language_vacancies_hh.update({language: summury_info})
    else:
        print('Less than 100 vacancies at hh.ru (Moscow). Skipping... ')
    return language_vacancies_hh

def checking_superjob(language):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    print('SuperJob.ru: Calculate for ', language)
    summury_info = {}
    text = f'Программист {language}'
    load_dotenv()
    superjob_key = os.getenv("SUPERJOB_KEY")
    headers = {"X-Api-App-Id": superjob_key}
    per_page = 10 #only for testing pagination
    payload = {'keyword': text, 'town': 4, 'no_agreement': 1, 'count': per_page} #vacancies w|o agreements
    response = requests.get(url, params=payload, headers=headers)
    founded_vacancies = response.json()['total']
    if founded_vacancies:
        summury_info.update({'Founded vacancies': founded_vacancies})
        page_number = 0
        total_pages = 1
        vacancies_processed = 0
        salaries = 0
        if founded_vacancies > per_page:
            total_pages = (founded_vacancies // per_page) + 1
        while page_number < total_pages:
            payload.update({'page': page_number})
            response = requests.get(url, params=payload, headers=headers)
            print('Reading page: ', page_number + 1, 'from total pages: ', total_pages)
            vacancies_catalog = response.json()['objects']
            for vacancy in vacancies_catalog:
                vacancies_processed += 1
                salaries = salaries + predict_rub_salary_sj(vacancy)
            page_number += 1
        average_salary = int(salaries / vacancies_processed)
        summury_info.update({'Vacancies processed': vacancies_processed})
        summury_info.update({'Аverage salary': average_salary})
        language_vacancies_sj.update({language: summury_info})
    else:
        print('There is no vacancies at SuperJob.ru (Moscow). Skipping... ')
    return language_vacancies_sj

if __name__ == '__main__':

    languages = [
        'TypeScript', 'Swift', 'Scala', 'Objective-C', 'Shell',
        'Go', 'C', 'C#', 'C++', 'PHP', 'Ruby', 'Python', 'Java',
        'JavaScript'
    ]

    #languages = ['Python', 'Java']

    language_vacancies_hh = {}
    language_vacancies_sj = {}


    for language in languages:
        language_vacancies_hh.update(checking_hh_ru(language))
        language_vacancies_sj.update(checking_superjob(language))

    print()
    print(create_table(language_vacancies_hh, 'HeadHunter Moscow'))
    print()
    print(create_table(language_vacancies_sj, 'SuperJob Moscow'))

