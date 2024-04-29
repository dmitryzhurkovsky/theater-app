from src.core.enums.base import BaseEnum


class StatusTypeEnum(BaseEnum):
    PENDING = "pending"
    ACTOR_APPROVED = "actor_approved"
    DIRECTOR_APPROVED = "director_approved"
    REJECTED = "rejected"
