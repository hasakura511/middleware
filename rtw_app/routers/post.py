from typing import List
from fastapi import APIRouter, status
from fastapi.datastructures import UploadFile
from fastapi.params import Depends, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from .schemas import PostBase, PostDisplay, UserAuth
from db.database import get_psql
from db import db_post
import random
import string
import shutil
from auth.oauth2 import get_current_user
from auth.exceptions import HTTPExceptions

# AssertionError: A path prefix must not end with '/', as the routes will start with '/'
router = APIRouter(
    prefix='/post',
    tags=['post']
)

img_url_types = ['absolute', 'relative']


@router.post('', response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_psql), current_user: UserAuth = Depends(get_current_user)):
    if not request.img_url_type in img_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="img_url_types of 'absolute' or 'relative' required")
    return db_post.create_post(db, request)


@router.get('/all', response_model=List[PostDisplay])
def get_all(db: Session = Depends(get_psql)):
    return db_post.get_all(db)


@router.post('/image')
def upload_image(image: UploadFile = File(...), current_user: UserAuth = Depends(get_current_user)):
    rand_str = ''.join(random.choice(string.ascii_letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}


@router.get('/delete/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_psql), current_user: UserAuth = Depends(get_current_user)):
    return db_post.delete_post(db, post_id, current_user)
