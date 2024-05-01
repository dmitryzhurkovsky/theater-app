from src.core.enums.base import BaseEnum


class StatusTypeEnum(BaseEnum):
    PENDING = "Pending"
    ACTOR_APPROVED = "Actor approved"
    DIRECTOR_APPROVED = "Director approved"
    REJECTED = "Rejected"
