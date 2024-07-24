import psycopg2
from data.config import PARAMS_BD

class CREATE_DB():
    """Класс для создания и наполнения базы данных и таблиц в ней"""
    def __init__(self) -> None:
        self.params = PARAMS_BD
        self.database_name = 'vacansies_hh'

    def __str__(self) -> str:
        return ("Класс для создания и наполнения базы данных и таблиц в ней")

    def create_database(self):
        """Создание базы данных (проверка подключения и удаление всех данныз из ранее созданной)
          и таблиц для сохранения данных о компаниях и вакансиях"""

        conn = psycopg2.connect(dbname='postgres', **self.params)

        with conn.cursor() as cur:
            conn.autocommit = True
            cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
            cur.execute(f"CREATE DATABASE {self.database_name}")
            conn.commit()
        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE companies(
                    company_id INT PRIMARY KEY, company_title VARCHAR(35) NOT NULL);
            CREATE TABLE vacancies (
                    vacancy_id INT PRIMARY KEY,
                    company_id INT REFERENCES companies(company_id),
                    vacancy_title VARCHAR(155) NOT NULL,
                    salary_from INT,
                    vacancy_url TEXT);
                    ''')
            conn.commit()
        conn.close()

    def filling_table(self, data_for_table, table_name):
        """Наполняет таблицу данными из json файла"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            for line in data_for_table:
                values = ("%s," * len(line))[:-1]
                try:
                    cur.execute(f"INSERT INTO {table_name} VALUES ({values})", tuple(line.values()))
                except psycopg2.errors.UniqueViolation:
                    pass
                conn.commit()
