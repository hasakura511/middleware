from routers.schemas import PostBase, UserAuth
from sqlalchemy.orm.session import Session
from db.sql_models import DBPost
from datetime import datetime as dt
from auth.exceptions import HTTPExceptions


def create_post(db: Session, request: PostBase):
    new_post = DBPost(
        img_url=request.img_url,
        img_url_type=request.img_url_type,
        caption=request.caption,
        timestamp=dt.now(),
        user_id=request.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_all(db: Session):
    return db.query(DBPost).all()


def delete_post(db: Session, post_id: int, current_user: UserAuth):
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not post:
        raise HTTPExceptions.not_found(f'Post id {post_id} not found')

    if post.user_id != current_user.id:
        raise HTTPExceptions.forbidden(
            f'Only user {post.user_id} can delete this post')

    db.delete(post)
    db.commit()
    return 'OK'
