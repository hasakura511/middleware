from routers.schemas import CommentBase, UserAuth
from sqlalchemy.orm.session import Session
from db.sql_models import DBComment
from datetime import datetime as dt
from auth.exceptions import HTTPExceptions


def create_comment(db: Session, request: CommentBase):
    new_comment = DBComment(
        text=request.text,
        username=request.username,
        timestamp=dt.now(),
        post_id=request.post_id,
    )
    db.add(new_comment)
    db.commit()
    # refresh adds id to the db object
    db.refresh(new_comment)
    return new_comment


def get_comments(db: Session, post_id: int):
    # don't forget the .all() --> returns list
    return db.query(DBComment).filter(DBComment.post_id == post_id).all()
