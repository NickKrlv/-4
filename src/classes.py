import pprint

import requests
from datetime import datetime
import json
import os
from abc import ABC, abstractmethod


class API(ABC):
    """
    Abstract class for API
    """

    @abstractmethod
    def get_vacancies(self):
        pass


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, name, page, count):
        self.name = name
        self.page = page
        self.count = count

    def __repr__(self):
        return f"Vacancy(name={self.name}, page={self.page}, count={self.count})"


class hh(Vacancy, API):
    """
    Class for hh.ru
    """

    def __init__(self, name, page, count):
        super().__init__(name, page, count)
        self.url = 'https://api.hh.ru'

    def get_vacancies(self):
        """ Метод для получения вакансий по запросу """

        data = requests.get(f'{self.url}/vacancies',
                            params={'text': self.name, 'page': self.page, 'per_page': self.count}).json()
        return data

    def load_vacancies(self):
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
                'solary_startswith': vacancy['salary']['from'] if vacancy.get('salary') else None,
                'solary_endswith': vacancy['salary']['to'] if vacancy.get('salary') else None,
                'responsibility': vacancy['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y")
            }
            vacancies.append(vacancy_info)

        return vacancies


class superjob(Vacancy, API):
    """
    Class for superjob.ru
    """

    def get_vacancies(self):
        pass


a = hh('Python разработчик', 1, 2)

pprint.pprint(a.get_vacancies())
