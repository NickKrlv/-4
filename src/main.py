from src.classes import *
from pprint import pprint


def user_interaction():
    while True:
        platforms = ["headhunter", "superjob"]
        platform = input("Выберите платформу HeadHunter или SuperJob (Enter, если обе): ").lower()

        if platform in ("headhunter", "hh", "HH"):
            name = input("Введите название вакансии: ")
            page = int(input("Введите страницу: "))
            top_n = int(input("Количество вакансий: "))
            salary = bool(input("Отображать вакансии только с зарплатой?\n"
                                "По умолчанию True.\n"
                                "Введите True или False: "))
            if salary == "":
                salary = True

            headhunter = HeadHunter(name, page, top_n, salary)
            data = headhunter.load_vacancies()
            pprint(data)

        elif platform in ("superjob", "sj", "SJ"):
            name = input("Введите название вакансии: ")
            page = int(input("Введите страницу: "))
            top_n = int(input("Количество вакансий: "))
            superjob = SuperJob(name, top_n, page)
            data = superjob.load_vacancies()
            pprint(data)

        elif platform == "":
            name = input("Введите название вакансии: ")
            print("Будут выведены результаты первой страницы с обеих платформ...")
            headhunter = HeadHunter(name, 1, 10, True)
            superjob = SuperJob(name, 1, 10)
            data_hh = headhunter.load_vacancies()
            data_sj = superjob.load_vacancies()
            data = data_hh + data_sj
            pprint(data)


if __name__ == "__main__":
    user_interaction()
