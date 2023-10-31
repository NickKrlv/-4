from abc import ABC, abstractmethod
from datetime import datetime

import requests

from src.vacancy import Vacancy


class API(ABC):
    """
    Abstract class for API
    """

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def load_vacancies(self):
        pass


class HeadHunter(Vacancy, API):
    """
    Class for hh.ru
    """

    def __init__(self, name: str, page: int, top_n: int, salary: True) -> None:
        super().__init__(name, page, top_n)
        self.salary = salary
        self.url = 'https://api.hh.ru'

    def get_vacancies(self) -> dict:
        """ Метод для получения вакансий по запросу """

        data = requests.get(f'{self.url}/vacancies',
                            params={'text': self.name, 'per_page': self.top_n,
                                    'only_with_salary': self.salary,
                                    'page': self.page, 'id': '113'}).json()
        return data

    def load_vacancies(self) -> list:
        """
        Метод для загрузки вакансии
        """
        data = self.get_vacancies()
        vacancies = []
        for vacancy in data.get('items', []):
            published_at = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'id': vacancy['id'],
                'name': vacancy['name'],
                'salary_bot': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'salary_top': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'], 'area': vacancy['area']['name'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vacancies.append(vacancy_info)

        return vacancies


class SuperJob(Vacancy, API):
    def __init__(self, name: str, page: int, top_n: int) -> None:
        super().__init__(name, page, top_n)
        self.url = 'https://api.superjob.ru/2.0/vacancies/'
        self.API_KEY = 'v3.r.129671221.990b428068d53605273fe5deeaebb481683b09eb.a856271df14092e5bb9fcde0df3575061475c724'

    def get_vacancies(self):
        headers = {
            'X-Api-App-Id': self.API_KEY
        }
        data = requests.get(self.url, headers=headers,
                            params={'keywords': self.name, 'page': self.page, 'count': self.top_n}).json()
        return data

    def load_vacancies(self):
        data = self.get_vacancies()
        vacancies = []
        for vacancy in data.get('objects', []):
            published_at = datetime.fromtimestamp(vacancy.get('date_published', ''))
            vacancy_info = {
                'id': vacancy['id'],
                'name': vacancy.get('profession', ''),
                'salary_bot': vacancy.get('payment_from', '') if vacancy.get('payment_from') else None,
                'salary_top': vacancy.get('payment_to') if vacancy.get('payment_to') else None,
                'responsibility': vacancy.get('candidat').replace('\n', '').replace('•', '')
                if vacancy.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),
            }

            vacancies.append(vacancy_info)

        return vacancies
