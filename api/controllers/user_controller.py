from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.models.entities.user_entity import UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final, Any
from api.utils.res.response_body import ResponseBody
from api.utils.res.responses_http import *
from api.models.schemas.user_schemas import UserOUT, UpdateUserDTO
from api.services.providers.provider_user_service import UserServiceProvider
from api.dependencies.service_dependency import *
from datetime import datetime

router: Final[APIRouter] = APIRouter(prefix="/api/v1/user", tags=["User"])

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.put(
    "",
    description="Endpoint to update user",
    response_model=ResponseBody[UserOUT],
    status_code=status.HTTP_200_OK,
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    },
)
def update(
    dto: UpdateUserDTO,
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ):
    
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

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

        user_updated: Final[UserEntity] = user_service.update(user,dto)

        user_out: Final[UserOUT] = user_updated.to_user_out()

        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody[dict](
                    code=status.HTTP_200_OK,
                    message="User updated with successfully",
                    status=True,
                    body=dict(user_out),
                    datetime = str(datetime.now())
                ))
            )        

    except Exception as e:
        return JSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    datetime = str(datetime.now())
                ))
            )

@router.delete(
    '',
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[None],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def delete(
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

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

        user_service.delete(user)
        
        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody[None](
                    code=status.HTTP_200_OK,
                    message="See you later",
                    status=True,
                    body=None,
                    datetime = str(datetime.now())
                ))
            )        

    except Exception as e:
        return JSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    datetime = str(datetime.now())
                ))
            )

@router.get(
    '',
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[UserOUT],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def get_me(
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

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

        user_out: Final[UserOUT] = user.to_user_out()

        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody[dict](
                    code=status.HTTP_200_OK,
                    message="User found with successfully",
                    status=True,
                    body=dict(user_out),
                    datetime = str(datetime.now())
                ))
            )        

    except Exception as e:
        return JSONResponse(
                status_code=500,
                content=dict(ResponseBody[Any](
                    code=500,
                    message="Error in server! Please try again later",
                    status=False,
                    body=str(e),
                    datetime = str(datetime.now())
                ))
            )