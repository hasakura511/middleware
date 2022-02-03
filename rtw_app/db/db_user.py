from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.sql_models import DBUser
from db.hashing import Hash
from fastapi.exceptions import HTTPException
from fastapi import status
from auth.exceptions import HTTPExceptions


def create_user(db: Session, request: UserBase):
    new_user = DBUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        raise HTTPExceptions.not_found(f'username {username} not found')
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                     detail=f'username {username} not found')
    return user
