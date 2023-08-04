from http import HTTPStatus


class ApiError(Exception):
    def __init__(self, status_code, message):
        super().__init__()
        self.status_code = status_code
        self.message = message


class NotFound(ApiError):
    def __init__(self, message):
        super().__init__(HTTPStatus.NOT_FOUND, message)


class BadRequest(ApiError):
    def __init__(self, message):
        super().__init__(HTTPStatus.BAD_REQUEST, message)


class InternalServerError(ApiError):
    def __init__(self, message):
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, message)
