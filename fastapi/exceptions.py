from fastapi import HTTPException, status


class TitleException(Exception):
    def __init__(self, name: str):
        self.name = name


class HttpExceptions():

    @staticmethod
    def user_not_found(detail):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)
