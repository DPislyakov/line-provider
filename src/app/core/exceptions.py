from typing import Union

from fastapi import HTTPException


class ApplicationError(HTTPException):
    status_code = 500

    def __init__(self, status_code: Union[int, None] = None, *args, **kwargs):
        super(ApplicationError, self).__init__(status_code=status_code or self.status_code, *args, **kwargs)


class UnauthorizedError(ApplicationError):
    status_code = 401


class AccessDeniedError(ApplicationError):
    status_code = 403


class NotFoundError(ApplicationError):
    status_code = 404


class AlreadyExistsError(ApplicationError):
    status_code = 409


class InvalidDataError(ApplicationError):
    status_code = 422
