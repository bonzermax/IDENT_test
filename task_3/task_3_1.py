from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from task_3.task_3_2 import UserCreateSchema

T = TypeVar("T")

engine = create_async_engine()

async def get_session():
    async with async_sessionmaker(engine) as session:
        yield session

class DatabaseError(Exception):
    pass


class AbstractRepository(Generic[T], ABC):
    """Абстрактный репозиторий, чтобы наследоваться при появлении других типов БД"""

    @abstractmethod
    def get_all(self) -> list[T]:
        pass


class SQLAlchemyRepository(AbstractRepository[T]):
    """Базовый класс для SQLAlchemy репозиториев"""

    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    # Можно реализовать общий метод и тогда у всех унаследованных классов уже будет реализован get_all()
    # по аналогии можно реализовать get_by_id, update и т.п.
    async def get_all(self) -> list[T]:
        try:
            stmt = select(self.model)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            # logger.error(
            #     f"Ошибка получения данных из БД ({self.__class__.__name__}) в get_all: {e}"
            # ) Можно залогировать ошибку получения данных, но имеет смысл обработать её в exception_handler и там уже записать в логи
            raise DatabaseError("Ошибка получения данных из БД") from e


class PatientRepository(SQLAlchemyRepository):
    """Репозиторий пациентов"""

    pass


# patient_repo = PatientRepository(session=session, model=PatientORM)
# print(patient_repo.get_all()) - получим список всех пациентов


class UserRepository(SQLAlchemyRepository):
    """Репозиторий пользователей"""

    async def get_user_by_phone(self, phone: str) -> UserORM | None:
        try:
            stmt = select(self.model).where(self.model.phone == phone)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            # logger.error(f"Ошибка при получение данных из БД: {e}") Аналогично, как
            raise DatabaseError("Ошибка получения пользователя") from e

    async def create_user(self, data: UserCreateSchema) -> UserORM:
        try:
            user = self.model(**data)
            self.session.add(user)
            await self.session.commit()
            return user
        except SQLAlchemyError as e:
            # logger.error(f"Ошибка добавления пользователя: {e}") Аналогично, как
            raise DatabaseError("Ошибка добавления пользователя") from e
