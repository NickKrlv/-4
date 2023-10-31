import json
from abc import ABC, abstractmethod


class Dump_json(ABC):
    """
    Abstract class for Dump_json
    """

    @abstractmethod
    def dump_file(self, vacancies):
        pass


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
