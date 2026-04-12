import pytest

from pydantic import BaseModel

from task_4.task_4_introspection import (
    check_models_input,
    get_cls_info,
)


class EmptyModel(BaseModel):
    pass


class ValidModel1(BaseModel):
    id: int
    fio: str = "test"


class ValidModel2(BaseModel):
    id: int


class InValidModel:
    id: int


"""Тесты check_all_are_basemodel()"""


def test_check_models_input_on_all_valid_models():
    assert check_models_input([ValidModel1, ValidModel2]) is True


def test_check_models_input_on_invalid_model():
    with pytest.raises(Exception):
        check_models_input([ValidModel1, InValidModel])


def test_check_models_input_on_empty_list():
    empty_list = list()
    with pytest.raises(Exception):
        check_models_input(empty_list)


def test_check_models_input_on_not_list_input():
    empty_set = set()
    with pytest.raises(Exception):
        check_models_input(empty_set)


"""Тесты get_cls_info()"""


def test_get_cls_info():
    result = get_cls_info(ValidModel1)
    assert result[0] == ("id", "int", "-")
    assert result[1] == ("fio", "str", "test")


def test_get_cls_info_on_empty_model():
    result = get_cls_info(EmptyModel)
    assert result == []
