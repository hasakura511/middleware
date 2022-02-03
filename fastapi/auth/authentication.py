from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.databases import get_db
from db import models
from db.hash import Hash
from auth.oauth2 import create_access_token

router = APIRouter(
    tags=['authentication']
)


# oauth2.py
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") <-- needs to be the same
@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.DBUser).filter(
        models.DBUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')

    access_token = create_access_token(data={'sub': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username

    }
