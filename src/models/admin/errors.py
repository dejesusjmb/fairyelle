class AdminError(Exception):
    def __init__(self, message):
        self.message = message


class IncorrectPasswordError(AdminError):
    pass


class InvalidEmailError(AdminError):
    pass
