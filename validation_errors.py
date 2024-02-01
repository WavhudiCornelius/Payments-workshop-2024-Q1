from enum import Enum

class ValidationError(Enum):
    # Name and Surname Errors
    ERR_NAME_ALPHA = "Name and surname must contain only alphabetic characters."
    ERR_NAME_SPECIAL_CHAR = "Name and surname must not contain special characters."

    # Email Errors
    ERR_EMAIL_INVALID = "Email address is invalid."

    # Age Errors
    ERR_AGE_NEG = "Age must not be negative."
    ERR_AGE_UNDER = "Age must be numeric."
    ERR_AGE_TOO_OLD = "Age must not be higher than 150."
    ERR_AGE_TOO_YOUNG = "Age must not be younger than 18."
