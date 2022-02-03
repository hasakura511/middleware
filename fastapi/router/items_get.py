from typing import Optional
from fastapi import Response, status, APIRouter, Depends
from enum import Enum
from router.items_post import required_func

router = APIRouter(
    prefix='/item',
    tags=['item']
)


# type checking
class ItemType(str, Enum):
    # define types
    short = 'short'
    medium = 'medium'
    long = 'long'


# order is important
@router.get("/all",
            # tags=['default'],
            summary="function name gets written here if nothing is supplied",
            description="description here, default is empty",
            response_description="description of the response here")
def read_all_items(item: Optional[int] = None,
                   req_param: dict = Depends(required_func)):
    # item is query param
    return {"item_id": "All", "item": item, "req_param": req_param}


# fastapi uses pydantic for type validation
@router.get("/{item_id}", status_code=status.HTTP_200_OK,
            # tags=['default']
            )
def read_item(item_id: int, response: Response, item: str = "Book", valid: bool = True, q: Optional[str] = "default"):
    # item_id is required path param, everything else is optional query param
    # this gets dumped as description
    '''
    Simulates retrieving items

    - **item_id** id of item mandatory path param
    - **item** name of item
    - **valid** optional query param (bool)
    '''
    # print(valid)
    if item_id > 500:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"{item_id} not found"}
    else:
        return {"item_id": item_id, "item": item, "valid": valid, "q": q}


@router.get('/type/{type}', tags=["default"])
def get_item_type(type: ItemType):
    # only allows the types specified in Blogtype
    return {'message': f'Item type {type}'}
