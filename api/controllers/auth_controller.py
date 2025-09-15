from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.models.schemas.user_schemas import CreateUserDTO, LoginDTO
from fastapi.responses import JSONResponse
from api.models.entities.user_entity import UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final
from api.utils.res.response_body import ResponseBody
from api.utils.res.tokens import Tokens
from api.utils.res.responses_http import *
from api.models.schemas.user_schemas import CreateUserDTO
from api.services.providers.provider_user_service import UserServiceProvider
from api.dependencies.service_dependency import *
from datetime import datetime
from api.services.providers.provider_crypto_service import verify_password

router: Final[APIRouter] = APIRouter(prefix="/api/v1/auth", tags=["auth"])

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.get(
    "/{refresh_token}",
    status_code=200,
    response_model=ResponseBody[Tokens],
    responses={
        401: RESPONSE_401,
        404: RESPONSE_404_USER
    }
)
def refresh_token_method(
    refresh_token: str,
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    ):
    
    check_token = jwt_service.decode_token(refresh_token)
    if check_token is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(ResponseBody[None](
                code=status.HTTP_401_UNAUTHORIZED,
                message="You are not authorized",
                status=False,
                body=None,
                datetime = str(datetime.now())
            ))
        )

    user_id: Final[int | None] = jwt_service.extract_user_id(refresh_token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(ResponseBody[None](
                code=status.HTTP_401_UNAUTHORIZED,
                message="You are not authorized",
                status=False,
                body=None,
                datetime = str(datetime.now())
            ))
        )

    user: Final[UserEntity | None] = user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(ResponseBody[None](
                code=status.HTTP_404_NOT_FOUND,
                message="You are not authorized",
                status=False,
                body=None,
                datetime = str(datetime.now())
            ))
        )

    token: Final[str] = jwt_service.create_access_token(user)
    new_refresh_token: Final[str] = jwt_service.create_refresh_token(user)

    user_service.set_refresh_token(new_refresh_token, user)

    tokens: Final[Tokens] = Tokens(token=token, refresh_token=new_refresh_token)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(ResponseBody[dict](
            message="New Tokens sended",
            code=status.HTTP_200_OK,
            status=True,
            body=dict(tokens),
            datetime = str(datetime.now())
        ))
    )


@router.post(
    "/register",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[Tokens],
    description="endpoint to register new user",
    responses={
        409: { "model": ResponseBody[None], "description": "Email already exists" },
        404: RESPONSE_404_USER
    }
    )
def resgiter(
    dto: CreateUserDTO,
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service)
):
    if user_service.exists_by_email(dto.email):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=dict(ResponseBody[None](
                code=status.HTTP_409_CONFLICT,
                message="Email already in use",
                status=False,
                body=None,
                datetime=str(datetime.now())
            ))
        )
    
    user_created: Final[UserEntity] = user_service.create(dto)

    token: Final[str] = jwt_service.create_access_token(user_created)
    refresh_token: Final[str] = jwt_service.create_refresh_token(user_created)

    user_service.set_refresh_token(refresh_token, user_created)

    tokens: Final[Tokens] = Tokens(token=token, refresh_token=refresh_token)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=dict(ResponseBody[dict](
            message="Welcome",
            code=201,
            status=True,
            body=dict(tokens),
            datetime=str(datetime.now())
        ))
    )
    

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[Tokens],
    description="endpoint to login user",
    responses={
        404: RESPONSE_404_USER,
        401: RESPONSE_401
    }
)
def login(
    dto: LoginDTO,
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service)
):
    user: Final[UserEntity] = user_service.get_by_email(dto.email)
    if user is None:
        return JSONResponse(
            status_code=401,
            content=dict(ResponseBody[None](
                code=401,
                message="Login invalid",
                status=False,
                body=None,
                datetime=str(datetime.now())
            ))
        )

    if verify_password(dto.password,user.password) == False :
        return JSONResponse(
            status_code=401,
            content=dict(ResponseBody[None](
                code=401,
                message="Login invalid",
                status=False,
                body=None,
                datetime=str(datetime.now())
            ))
        )

    token: Final[str] = jwt_service.create_access_token(user)
    refresh_token: Final[str] = jwt_service.create_refresh_token(user)

    user_service.set_refresh_token(refresh_token, user)

    tokens: Final[Tokens] = Tokens(token=token, refresh_token=refresh_token)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=dict(ResponseBody[dict](
            message="Welcome again",
            code=status.HTTP_200_OK,
            status=True,
            body=dict(tokens),
            datetime=str(str(datetime.now()))
        ))
    )


@router.get(
    "/revoke",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[None],
    description="endpoint logout of user",
    responses={
        404: RESPONSE_404_USER,
        401: RESPONSE_401
    }
    )
def revoke(
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    token = jwt_service.valid_credentials(credentials)

    user_id: Final[int | None] = jwt_service.extract_user_id(token)
    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=dict(ResponseBody[None](
                code=status.HTTP_401_UNAUTHORIZED,
                message="You are not authorized",
                status=False,
                body=None,
                datetime = str(datetime.now())
            ))
        )

    user: Final[UserEntity | None] = user_service.get_by_id(user_id)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=dict(ResponseBody[None](
                code=status.HTTP_404_NOT_FOUND,
                message="User not found",
                status=False,
                body=None,
                datetime = str(datetime.now())
            ))
        )

    user_service.set_refresh_token("", user)

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(ResponseBody[None](
                code=status.HTTP_200_OK,
                message="Bye Bye",
                status=True,
                body=None,
                datetime = str(datetime.now())
            ))
        )