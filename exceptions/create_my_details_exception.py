from exceptions.custome_exception import CustomException


class NameNotFound(CustomException):
    def __init__(self, name: str):
        super().__init__(
            status_code=404,
            detail=f"Name '{name}' was not found",
            exception_type="NameNotFound",
            additional_info={
                "name": name
            }
        )


class AgeNotFound(CustomException):
    def __init__(self, age: int):
        super().__init__(
            status_code=404,
            detail=f"Age '{age}' was not found",
            exception_type="AgeNotFound",
            additional_info={
                "age": age
            }
        )


class AddressNotFound(CustomException):
    def __init__(self, address: str):
        super().__init__(
            status_code=404,
            detail=f"Address '{address}' was not found",
            exception_type="AddressNotFound",
            additional_info={
                "address": address
            }
        )
