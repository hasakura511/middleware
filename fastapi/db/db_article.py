from db.models import DBArticle, DBUser
from exceptions import TitleException, HttpExceptions
from schemas import ArticleBase
from sqlalchemy.orm.session import Session
from fastapi import HTTPException, status


def _check(db_object, id_=None):
    # print(db_object.__dict__)
    if not db_object:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{DBArticle.__tablename__} id {id_} not found')


# post
def db_create_article(db: Session, request: ArticleBase):
    # if request.content.startswith('testing'):
    if not request.title:
        raise TitleException('Need Title')

    user = db.query(DBUser).filter(DBUser.id == request.user_id).first()

    if not user:
        HttpExceptions.user_not_found(f'User {request.user_id} does not exist')

    new_article = DBArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.user_id,
    )

    db.add(new_article)
    db.commit()
    # need to refresh to get the id
    db.refresh(new_article)
    return new_article


# get
def db_get_article(db: Session, article_id: int):

    article = db.query(DBArticle).filter(DBArticle.id == article_id).first()
    _check(article, article_id)
    return article


# get
def db_get_all_articles(db: Session):
    return db.query(DBArticle).all()
