import psycopg2
from data.config import PARAMS_BD

class DBManager():
    """Класс для поиска вакансий в базе данных по запросам """
    def __init__(self) -> None:
        self.params = PARAMS_BD
        self.database_name = 'vacansies_hh'
        self.conn = psycopg2.connect(dbname=self.database_name, **self.params)

    def cursor(self, request):
        """Получает запрос, подключается в БД, выдает результат"""
        with  self.conn.cursor() as cur:
            cur.execute(f'{request}')
            rows = cur.fetchall()
            for row in rows:
                print(row)
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        self.cursor('''SELECT company_title, COUNT(*) AS quin
                    FROM companies JOIN vacancies USING (company_id)
                    GROUP BY company_id''')

    def get_all_vacancies(self):
        """Получает список всех вакансий"""
        self.cursor('''SELECT company_title, vacancy_title, salary_from ,vacancy_url FROM companies 
                    JOIN vacancies USING (company_id)''')

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        self.cursor('''SELECT AVG(salary_from) FROM vacancies
                    WHERE salary_from IS NOT NULL''')

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cursor('''SELECT company_title, vacancy_title, salary_from ,vacancy_url FROM companies 
                JOIN vacancies USING (company_id)
                WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)''')

    def get_vacancies_with_keyword(self, user_request):
        """Получает слово для поиска, возвращает найденные сущности"""
        with self.conn.cursor() as cur:
            cur.execute(f'''SELECT company_title, vacancy_title, salary_from ,vacancy_url FROM vacancies
                            JOIN companies USING (company_id)
                            WHERE vacancy_title LIKE '%{user_request}%' ''')
            rows = cur.fetchall()
            if len(rows) == 0:
                print("Вакансий с таким запросом нет.")
            else:
                print(f'Вывожу список вакансий, в названиях которых есть: {user_request}:')
                for row in rows:
                    print(row)
        self.conn.close()
