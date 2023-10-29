import pytest
from src.main import *


def test_headhunter():
    vacancies = HeadHunter('python', 1, 10, True).get_vacancies()
    assert len(vacancies) == 10

    vacancies = HeadHunter('python', 1, 10, False).load_vacancies()
    assert len(vacancies) == 10


def test_superjob():
    vacancies = SuperJob('python', 1, 5).get_vacancies()
    assert len(vacancies) == 5

    vacancies = SuperJob('python', 1, 5).load_vacancies()
    assert len(vacancies) == 5


def test_filter():
    vacancies = HeadHunter('python', 1, 10, True).load_vacancies()
    assert len(vacancies) == 10
    vacancies = Filter_vacancies.filter(vacancies, ['Чурчхелла'])
    assert len(vacancies) == 0
