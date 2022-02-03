from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from db.mongo_models import TaskModel, UpdateTaskModel

collection = 'tasks'
router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.post("/", response_description="Add new task", response_model=TaskModel)
async def create_task(request: Request, task: TaskModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await request.app.mongodb[collection].insert_one(task)
    created_task = await request.app.mongodb[collection].find_one(
        {"_id": new_task.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)


@router.get("/", response_description="List all tasks", response_model=List[TaskModel])
async def list_tasks(request: Request):
    tasks = []
    for doc in await request.app.mongodb[collection].find().to_list(length=100):
        tasks.append(doc)
    return tasks


@router.get("/{id}", response_description="Get a single task", response_model=TaskModel)
async def show_task(id: str, request: Request):
    if (task := await request.app.mongodb[collection].find_one({"_id": id})) is not None:
        return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.put("/{id}", response_description="Update a task", response_model=TaskModel)
async def update_task(id: str, request: Request, task: UpdateTaskModel = Body(...)):
    task = {k: v for k, v in task.dict().items() if v is not None}

    if len(task) >= 1:
        update_result = await request.app.mongodb[collection].update_one(
            {"_id": id}, {"$set": task}
        )

        if update_result.modified_count == 1:
            if (
                updated_task := await request.app.mongodb[collection].find_one({"_id": id})
            ) is not None:
                return updated_task

    if (
        existing_task := await request.app.mongodb[collection].find_one({"_id": id})
    ) is not None:
        return existing_task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/{id}", response_description="Delete Task", response_model=TaskModel)
async def delete_task(id: str, request: Request):
    delete_result = await request.app.mongodb[collection].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")
