from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import models
import schemas
import service
from db import get_db
from utils import create_access_token, create_refresh_token, get_jwt_identity

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login/")
user_router = APIRouter()
app_router = APIRouter()


def get_user_by_token(token=Depends(oauth2_scheme)) -> models.User:
    db_session = next(get_db())

    def raise_401_exception(detail: str = "Недостаточно прав."):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        username = get_jwt_identity(token)
        if username is None:
            raise_401_exception()
    except ExpiredSignatureError:
        raise_401_exception(
            "Истек срок действия данных для входа. Пожалуйста, войдите снова."
        )
    except Exception:
        raise_401_exception()

    return service.get_user_by_username(db_session, username)


@app_router.get("/health/", status_code=status.HTTP_200_OK)
def read_item():
    return {"status": "OK"}


@user_router.post("/register/", summary="register user")
def register_user(register_dto: schemas.RegisterUserDto, db: Session = Depends(get_db)):
    """
    Регистрация пользователя:

    - **username**: логин
    - **first_name**: имя
    - **last_name**: фамилия
    - **email**: email
    - **password**: Пароль
    """
    # forwarded_for, user_agent = get_auth_headers()
    user = service.register_user(db, register_dto)
    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)
    data = schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
    return data


@user_router.post("/login/", summary="login user")
def login_user(login_dto: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Авторизация пользователя:

    - **username**: логин
    - **password**: пароль
    """

    # forwarded_for, user_agent = get_auth_headers()
    user = service.verify_user(db, schemas.LoginDto(username=login_dto.username, password=login_dto.password))
    access_token = create_access_token(user.username)
    refresh_token = create_refresh_token(user.username)
    data = schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
    return data


@user_router.post("/refresh/", summary="refresh user token")
def get_user_refresh_token(current_user=Depends(get_user_by_token)):
    return create_access_token(current_user.username)


@user_router.get("/signin/", summary="signin user")
def signin():
    return {"message": "Please go to login and provide Login/Password"}


@user_router.get(
    "/auth/",
    summary="auth user",
)
def get_user(
        db: Session = Depends(get_db),
        current_user=Depends(get_user_by_token)
):
    """
    Аутентификация пользователя:
    """

    headers = {
        "X-UserId": str(current_user.id),
        "X-Username": current_user.username,
        "X-Email": current_user.email,
        "X-First-Name": current_user.first_name,
        "X-Last-Name": current_user.last_name,
    }

    return JSONResponse(content={"status": "OK"}, headers=headers)


api_router = APIRouter()

api_router.include_router(user_router, prefix="/user", tags=["user"])
api_router.include_router(app_router, prefix="/app", tags=["app"])
