from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

T = TypeVar('T')

class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    def get_all(self) -> list[T]:
        pass

class SQLAlchemyRepository(AbstractRepository[T]):
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
            logger.error(f'Ошибка при получение данных из БД: {e}')
            return []

class PatientRepository(SQLAlchemyRepository):
    pass

