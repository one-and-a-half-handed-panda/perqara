import re
from uuid import UUID

from pydantic import BaseModel, ValidationInfo, field_validator


def is_valid_uuid_v4(v: str) -> bool:
    try:
        UUID(v, version=4)
    except ValueError:
        return False
    else:
        return True


class CreateUserRequest(BaseModel):
    user_name: str
    user_age: int

    @field_validator("user_name")
    @classmethod
    def validate_name(cls, v: str, info: ValidationInfo) -> str:
        assert isinstance(v, str) and re.match("[a-zA-Z ]{2,}$", v), f"{info.field_name} must be a string of at least 2 letters"
        
        return v

    @field_validator("user_age")
    @classmethod
    def validate_age(cls, v: int):
        assert v >= 17, "The user must be at least 17 years old!"
        
        return v


class UpdateUserRequest(BaseModel):
    user_id: str
    user_name: str
    user_age: int

    @field_validator("user_id")
    @classmethod
    def validate_uuid_v4(cls, v: str, info: ValidationInfo):
        assert is_valid_uuid_v4(v), f"{info.field_name} must be a valid UUID v4"
        
        return v

    @field_validator("user_name")
    @classmethod
    def validate_name(cls, v: str, info: ValidationInfo):
        assert isinstance(v, str) and re.match("[a-zA-Z ]{2,}$", v), f"{info.field_name} must be a string of at least 2 letters"
        
        return v

    @field_validator("user_age")
    @classmethod
    def validate_integer(cls, v: int, info: ValidationInfo):
        assert v >= 17, "The user must be at least 17 years old!"
        
        return v