from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationInfo, field_validator


def is_valid_http_status_code(v: str):
    try:
        int(v)

        if len(v) == 3:
            return True
        else:
            return False
    except ValueError:
        return False
    

def is_valid_timestamp(v: str):
    try:
        datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False
    else:
        return True


class DefaultSuccessResponse(BaseModel):
    success: bool = True
    code: str = "200"
    message: str = "OK"
    data: Optional[dict]

    @field_validator("success")
    @classmethod
    def validate_success(cls, v: bool, info: ValidationInfo):
        assert v, f"{info.field_name} must be True"
        
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str, info: ValidationInfo):
        assert is_valid_http_status_code(v), f"{info.field_name} must be 3 digits integer"
        
        return v


class DefaultListResponse(BaseModel):
    success: bool = True
    code: str = "200"
    message: str = "OK"
    data: Optional[list[dict]]

    @field_validator("success")
    @classmethod
    def validate_success(cls, v: bool, info: ValidationInfo):
        assert v, f"{info.field_name} must be True"
        
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str, info: ValidationInfo):
        assert is_valid_http_status_code(v), f"{info.field_name} must be 3 digits integer"
        
        return v


class DefaultErrorResponse(BaseModel):
    success: bool = False
    code: str
    message: str
    timestamp: str

    @field_validator("success")
    @classmethod
    def validate_success(cls, v: bool, info: ValidationInfo):
        assert v, f"{info.field_name} must be True"
        
        return v

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str, info: ValidationInfo):
        assert is_valid_http_status_code(v), f"{info.field_name} must be 3 digits integer"
        
        return v

    @field_validator("timestamp")
    @classmethod
    def validate_timestamp(cls, v: str, info: ValidationInfo):
        assert is_valid_timestamp(v), f"{info.field_name} must be a valid timestamp with 'yyyy-mm-dd HH:ii:ss' format"
        
        return v
    
    def to_json(self):
        return {
            "code": self.code,
            "message": self.message,
            "timestamp": self.timestamp,
        }