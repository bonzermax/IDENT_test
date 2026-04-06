from datetime import date

from sqlalchemy import String, Date, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from task_1 import Base, IdMixin

"""Вариант №2"""

class Patient(Base):
    """Таблица пациентов"""

    med_card_num: Mapped[str] = mapped_column(String, nullable=False)

class Person(IdMixin, Base):
    """Таблица персон"""

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String)

class Employee(Base):
    """Таблица работников"""

    person_id: Mapped[UUID] = mapped_column(ForeignKey('Person.id'), nullable=False)

    inn: Mapped[str] = mapped_column(String, nullable=False)

