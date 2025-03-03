import orjson


def prettify(log_entry: dict) -> dict:
    return {
        "pretty_format": log_entry,
        **{k: orjson.dumps(v or {}, option=orjson.OPT_SORT_KEYS).decode("utf-8") for k, v in log_entry.items()},
    }
