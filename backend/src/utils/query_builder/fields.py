from sqlalchemy.orm import DeclarativeBase

from src.core.exceptions import QueryBuilderException


class FieldParser:
    def __init__(self, model_cls: DeclarativeBase, field_name: str):
        self.model_cls = model_cls
        self.full_field_name = field_name

        # Split and store the path and name for easier access later
        self.path = self.full_field_name.split("::")[0].split(".")
        self.name = self.path[0]

    @property
    def field(self):
        """Fetch the field based on the model class and name."""
        if not hasattr(self, "_field"):
            try:
                self._field = getattr(self.model_cls, self.name)  # noqa
            except AttributeError:
                raise QueryBuilderException(
                    f"Couldn't find `{self.full_field_name}` - INVALID FIELD"
                )

        return self._field

    def _find_type(self):
        """Find the type of the field within the model."""
        if (
            hasattr(self.model_cls, "__table__")
            and self.name in self.model_cls.__table__.c
        ):
            return self.model_cls.__table__.c[self.name].type

        return None
