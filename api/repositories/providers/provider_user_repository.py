from sqlalchemy.orm import Session
from datetime import datetime
from api.repositories.base.base_user_repository import BaseUserRepository
from api.models.entities.user_entity import UserEntity

class UserRepositoryProvider(BaseUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> (UserEntity | None):
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()

    def exists_by_email(self, email: str) -> bool:
        return self.db.query(UserEntity).filter(UserEntity.email == email).count() >= 1

    def get_by_id(self, id: int) -> (UserEntity | None):
        return self.db.query(UserEntity).filter(UserEntity.id == id).first()
    
    def create(self, user: UserEntity) -> UserEntity:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def delete(self, user: UserEntity):
        self.db.delete(user)
        self.db.commit()

    def refresh_token(self, refresh_token: str, user: UserEntity) -> UserEntity:
        user.refresh_token = refresh_token

        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user) -> UserEntity:
        user.updated_at = datetime.now()
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def save(self, user: UserEntity) -> UserEntity:
        self.db.commit()
        self.db.refresh(user)

        return user