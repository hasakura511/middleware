from fastapi import APIRouter, Depends
from fastapi.requests import Request
from typing import List, Dict
from custom_log import product_logger

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies=[Depends(product_logger)]
)


def convert_params(request: Request, separator: str):
    query_params = []

    for key, value in request.query_params.items():
        query_params.append(f'{key} {separator} {value}')

    return query_params


def convert_headers(request: Request, separator: str = '--', query_params: List = Depends(convert_params)):
    #out_headers = []
    out_headers = {}

    for key, value in request.headers.items():
        #out_headers.append(f'{key} {separator} {value}')
        out_headers[key] = value
    return {'headers': out_headers, 'query_params': query_params}


@router.get('')
def get_items(separator: str = '--', headers: Dict = Depends(convert_headers)):
    return {
        'items': ['a', 'b'],
        'headers': headers
    }


class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


# Account will be automatically be created using the args passed
# Account = Depends() shortcut Account = Depends(Account)
@router.post('/user')
def create_user(name: str, email: str, password: str, account: Account = Depends()):
    return {'name': account.name, 'email': account.email}
