from typing import List
from pydantic import BaseModel


# used in body of post request
class UserBase(BaseModel):
    # colons indicate annotations
    username: str
    email: str
    password: str


# used in body of post request
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    user_id: int


# used in body of post request
class ProductBase(BaseModel):
    title: str
    description: str
    price: float


# defines user inside ArticleDisplay works because of model relationships
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config():
        orm_mode = True


# defines article inside user display works because of model relationships
class Article(BaseModel):
    id: int
    title: str
    content: str
    published: bool

    class Config():
        orm_mode = True


# used in response model
# can cross-link w/ User because relationship is defined in models
class ArticleDisplay(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user_id: int
    user: User

    class Config():
        orm_mode = True


# used in response model
# can cross-link w/ Article because relationship is defined in models
class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    items: List[Article] = []

    # class config returns database data into the above schema (username/email)  --> response model
    class Config():
        orm_mode = True
