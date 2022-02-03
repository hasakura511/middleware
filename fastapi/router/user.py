from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from db.db_user import *
from db.databases import get_db
from typing import List

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Create user - response_model uses the defined schema to return data to the post request. if not applies uses the UserBase schema
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_create_user(db, request)


# Update user
@router.post('/{user_id}/update')
def update_user(user_id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_update_user(db, user_id, request)


# Read all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_get_all_users(db)


# Read one user
@router.get('/{user_id}', response_model=UserDisplay)
def get_all_users(user_id: int, db: Session = Depends(get_db)):
    return db_get_user(db, user_id)


# Delete user
@router.get('/{user_id}/delete')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return db_delete_user(db, user_id)
