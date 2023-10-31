class Sorting:
    """
    Сортирует список вакансий по зарплате в порядке убывания.

    Аргументы:
        vacancies (list): Список вакансий, где каждая вакансия представлена в виде словаря с ключом 'salary_bot'.

    Возвращает:
        list: Отсортированный список вакансий, отсортированный по зарплате в порядке убывания.
    """

    @staticmethod
    def sort_by_salary(vacancies):
        def get_salary_bot(vacancy):
            return vacancy.get('salary_bot', float('-inf')) if vacancy.get('salary_bot') is not None else float('-inf')

        return sorted(vacancies, key=get_salary_bot, reverse=True)