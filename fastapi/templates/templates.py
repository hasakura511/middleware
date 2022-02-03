from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.background import BackgroundTasks
from schemas import ProductBase
from custom_log import product_logger

router = APIRouter(
    prefix='/templates',
    tags=['templates']
)

templates = Jinja2Templates(directory='templates')


@router.get('/products/{id}', response_class=HTMLResponse)
def get_product(id: str, request: Request, bt: BackgroundTasks):
    # creates a thread in run_in_threadpool
    bt.add_task(product_logger, router.prefix +
                f'/products/{id}', f'get product id {id}')
    return templates.TemplateResponse("product.html",
                                      context={
                                          'request': request,
                                          'id': id,
                                          'title': 'test product',
                                          'description': 'test desc',
                                          'price': 9.99,
                                          'stylesheet': '/templates/static/styles.css'
                                      })


@router.post('/products/{id}', response_class=HTMLResponse)
def post_product(id: str, request: Request, product: ProductBase):
    return templates.TemplateResponse("product.html",
                                      context={
                                          'request': request,
                                          'id': id,
                                          'title': product.title,
                                          'description': product.description,
                                          'price': product.price,
                                          'stylesheet': '/templates/static/styles.css'
                                      })
