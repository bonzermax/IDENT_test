from datetime import date, datetime

from sqlalchemy import String, Date, UUID, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from task_1 import Base, IdMixin

"""Вариант №2"""

class Patient(Base):
    """Таблица пациентов"""
    person_id: Mapped[UUID] = mapped_column(ForeignKey('Person.id'), nullable=False, primary_key=True)

    med_card_num: Mapped[str] = mapped_column(String, nullable=False)

    person: Mapped["Person"] = relationship(back_populates="patients")

class Person(IdMixin, Base):
    """Таблица персон"""

    full_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String)

    patients: Mapped["Patient"] = relationship(back_populates='persons')
    employee: Mapped["Employee"] = relationship(back_populates='persons')

class Employee(Base):
    """Таблица работников"""

    person_id: Mapped[UUID] = mapped_column(ForeignKey('Persons.id'), nullable=False, primary_key=True)

    inn: Mapped[str] = mapped_column(String, nullable=False)

    person: Mapped["Person"] = relationship(back_populates="employees")


class Visit(IdMixin, Base):
    """Таблица посещений"""

    patient_id: Mapped[UUID] = mapped_column(ForeignKey('Patients.person_id'), nullable=False)
    employee_id: Mapped[UUID] = mapped_column(ForeignKey('Employees.person_id'), nullable=False)

    visit_datetime: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())