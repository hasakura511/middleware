from typing import List
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from routers.schemas import CommentBase, UserAuth, CommentDisplay
from db.database import get_psql
from db import db_comment
from auth.exceptions import HTTPExceptions
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


@router.get('/all/{post_id}', response_model=List[CommentDisplay])
def get_comments(post_id: int, db: Session = Depends(get_psql)):
    return db_comment.get_comments(db, post_id)


@router.post('')
def create_comment(request: CommentBase, db: Session = Depends(get_psql), current_user: UserAuth = Depends(get_current_user)):
    return db_comment.create_comment(db, request)
