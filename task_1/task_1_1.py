from datetime import date, datetime

from sqlalchemy import String, Date, UUID, ForeignKey, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
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

class Visit(IdMixin, Base):
    """Таблица посещений"""

    patient_id: Mapped[UUID] = mapped_column(ForeignKey('Patient.id'), nullable=False)
    employee_id: Mapped[UUID] = mapped_column(ForeignKey('Employee.id'), nullable=False)

    visit_datetime: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())
