from typing import Optional, Sequence, Union
from uuid import UUID

from pydantic import BaseModel
from pydantic_core import PydanticUndefinedType

from task_4.task_4_print import print_models_info


class NotBaseModelSubclass(Exception):
    pass


class Task(BaseModel):
    id: int = 1
    name: str = None
    fio: Optional[str]
    key_id: UUID
    stmt: None
    stmt2: Union[str, int]


class Task2(BaseModel):
    ids: int = 1
    name: str = None
    fio: Optional[str]
    key_id: UUID
    stmt: None
    stmt2: Union[str, int]


class Task3(BaseModel):
    id: int = 1
    name: str = None
    fio: Optional[dict]
    key_id: UUID
    stmt: None
    stmt2: Union[str, dict]


def check_all_are_basemodel(_models: set) -> bool:
    """Проверка, что все модели наследуются от BaseModel"""
    for m in _models:
        if not issubclass(m, BaseModel):
            raise NotBaseModelSubclass(f"{m.__name__} не наследуется от BaseModel")
    return True


def format_annotation(annotation) -> str:
    """Приведение аннотации поля к строке и удаление лишней информации"""
    if isinstance(annotation, type):
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def get_cls_info(_model: type[BaseModel]) -> list:
    """Формирование списка с информацией о полях класса"""
    class_info = []

    model_fields = _model.model_fields
    model_annotations = _model.__annotations__

    for key, value in model_fields.items():
        field_annotation = model_annotations.get(key)
        field_default = (
            value.default
            if value and not isinstance(value.default, PydanticUndefinedType)
            else "-"
        )

        row = (key, format_annotation(field_annotation), str(field_default))
        class_info.append(row)

    return class_info


def process_user_models(_models: set):
    """Обработка классов"""
    check_all_are_basemodel(_models)

    models_info = dict()
    for model in _models:
        cls_info = get_cls_info(model)
        models_info[model.__name__] = cls_info

    print_models_info(models_info)


if __name__ == "__main__":
    user_models = {
        Task,
        Task2,
        Task3,
    }  # set, чтобы дубли не выводились, даже если они попадут

    if user_models:
        process_user_models(user_models)
