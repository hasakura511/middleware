
import uvicorn
from fastapi import FastAPI
from db.database import Databases
from routers import tasks, user, post, comment
from auth import authentication
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# mongo needs its own event loop
databases = Databases()
app = FastAPI()

# middleware
origins = [
    # 'http://localhost:3000/' <- remove last /
    'http://localhost:3000',
    'http://103.236.176.253:3000',
    'http://rtw_client:3000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/images', StaticFiles(directory='images'), name='images')

app.include_router(tasks.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(authentication.router)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = databases.async_mongo_client
    app.mongodb = app.mongodb_client["rtw"]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
def root():
    return 'RTW App'


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001,
                log_level="info", reload=True)
