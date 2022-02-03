from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from .schemas import UserBase, UserDisplay
from db.database import get_psql
from db import db_user
from auth.exceptions import HTTPExceptions

# AssertionError: A path prefix must not end with '/', as the routes will start with '/'
router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_psql)):
    return db_user.create_user(db, request)
