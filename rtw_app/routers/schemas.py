from typing import List
from pydantic import BaseModel
from datetime import datetime as dt


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


# used for authentication
class UserAuth(BaseModel):
    id: int
    username: str
    email: str


class CommentBase(BaseModel):
    username: str
    text: str
    post_id: int


class CommentDisplay(BaseModel):
    id: int
    text: str
    username: str
    timestamp: dt
    post_id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    img_url: str
    img_url_type: str
    caption: str
    user_id: int


class PostDisplay(BaseModel):
    id: int
    img_url: str
    img_url_type: str
    caption: str
    timestamp: dt
    user: UserDisplay
    comments: List[CommentDisplay]

    class Config:
        orm_mode = True
