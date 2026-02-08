class CustomException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: str,
        exception_type: str,
        additional_info: dict | None = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.exception_type = exception_type
        self.additional_info = additional_info or {}
