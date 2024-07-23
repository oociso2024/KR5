from utils import create_database, users_work

def main():
    create_database()
    #Создаем базу данных и таблицы и наполняем актуальными вакансиями

    print('Вакансии загружены в базу данных (валюта "РУБ")')

    users_work()
    #Начинаем работу с пользователем

if __name__ == "__main__":
    main()