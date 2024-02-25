import uuid

from models.exceptions import UserNotFoundException
from sqlalchemy import UUID, Column, SmallInteger, String
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column("user_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("user_name", String)
    age = Column("user_age", SmallInteger)


class UserAccessor:
    def __init__(self, db: Session) -> None:
        self.db = db


    def insert_user(self, user_name: str, user_age: int) -> User:
        new_user = User()
        new_user.name = user_name
        new_user.age = user_age

        self.db.add(new_user)
        self.db.flush()

        return new_user


    def select_all_users(self) -> list[User]:
        return self.db.query(User).all()


    def select_user_by_id(self, user_id: str) -> list[User]:
        selected_user: User = self.db.query(User).filter(User.id == uuid.UUID(user_id, version=4)).first()
        if not selected_user:
            raise UserNotFoundException()

        return selected_user


    def update_user_by_id(self, user: User) -> User:
        selected_user: User = self.select_user_by_id(user_id=user.id)
        if selected_user:
            selected_user.age = user.age
            selected_user.name = user.name
        else:
            raise UserNotFoundException()

        self.db.flush()

        return selected_user


    def delete_user_by_id(self, user_id: UUID):
        '''
        Delete one user which name match with user_name
        '''

        selected_user = self.select_user_by_id(user_id=user_id)
        if selected_user:
            self.db.delete(selected_user)
        else:
            raise UserNotFoundException()