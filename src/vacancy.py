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