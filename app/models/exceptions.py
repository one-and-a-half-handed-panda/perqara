from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(self, message = "User not found!") -> None:
        super().__init__(detail=message, status_code=status.HTTP_404_NOT_FOUND)