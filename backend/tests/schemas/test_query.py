from src.core.schemas import QueryParameters


def test_query_parameters():
    sort = "id:desc,name:asc,two_values:desc,one_value"
    page = 100
    per_page = 21
    params = QueryParameters(sort=sort, page=page, per_page=per_page)

    assert params.sort[0].field == "id"
    assert params.sort[0].order == "desc"

    assert params.sort[1].field == "name"
    assert params.sort[1].order == "asc"

    assert params.sort[2].field == "two_values"
    assert params.sort[2].order == "desc"

    assert params.sort[3].field == "one_value"
    assert params.sort[3].order == "asc"


def test_default_query_parameters():
    params = QueryParameters()
    assert params.sort == []
    assert params.page is None
    assert params.per_page is None


def test_default_single_sort_query():
    params = QueryParameters(sort="id")
    assert params.sort[0].field == "id"
