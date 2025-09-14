from api.repositories.base.base_user_repository import BaseUserRepository


class UserRepositoryProdiver(BaseUserRepository):
    def __init__(self, db):
        self.db = db