import pprint

import requests
from datetime import datetime
import json
from abc import ABC, abstractmethod


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


class Dump_json(ABC):
    """
    Abstract class for Dump_json
    """

    @abstractmethod
    def dump_file(self, vacancies):
        pass


class Vacancy:
    """
    Класс для работы с вакансиями
    """

    def __init__(self, name: str, page: int, top_n: int) -> None:
        self.name = name
        self.top_n = top_n
        self.page = page

    def __repr__(self):
        return f'Vacancy(name={self.name}, top_n={self.top_n})'


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
                'solary_ot': vacancy.get('payment_from', '') if vacancy.get('payment_from') else None,
                'solary_do': vacancy.get('payment_to') if vacancy.get('payment_to') else None,
                'responsibility': vacancy.get('candidat').replace('\n', '').replace('•', '')
                if vacancy.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),
            }

            vacancies.append(vacancy_info)

        return vacancies


class Dump_json_hh(Dump_json):
    """
    Загрузка вакансий hh в json
    """

    def __init__(self, vacancies):
        self.vacancies = vacancies

    def dump_file(self, **kwargs):
        """
        Записывает содержимое списка `vacancies` в файл в формате JSON.

        """
        with open('vacancies_hh.json', 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=2)


class Dump_json_sj(Dump_json):
    """
    Загрузка вакансий sj в json
    """

    def __init__(self, vacancies):
        self.vacancies = vacancies

    def dump_file(self, **kwargs):
        """
        Записывает содержимое списка `vacancies` в файл в формате JSON.

        """
        with open('vacancies_sj.json', 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False, indent=2)


class Filter_vacancies:
    """
    Фильтрует заданный список вакансий на основе предоставленных фильтров.

    Параметры:
        vacancies (list): Список вакансий для фильтрации.
        filter_words (list): Список слов для фильтрации вакансий.

    Возвращает:
        list: Отфильтрованный список вакансий, соответствующий любому из фильтровых слов в их поле ответственности.
    """

    @classmethod
    def filter(cls, vacancies, filter_words):
        filtered_vacancies = []
        for vacancy in vacancies:
            for word in filter_words:
                if word in vacancy['responsibility']:
                    filtered_vacancies.append(vacancy)
        return filtered_vacancies


if __name__ == "__main__":

    while answer := input("Хотите загрузить вакансии из HeadHunter или SuperJob? Да/Нет: ").lower():
        if answer == "да":
            platforms = ["headhunter", "superjob"]
            platform = input("Выберите платформу HeadHunter или SuperJob: ").lower()

            if platform in ("headhunter", "hh", "HH"):
                name = input("Введите ключевое слово в вакансии: ")
                page = int(input("Введите страницу: "))
                top_n = int(input("Количество вакансий: "))
                salary = bool(input("Отображать вакансии только с зарплатой?\n"
                                    "По умолчанию True.\n"
                                    "Введите True или False: "))
                if salary == "":
                    salary = True

                data_hh = HeadHunter(name, page, top_n, salary).load_vacancies()

                if answer_filter := input("Хотите отфильтровать вакансии по вашим\n"
                                          "ключевым словам в описании?\n"
                                          "(количество вакансий может уменьшиться) Да/Нет: ").lower():
                    if answer_filter == "да":
                        filter_words = input("Введите ключевые слова через пробел: ").split()
                        filtered_vacancies = Filter_vacancies.filter(data_hh, filter_words)
                        data_hh = filtered_vacancies
                        data_hh = Dump_json_hh(data_hh)
                        data_hh.dump_file()

                    else:
                        data_hh = Dump_json_hh(data_hh)
                        data_hh.dump_file()

                with open('vacancies_hh.json', 'r', encoding='utf-8') as file:
                    data_hh = json.load(file)

                    if len(data_hh) == 0:
                        print("Ничего не найдено")

                    else:
                        for vacancy in data_hh:
                            date = vacancy.get('data')
                            name = vacancy.get('name')
                            responsibility = vacancy.get('responsibility')
                            area = vacancy.get('area')
                            if vacancy.get('salary_bot'):
                                salary_bot = vacancy.get('salary_bot')
                            else:
                                salary_bot = None
                            if vacancy.get('salary_top'):
                                salary_top = vacancy.get('salary_top')
                            else:
                                salary_top = None
                            if salary_bot and salary_top:
                                print(f'{date} | {name} | {responsibility} | {area} | {salary_bot} - {salary_top}')
                            else:
                                print(f'{date} | {name} | {responsibility} | {area}')

            elif platform in ("superjob", "sj", "SJ"):
                name = input("Введите ключевое слово в вакансии: ")
                page = int(input("Введите страницу: "))
                top_n = int(input("Количество вакансий: "))
                data_sj = SuperJob(name, page, top_n).load_vacancies()

                if answer_filter := input("Хотите отфильтровать вакансии по вашим\n"
                                          "ключевым словам в описании?\n"
                                          "(количество вакансий может уменьшиться) Да/Нет: ").lower():
                    if answer_filter == "да":
                        filter_words = input("Введите ключевые слова через пробел: ").split()
                        filtered_vacancies = Filter_vacancies.filter(data_sj, filter_words)
                        data_sj = Dump_json_sj(filtered_vacancies)
                        data_sj.dump_file()

                    else:
                        data_sj = Dump_json_sj(data_sj)
                        data_sj.dump_file()

                with open('vacancies_sj.json', 'r', encoding='utf-8') as file:
                    data_sj = json.load(file)

                    if len(data_sj) == 0:
                        print("Ничего не найдено")

                    else:
                        for vacancy in data_sj:
                            date = vacancy.get('data')
                            name = vacancy.get('name')
                            responsibility = vacancy.get('responsibility')

                            print(f'{date} | {name} | {responsibility}')

            else:
                print("Неизвестная платформа")
                continue

        elif answer == "нет":
            break

        else:
            print("Неизвестная команда")
            continue
