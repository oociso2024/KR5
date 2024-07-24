import json
from creating_database import CREATE_DB
from data.config import PATH_COMPANY
from db_manager import DBManager
import API_classes


def all_vacancies(path_companies):
    """Получает список вакансии всех компаний записанных в файле 'path_companies' """
    with open(path_companies, 'r', encoding='UTF-8') as f:
        all_companies = json.load(f)
        vacancy_hh_all = []
        for employer in all_companies:
            data_hh = API_classes.HH_API(employer["company_id"])
            vacancy_company = data_hh.preparation_vacancy_one_company()
            vacancy_hh_all.extend(vacancy_company)
    return vacancy_hh_all

def create_database():
    """Создает базу данных с таблицами и заполняет их"""
    db = CREATE_DB()
    db.create_database()
    with open(PATH_COMPANY, 'r', encoding="utf-8") as comp:
        data_for_company = json.load(comp)
    db.filling_table(data_for_company, 'companies')
    data_for_vacancy = all_vacancies(PATH_COMPANY)
    db.filling_table(data_for_vacancy, 'vacancies')

def users_work():
    """Функция для работы с пользователем"""

    while True:
        exempl_db = DBManager()
        # Создаем экземпляр класса для работы с пользователем
        try:
            choice_action = int(input("""
            Программа может показать:
                1 - список всех компаний и количество вакансий у каждой компании,
                2 - список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию,
                3 - среднюю зарплату по вакансиям,
                4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям,
                5 - список всех вакансий, по запросу от пользователя.

                0 - выход из программы 

                Выберите действие (цифра от 0 до 5) и нажмите "Enter": """))

            if choice_action == 1:
                print('Вывожу список всех компаний и количество вакансий у каждой компании: ')
                exempl_db.get_companies_and_vacancies_count()

            elif choice_action == 2:
                print('Вывожу список всех вакансий:')
                exempl_db.get_all_vacancies()

            elif choice_action == 3:
                print('Вывожу среднюю зарплату по вакансиям:')
                exempl_db.get_avg_salary()

            elif choice_action == 4:
                print('Вывожу список всех вакансий, у которых зарплата выше средней по всем вакансиям:')
                exempl_db.get_vacancies_with_higher_salary()

            elif choice_action == 5:
                requst_user = input("Введите слово или фразу для поиска: ")
                exempl_db.get_vacancies_with_keyword(requst_user)

            elif choice_action == 0:
                print("Программа завершена.")
                break
            else:
                print("Операцию на этот номер пока не назначили. Попробуйте ещё раз")
                continue
        except ValueError:
            print("Не верный ввод, вводимые данные должны быть цифрой от 0 до 5. Попробуйте ещё раз")
            continue
