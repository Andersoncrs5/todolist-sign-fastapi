from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from api.models.entities.user_entity import UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Final, Any
from api.utils.res.response_body import ResponseBody
from api.utils.res.responses_http import *
from api.models.schemas.task_schemas import UpdateTaskDTO, CreateTaskDTO, TaskOUT
from api.services.providers.provider_user_service import UserServiceProvider
from api.dependencies.service_dependency import *
from datetime import datetime
from api.utils.filters.task_filter import TaskFilter
from fastapi_pagination import Page, add_pagination, paginate
from api.models.entities.task_entity import TaskEntity

router: Final[APIRouter] = APIRouter(prefix="/api/v1/task", tags=["Task"])

bearer_scheme: Final[HTTPBearer] = HTTPBearer()

@router.put(
    "/{task_id}/toggle/status/is_done",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[TaskOUT],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def change_status_done(
    task_id: int,
    task_service: TaskServiceProvider = Depends(get_task_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id = jwt_service.extract_user_id(token)
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

        if task_id <= 0 or task_id is None:
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_400_BAD_REQUEST,
                        message="Task Id is required",
                        status=False,
                        body=None,
                        datetime = str(datetime.now())
                    ))
                )

        task: Final[TaskEntity | None] = task_service.get_by_id(task_id)
        if task is None:
            return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_404_NOT_FOUND,
                        message="Task not found",
                        status=False,
                        body=None,
                        datetime = str(datetime.now())
                    ))
                )

        if user_id == task.user_id:
            return JSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="You are not authorized to change status done this task",
                    status=False,
                    body=None,
                    datetime = str(datetime.now())
                ))
            )

        task_changed: Final[TaskEntity] = task_service.change_status_done(task)
        task_out: Final[TaskOUT] = task_changed.to_task_out()

        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody[TaskOUT](
                    code=status.HTTP_200_OK,
                    message="Task status changed with successfully",
                    status=True,
                    body=task_out,
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
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[None],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def delete_task(
    task_id: int,
    task_service: TaskServiceProvider = Depends(get_task_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id = jwt_service.extract_user_id(token)
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

        if task_id <= 0 or task_id is None:
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_400_BAD_REQUEST,
                        message="Task Id is required",
                        status=False,
                        body=None,
                        datetime = str(datetime.now())
                    ))
                )

        task: Final[TaskEntity | None] = task_service.get_by_id(task_id)
        if task is None:
            return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_404_NOT_FOUND,
                        message="Task not found",
                        status=False,
                        body=None,
                        datetime = str(datetime.now())
                    ))
                )

        if user_id == task.user_id:
            return JSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="You are not authorized to delete this task",
                    status=False,
                    body=None,
                    datetime = str(datetime.now())
                ))
            )

        task_service.delete(task)

        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody[None](
                    code=status.HTTP_200_OK,
                    message="Task deleted with successfully",
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
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBody[TaskOUT],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def get_task(
    task_id: int,
    task_service: TaskServiceProvider = Depends(get_task_provider_dependency),
    jwt_service: BaseJwtService = Depends(get_jwt_service),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        token: Final[str] = jwt_service.valid_credentials(credentials)

        user_id = jwt_service.extract_user_id(token)
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

        if task_id <= 0 or task_id is None:
            return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_400_BAD_REQUEST,
                        message="Task Id is required",
                        status=False,
                        body=None,
                        datetime = str(datetime.now())
                    ))
                )

        task: Final[TaskEntity | None] = task_service.get_by_id(task_id)
        if task is None:
            return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=dict(ResponseBody[None](
                        code=status.HTTP_404_NOT_FOUND,
                        message="Task not found",
                        status=False,
                        body=None,
                        datetime = str(datetime.now())
                    ))
                )

        if user_id == task.user_id:
            return JSONResponse(
                status_code=409,
                content=dict(ResponseBody[None](
                    code=409,
                    message="You are not authorized to read this task",
                    status=False,
                    body=None,
                    datetime = str(datetime.now())
                ))
            )

        task_out: Final[TaskOUT] = task.to_task_out()

        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=dict(ResponseBody[dict](
                    code=status.HTTP_200_OK,
                    message="Task found with successfully",
                    status=True,
                    body=dict(task_out),
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
    "",
    status_code=status.HTTP_200_OK,
    response_model=Page[TaskOUT],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def get_all(
    task_filter: TaskFilter = Depends(),
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    task_service: TaskServiceProvider = Depends(get_task_provider_dependency),
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

        tasks: Final = task_service.get_all_user_id_filtered(user_id, task_filter)

        return paginate(tasks)

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

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBody[TaskOUT],
    responses = {
        401: RESPONSE_401,
        404: RESPONSE_404_USER,
        500: RESPONSE_500,
    }
)
def create(
    dto: CreateTaskDTO,
    user_service: UserServiceProvider = Depends(get_user_provider_dependency),
    task_service: TaskServiceProvider = Depends(get_task_provider_dependency),
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

        task: Final = task_service.create(user, dto)

        task_mapped: Final[TaskOUT] = task.to_task_out()

        return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=dict(ResponseBody[dict](
                    code=status.HTTP_201_CREATED,
                    message="Task created with successfully",
                    status=True,
                    body=dict(task_mapped),
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

add_pagination(router)