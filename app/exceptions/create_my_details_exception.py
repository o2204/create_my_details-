from exceptions.custome_exception import CustomException


class NameNotFound(CustomException):
    def __init__(self, name: str):
        super().__init__(
            exception_type="NameNotFound",
            additional_info={
                "name": name
            }
        )


class AgeNotFound(CustomException):
    def __init__(self, age: int):
        super().__init__(
            detail=f"Age '{age}' was not found",
            exception_type="AgeNotFound",
            additional_info={
                "age": age
            }
        )


class AddressNotFound(CustomException):
    def __init__(self, add: str):
        super().__init__(
            exception_type="AddressNotFound",
            additional_info={
                "address": add
            }
        )
