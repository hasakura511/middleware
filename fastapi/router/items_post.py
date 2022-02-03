from fastapi import APIRouter, Query, Body, Path, Depends
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/items',
    tags=['items'],
)


# pydantic validates and converts into the correct datatypes
class Image(BaseModel):
    url: str
    alias: str


class ItemModel(BaseModel):
    title: str
    content: str
    comment_title: int
    published: Optional[bool]
    tags: List[str] = []
    metadata: Dict[str, str] = {}
    image: Optional[Image] = None


@router.post('/new')
def create_items(item: ItemModel):
    print(item)
    return {"body": item}


@router.post('/new2/{item_id}')
def create_items(item: ItemModel, item_id: int, version: int = 1):
    # id is path param, version is query param
    print(item_id, version, item)
    return {"body": item,
            "path": item_id,
            "query": version}


@router.post('/new/{item_id}/comment/{comment_id}')
def create_comment(item: ItemModel, item_id: int,
                   comment_title: int = Query(None,
                                              title='Title of the comment',
                                              description=' some description for comment_title',
                                              alias='commentTitle',
                                              deprecated=True),
                   #content: str = Body('optional content body'),
                   # elipsis makes content required
                   content: str = Body(...,
                                       min_length=10,
                                       max_length=50,
                                       # accept only lowercase alphabets and spaces
                                       regex='[a-z\s]*$',
                                       ),
                   # ?commentId=3&v=string1&v=string2&v=string3'
                   v: Optional[List[str]] = Query(["1", "2"]),
                   #gt, ge, lt, le
                   comment_id: int = Path(None, gt=5, le=10),
                   ):
    # Query description appears in the api docs
    # alias changes the ?comment_title to ?commentTitle body
    # deprecated shows deprecated in the docs
    return {"body": {'item': item, 'content': content},
            "path": {'item_id': item_id, 'comment_id': comment_id},
            "query": {'comment_title': comment_title, 'version': v},
            }


def required_func():
    return {'message': 'Learning FastAPI'}
