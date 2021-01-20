class APIException(Exception):
    def __init__(self, message: str = None, code: int = 400):
        self.code = code
        self.message = message
