# python lib
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.websockets import WebSocket
import uvicorn
from fastapi import FastAPI, Response, status, Request
from enum import Enum
from exceptions import TitleException
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from fastapi.staticfiles import StaticFiles
import time

# routers
from router import items_get, items_post, user, article, product, file, websocket_chat, dependencies

# templates
from templates import templates

# db models
from db import models
from db.databases import engine

# graphql schemas
from schemas_graphql import graphql_app

# creates sqlite db file & model
models.Base.metadata.create_all(engine)

# app = FastAPI(openapi_url="/api/openapi.json")
app = FastAPI()

# middleware
origins = [
    # 'http://localhost:3000/' <- remove last /
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Currently only middleware("http") is supported


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    # preprocess above
    # call next is the api that was called.
    response = await call_next(request)
    # postprocess below
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

# mount filesystem directory
'''
The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. So, any path that starts with "/static" will be handled by it.

The directory="static" refers to the name of the directory that contains your static files.

The name="static" gives it a name that can be used internally by FastAPI.
'''
app.mount('/files', StaticFiles(directory='files'), name='files')
app.mount('/templates/static',
          StaticFiles(directory='templates/static'), name='static')

# graphql api
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# rest api routers
app.include_router(authentication.router)
app.include_router(items_get.router)
app.include_router(items_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(file.router)
app.include_router(templates.router)
app.include_router(websocket_chat.router)
app.include_router(dependencies.router)


@ app.get("/")
def read_root():
    return {"Hello": "World"}


@ app.get("/test/")
def read_test():
    return {"test": "test"}


# no slash
@ app.get("/test")
def read_test2():
    return {"test2": "test2"}


# exception handlers
@ app.exception_handler(TitleException)
def title_exception_handler(request: Request, exc: TitleException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={'detail': exc.name}
    )


# intercepts all HTTP Exceptions
# @app.exception_handler(HTTPException)
# def custom_exception_handler(request: Request, exc: HTTPException):
#     return PlainTextResponse(
#         str(exc),
#         status_code=status.HTTP_400_BAD_REQUEST,
#     )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000,
                log_level="info", reload=True)
