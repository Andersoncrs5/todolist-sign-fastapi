from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.models.schemas.user_schemas import CreateUserDTO, LoginDTO
from fastapi.responses import JSONResponse
from api.models.entities.user_entity import UserEntity
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

bearer_scheme = HTTPBearer()

