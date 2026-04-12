from datetime import date, datetime

from sqlalchemy import String, Date, Boolean, UUID, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import mapped_column, Mapped

from task_1 import Base, IdMixin

"""Вариант №3"""

class Person(IdMixin, Base):
    """Таблица персон"""

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String)
    inn: Mapped[str] = mapped_column(String, nullable=True)
    med_card_num: Mapped[str] = mapped_column(String, nullable=True)
    is_patient: Mapped[bool] = mapped_column(Boolean)
    is_employee: Mapped[bool] = mapped_column(Boolean)


class Visit(IdMixin, Base):
    """Таблица посещений"""

    patient_id: Mapped[UUID] = mapped_column(ForeignKey('Persons.id'), nullable=False)
    employee_id: Mapped[UUID] = mapped_column(ForeignKey('Persons.id'), nullable=False)

    visit_datetime: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())