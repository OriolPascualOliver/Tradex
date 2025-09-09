class EmailNotValidError(ValueError):
    pass


def validate_email(email, *args, **kwargs):
    return type("Email", (), {"email": email, "normalized": email})


__version__ = "2.0.0"
