from fastapi import HTTPException, status


class HTTPExceptions():

    @staticmethod
    def not_found(detail):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)

    @staticmethod
    def forbidden(detail):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=detail)
