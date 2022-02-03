from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from db.databases import get_db
from typing import List
from auth.oauth2 import get_current_user, oauth2_scheme
import shutil
from os.path import exists

router = APIRouter(
    prefix='/file',
    tags=['file']
)

UPLOAD_PATH = 'files/'


def _check(path):
    if not exists(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{path} not found')


# basic file functionality, stored in memory
@router.post('/utf8')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    return {
        'lines': lines
    }


# stored in memory up to a certain size, then on disk
@router.post('/upload')
def get_uploadfile(file: UploadFile = File(...)):
    # may want to give file a unique name
    path = UPLOAD_PATH+file.filename

    # override/create file if not exists (w+b)
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        'file': path,
        'type': file.content_type,
    }


# response_class=FileResponse --> given path, returns the file in the body
@router.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
    path = f'files/{name}'
    _check(path)
    return path
