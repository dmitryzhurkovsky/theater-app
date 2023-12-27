from src.core.database.utils.repository import AbstractRepository


class BaseService:
    def __init__(self, repository: type[AbstractRepository]):
        self.repository: AbstractRepository = repository()
