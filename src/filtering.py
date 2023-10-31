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