from sqlalchemy.sql import Select

from src.utils.query_builder.fields import FieldParser


class OnlyFieldsQueryBuilder:
    def __init__(self, model, fields: list[str]) -> None:
        self.model = model
        self.fields = fields

    def build(self, stmt: Select) -> Select:
        only_fields = []

        for field in self.fields:
            field_parser = FieldParser(self.model, field)
            only_fields.append(field_parser.field)

        return stmt.with_only_columns(*only_fields) if only_fields else stmt
