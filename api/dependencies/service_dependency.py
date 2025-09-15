from sqlalchemy.orm import Session
from fastapi import Depends
from api.configs.db.database import get_db
from api.repositories.providers.provider_user_repository import UserRepositoryProvider
from api.services.providers.provider_user_service import UserServiceProvider
from api.services.providers.provider_jwt_service import JwtServiceProvider
from api.services.base.base_jwt_service import BaseJwtService
from typing import Final

def get_user_provider_dependency(db: Session = Depends(get_db)) -> UserServiceProvider:
    repository: Final = UserRepositoryProvider(db)
    return UserServiceProvider(repository)

def get_jwt_service() -> BaseJwtService:
    return JwtServiceProvider()