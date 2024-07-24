import requests, json
from data.config import HH_VACANCIES_URL, HH_HEADERS, COUNT_HH, PATH_LOG, currency_change, PAGES


class HH_API():
    """Класс для поиска вакансий на сайте HH.ru по id_работодателя"""

    def __init__(self, employer_id: str) -> None:
        self.employer_id = employer_id
        self.__url = HH_VACANCIES_URL
        self.__headers = HH_HEADERS
        self.__page = PAGES

    def __str__(self) -> str:
        return ("Класс для поиска вакансий на сайте HH.ru по id работодателя")

    def get_response(self, page):
        """Принимает параметры и выдает список найденных вакансий в формате Json"""
        self.page = page
        self.response = requests.get(url=self.__url, headers=self.__headers,
                                     params={"employer_id": self.employer_id,
                                             "per_page": COUNT_HH,
                                             'page': self.page,
                                             "archived": False})
        return self.response.json()

    def preparation_vacancy_one_company(self):
        """Получает данные в формате Json и возвращает общий список словарей с только необходимыми параметрами
        вакансий"""
        all_vacancy = []
        for page in range(self.__page):
            vacancy_hh = self.get_response(page)
            for vacancy in vacancy_hh["items"]:
                try:
                    all_vacancy.append(dict(vacancy_id=int(vacancy['id']),
                                            employer_id=self.employer_id, vacancy_name=vacancy.get('name'),
                                            salary_from=(self.currency_exchange(vacancy['salary']['from'],
                                                                                vacancy['salary'][
                                                                                    'currency'])) if vacancy.get(
                                                'salary')
                                            else None, url=vacancy['alternate_url']))
                except TypeError:
                    with open(PATH_LOG, "a", encoding="UTF-8") as file:
                        file.write(json.dumps(vacancy, ensure_ascii=False))
                    continue
        return all_vacancy

    def currency_exchange(self, salary, currenty):
        """Получает данные о сумме и валюте, и возвращает сумму конвертируемую в рубли при необходимости"""
        if salary != None and salary != 0:
            if currenty == "RUR" or "rub":
                data_change = salary
            else:
                data_change = salary * currency_change[currenty.upper()]
        else:
            data_change = None
        return data_change
