from datetime import date

from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped

from task_1 import Base, IdMixin

"""Вариант №1"""

class Patient(IdMixin, Base):
    """Таблица пациентов"""

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String)
    med_card_num: Mapped[str] = mapped_column(String, nullable=False)

class Employee(IdMixin, Base):
    """Таблица работников"""

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String)
    inn: Mapped[str] = mapped_column(String, nullable=False)

