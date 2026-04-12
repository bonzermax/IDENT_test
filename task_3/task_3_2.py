from sqlite3 import DatabaseError
from typing import Any, Self
from urllib.request import Request
from fastapi.params import Depends
from pydantic import BaseModel, Field
from pydantic.config import ExtraValues
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated
from starlette.responses import JSONResponse

from task_3.task_3_1 import UserRepository, get_session


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserCreateSchema(BaseModel):
    # Валидируем, что в поле телефон попадёт только то, что похоже на телефон
    phone: str = Field(pattern=r"^\+?\d{10,15}$")
    name: str = Field(min_length=2, max_length=100)


class UserService:
    """Сервисной слой для работы с пользователями"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_by_phone(self, phone):
        user = await self.user_repo.get_user_by_phone(phone)

        if user is None:
            raise UserNotFoundError("Пользователь не найден")

        return user

    async def register_user(self, user):
        user_exist = await self.user_repo.get_user_by_phone(user.phone)

        if user_exist:
            raise UserAlreadyExistsError("Пользователь уже существует")

        return self.user_repo.create_user(user)

def get_user_repo(
    session: AsyncSession = Annotated[AsyncSession, Depends(get_session)]
) -> UserRepository:
    return UserRepository(session, UserORM)

def get_user_service(
    repo: UserRepository = Annotated[UserRepository, Depends(get_user_repo)]
) -> UserService:
    return UserService(repo)

@app.exception_handler(UserNotFoundError)
async def database_error_handler(
    request: Request,
    exception: UserNotFoundError,
):
    # логируем ошибку, если требуется и возвращаем статус код
    return JSONResponse(
        status_code=404,
        content={"detail": "Пользователь не найден"},
    )


@app.exception_handler(UserAlreadyExistsError)
async def user_exist_handler(
    request: Request,
    exception: UserAlreadyExistsError,
):
    # логируем ошибку и возвращаем статус код
    return JSONResponse(
        status_code=409,
        content={"detail": "Пользователь уже существует"},
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(
    request: Request,
    exception: DatabaseError,
):
    # логируем ошибку БД и возвращаем статус код
    return JSONResponse(
        status_code=500,
        content={"detail": "Ошибка на стороне сервера"},
    )


@user_router.post(
    "/register", response_model=UserCreateSchema
)  # Отдельный роутер для работы с пользователями
async def register_patient(
    user: UserCreateSchema,
    service: UserService = Annotated[UserService, Depends(get_user_service)],
) -> UserCreateSchema:
    return await service.register_user(user=user)
