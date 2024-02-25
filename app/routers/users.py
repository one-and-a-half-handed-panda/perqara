import traceback
from datetime import datetime

from accessors.users import User, UserAccessor
from database import get_db_session
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models.exceptions import UserNotFoundException
from models.requests import (
    CreateUserRequest,
    UpdateUserRequest,
    is_valid_uuid_v4,
)
from models.responses import (
    DefaultErrorResponse,
    DefaultListResponse,
    DefaultSuccessResponse,
)
from pydantic_core import ValidationError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/users")
def create_user(request: CreateUserRequest, db: Session = Depends(get_db_session)):
    try:
        new_user: User = UserAccessor(db).insert_user(
            user_name=request.user_name,
            user_age=request.user_age
        )
        db.commit()
    except ValidationError:
        db.rollback()
        return DefaultErrorResponse(
            code='422',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
    except Exception:
        db.rollback()
        return DefaultErrorResponse(
            code='500',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    return DefaultSuccessResponse(data={
        "user_id": new_user.id,
        "user_name": new_user.name,
        "user_age": new_user.age,
    })


@router.get("/users")
def get_users(db: Session = Depends(get_db_session)):
    try:
        users: list[User] = UserAccessor(db).select_all_users()

        response_data = []
        for user in users:
            response_data.append({
                "user_id": user.id,
                "user_name": user.name,
                "user_age": user.age,
            })
    except Exception:
        return DefaultErrorResponse(
            code='500',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    return DefaultListResponse(data=response_data)


@router.get("/users/{user_id}")
def get_user_by_id(user_id: str, db: Session = Depends(get_db_session)):
    try:
        if not is_valid_uuid_v4(user_id):
            raise ValidationError("user_id must be a valid UUID v4!")

        user: User = UserAccessor(db).select_user_by_id(user_id=user_id)
    except UserNotFoundException as e:
        return JSONResponse(DefaultErrorResponse(
            code=str(e.status_code),
            message=e.detail,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ).to_json(), status_code=e.status_code)
    except ValidationError:
        return DefaultErrorResponse(
            code='422',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
    except Exception:
        return DefaultErrorResponse(
            code='500',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    return DefaultSuccessResponse(data={
        "user_id": user.id,
        "user_name": user.name,
        "user_age": user.age,
    })


@router.put("/users/{user_id}")
def update_user(request: UpdateUserRequest, db: Session = Depends(get_db_session)):
    try:
        selected_user = User()
        selected_user.id = request.user_id
        selected_user.age = request.user_age
        selected_user.name = request.user_name

        updated_user: User = UserAccessor(db).update_user_by_id(selected_user)
        db.commit()
    except UserNotFoundException as e:
        return JSONResponse(DefaultErrorResponse(
            code=str(e.status_code),
            message=e.detail,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ).to_json(), status_code=e.status_code)
    except ValidationError:
        db.rollback()
        return DefaultErrorResponse(
            code='422',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
    except Exception:
        db.rollback()
        return DefaultErrorResponse(
            code='500',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    return DefaultSuccessResponse(data={
        "user_id": updated_user.id,
        "user_name": updated_user.name,
        "user_age": updated_user.age,
    })


@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db_session)):
    try:
        if not is_valid_uuid_v4(user_id):
            raise ValidationError("user_id must be a valid UUID v4!")

        UserAccessor(db).delete_user_by_id(user_id=user_id)
        db.commit()
    except UserNotFoundException as e:
        return JSONResponse(DefaultErrorResponse(
            code=str(e.status_code),
            message=e.detail,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ).to_json(), status_code=e.status_code)
    except ValidationError:
        db.rollback()
        return DefaultErrorResponse(
            code='422',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
    except Exception:
        db.rollback()
        return DefaultErrorResponse(
            code='500',
            message=traceback.format_exc(),
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    return DefaultSuccessResponse(data={
        "user_id": user_id,
    })