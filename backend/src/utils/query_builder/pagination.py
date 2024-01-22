from sqlalchemy.sql import Select, select

from src.core.exceptions import PaginationBuilderException


class PaginatorConfig:
    def __init__(
        self,
        page: int | None = None,
        per_page: int | None = None,
        default_per_page: int = 100,
        max_per_page: int = 100,
    ) -> None:
        """
        Initialize a Paginator instance.

        :param page: Current page number.
        :param per_page: Number of items per page
        :param max_per_page: Maximum number of items allowed per page, defaults to 100
        """
        self.max_per_page = max_per_page
        self.per_page = per_page
        self.page = page

        # If neither page nor per_page are provided, set them to defaults
        if page is None and per_page is None:
            self.set_page(1)
            self.set_per_page(default_per_page)
        else:
            self.set_page(page or 1)
            self.set_per_page(per_page or max_per_page)

        self.offset = (self.page - 1) * self.per_page

    def set_page(self, page: int) -> None:
        """
        Set page value ensuring it is a positive integer.

        :param page: Desired page number
        """
        if page < 1 or not isinstance(page, int):
            raise PaginationBuilderException("Page value must be a positive integer.")

        self.page = page

    def set_per_page(self, per_page: int) -> None:
        """
        Set per_page value while ensuring it doesn't exceed the maximum allowed and is a positive integer.

        :param per_page: Desired number of items per page
        """
        if per_page < 1 or not isinstance(per_page, int):
            raise PaginationBuilderException("Per page value must be a positive integer.")

        if per_page > self.max_per_page:
            self.per_page = self.max_per_page
        else:
            self.per_page = per_page


class PaginationQueryBuilder:
    def __init__(self, config: PaginatorConfig):
        """
        Initialize a Pagination instance.
        """
        self.config = config

    def build(self, stmt: select) -> Select:
        """
        Apply pagination to the query.

        :return: Modified query with limit and offset applied
        """
        return stmt.offset(self.config.offset).limit(self.config.per_page)
