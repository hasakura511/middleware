from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List
from custom_log import product_logger
import time

router = APIRouter(
    prefix='/product',
    tags=['product']
)

products = ['product1', 'product2', 'product3']


# await func() require async def func()
async def time_consuming_func():
    time.sleep(1)
    return 'ok'


# forms
@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products


# request headers - use Header - need to inspect to see this
@router.get('/withheader')
def get_products(
    response: Response,
    # single header
    #custom_header: Optional[str] = Header(None)
    # multiple header
    custom_header: Optional[List[str]] = Header(None),
    # get cookie with key == 'test_cookie'
    test_cookie: Optional[str] = Cookie(None)
):
    print(custom_header, test_cookie)
    product_logger(router.prefix+'/withheader',
                   ','.join([str(custom_header), str(test_cookie)]))
    # add response headers
    response.headers['custom-response-header'] = 'test'
    if custom_header:
        response.headers['custom-request-headers'] = ' ,'.join(custom_header)
    return {
        'data': products,
        'custom_header': custom_header,
        'my_cookie': test_cookie,
    }


@router.get('/all')
async def get_all_products():
    await time_consuming_func()
    # need conversion for class objects
    data = ' '.join(products)
    # simple objects auto-converted to json
    # return products
    # different types of responses: text,xml,html, files, streaming
    response = Response(content=data, media_type='text/plain')
    response.set_cookie(key="test_cookie", value="test cookie value")
    return response


# responses populate the docs
@router.get('/{id}', responses={
    200: {"content": {
        "text/html": {
            "example": "<div>Product</div>"
        }
    },
        "description": "Returns the HTML for an object"
    },
    404: {"content": {
        "text/html": {
            "example": "Product not available"
        }
    },
        "description": "A error message"
    },
},)
def get_product(id: int):
    if id not in list(range(len(products))):
        return PlainTextResponse(status_code=404, content='Product not available', media_type='text/plain')

    product = products[id]
    out = f'''
    <head>
     <style>
     .product {{
         width:500px;
         height: 30px;
         border: 2px inset green;
         background-color: lightblue;
         text-align: center;
         }}
     </style>
    </head>
    <div class = "product">{product}</div>
    '''
    return HTMLResponse(content=out, media_type="text/html")
