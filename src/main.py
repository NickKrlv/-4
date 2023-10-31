import json

from api import HeadHunter, SuperJob
from dump_json import Dump_json_hh, Dump_json_sj
from filtering import Filter_vacancies
from sorting import Sorting


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

                if answer_sorting := input("Хотите сортировать вакансии по зарплате?\n"
                                           "Да/Нет: ").lower():
                    if answer_sorting == "да":
                        data_hh = Sorting.sort_by_salary(data_hh)

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

                if answer_sorting := input("Хотите сортировать вакансии по зарплате?\n"
                                           "Да/Нет: ").lower():
                    if answer_sorting == "да":
                        data_sj = Sorting.sort_by_salary(data_sj)

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