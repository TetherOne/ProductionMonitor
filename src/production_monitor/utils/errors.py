from typing import Any

from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DEFAULT_DETAIL = "Server error"

    def __init__(self, detail: str | None = None, **kwargs: dict[str, Any]) -> None:
        super().__init__(
            status_code=self.STATUS_CODE,
            detail=detail or self.DEFAULT_DETAIL,
            **kwargs,
        )


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DEFAULT_DETAIL = "Not found"
