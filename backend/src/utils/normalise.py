from typing import Any


def _normalise(
    value: Any,
    path: str,
    case_insensitive: list[str],
) -> Any:
    """
    Recursively normalise a value by removing it or transforming it to an adequate form.

    Parameters:
    value: The value to normalise.
    path (str): The path to the current value.
    case_insensitive (list[str]): A list of paths to values that should be none case sensitive (lowercase).

    Returns:
    The normalised value.
    """

    if isinstance(value, dict):
        return _normalise_dict(value, path, case_insensitive)
    if isinstance(value, list):
        return _normalise_list(value, path, case_insensitive)
    if isinstance(value, str):
        return _normalise_string(value, path, case_insensitive)

    return value


def _normalise_list(
    values: list,
    path: str,
    case_insensitive: list[str],
) -> list | None:
    """
    Recursively normalise a list by removing `None` items, empty strings, strings of only
    whitespace, empty dictionaries, empty lists, and sorting the remaining items.

    Parameters:
    values (list): The list to normalise.
    path (str): The path to the current value (list).
    case_insensitive (list[str]): A list of paths to values that should be none case sensitive (lowercase).

    Returns:
    list | None: The normalised list, or `None` if the list is empty.
    """

    values = [
        item
        for item in (_normalise(i, path, case_insensitive) for i in values)
        if item not in ({}, [], None, "")
    ]

    if not values:
        return None

    vtype = type(values[0])
    if not all(isinstance(i, vtype) for i in values):
        return values

    if vtype == str:
        values = [v.lower() for v in values] if path in case_insensitive else values
        return sorted(set(values), key=str.lower)

    if vtype in (int, float, bool):
        return sorted(set(values))

    return values


def _normalise_string(
    s: str,
    path: str,
    case_insensitive: list[str],
) -> str | None:
    """
    Normalise a string by trimming leading and trailing whitespaces.

    Parameters:
    s (str): The string to normalise.

    Returns:
    str | None: The normalised string, or `None` if the string is empty.
    """

    s = s.lower() if path in case_insensitive else s

    return s.strip() or None


def _normalise_dict(
    body: dict | None,
    path: str,
    case_insensitive: list[str],
) -> dict:
    """
    Recursively normalise a dictionary by removing key-value pairs where the value is `None`,
    an empty string, a string of only whitespace, an empty dictionary, or an empty list.

    This function also handles lists, removing `None` items, empty strings, strings of only
    whitespace, empty dictionaries, empty lists, and sorting the remaining items.

    In addition, it trims leading and trailing whitespaces from string values.

    Parameters:
    body (dict | None): The dictionary to normalise.
    path (str): The path to the current value (dict).
    case_insensitive (list[str]): A list of paths to values that should be none case sensitive (lowercase).

    Returns:
    dict: The normalised dictionary.
    """
    if body is None:
        return {}

    return {
        key: normalised_value
        for key, value in body.items()
        if (
            normalised_value := _normalise(
                value,
                path=".".join(filter(None, [path, key])),
                case_insensitive=case_insensitive,
            )
        )
        not in ({}, [], None, "")
    }


def normalise_dict(
    body: dict | None, *, case_insensitive: list[str] | None = None
) -> dict:
    """
    Recursively normalise a dictionary by removing key-value pairs where the value is `None`,
    an empty string, a string of only whitespace, an empty dictionary, or an empty list.

    This function also handles lists, removing `None` items, empty strings, strings of only
    whitespace, empty dictionaries, empty lists, and sorting the remaining items.

    In addition, it trims leading and trailing whitespaces from string values.

    Parameters:
    body (dict | None): The dictionary to normalise.
    case_insensitive (list[str]): A list of paths to values that should be none case sensitive (lowercase).

    Returns:
    dict: The normalised dictionary.
    """
    if case_insensitive is None:
        case_insensitive = []

    return _normalise_dict(body, case_insensitive=case_insensitive, path="")
