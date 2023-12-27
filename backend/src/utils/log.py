import json


def prettify(log_entry: dict) -> dict:
    return {
        "pretty_format": log_entry,
        **{
            k: json.dumps(v or {}, sort_keys=True, separators=(",", ":"))
            for k, v in log_entry.items()
        },
    }
