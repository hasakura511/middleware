from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from db.database import get_psql
from db import sql_models
from db.hashing import Hash
from auth.oauth2 import create_access_token

router = APIRouter(
    tags=['authentication']
)


# oauth2.py
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") <-- needs to be the same
@router.post('/login')
async def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_psql)):
    user = db.query(sql_models.DBUser).filter(
        sql_models.DBUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')

    access_token = await create_access_token(data={'username': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username

    }
