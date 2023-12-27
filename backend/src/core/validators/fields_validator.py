import re

from fastapi import HTTPException

LETTER_MATCH_VALIDATOR = re.compile(r"^[a-zA-Z\-]+$")


# TODO Maxim Suprun. Why do we use this?
def validate_field(field):
    if not LETTER_MATCH_VALIDATOR.match(field):
        raise HTTPException(
            status_code=422, detail="First and last names should contains only letters"
        )
    return field
