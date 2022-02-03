from fastapi import APIRouter, Depends
from schemas import ArticleBase, ArticleDisplay, UserBase
from sqlalchemy.orm import Session
from db.db_article import *
from db.databases import get_db
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix='/article',
    tags=['article']
)


# Create user - response_model uses the defined schema to return data to the post request. if not applies uses the UserBase schema
@router.post('/', response_model=ArticleDisplay)
def article(request: ArticleBase, db: Session = Depends(get_db),
            current_user: UserBase = Depends(get_current_user),):
    return db_create_article(db, request)


# Read one user
@router.get('/{article_id}',
            response_model=ArticleDisplay,
            )
def get_article(article_id: int, db: Session = Depends(get_db),
                # token authentication
                #token: str = Depends(oauth2_scheme),
                # user authentication using tokens
                current_user: UserBase = Depends(get_current_user),
                ):
    return db_get_article(db, article_id)
    # return {
    #     'data': db_get_article(db, article_id),
    #     'current_user': current_user,
    # }


# Read all users
@router.get('/', response_model=List[ArticleDisplay])
def get_all_articles(db: Session = Depends(get_db)):
    return db_get_all_articles(db)
