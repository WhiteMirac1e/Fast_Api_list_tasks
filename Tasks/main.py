import logging
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[bool] = False


tasks = []


@app.get("/tasks/", response_model=list[Task])
async def get_tasks():
    return [task for task in tasks if not task.status]


@app.get("/tasks/{id}", response_model=Task)
async def get_tasks_id(id: int):
    task = [task for task in tasks if task.id == id]
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task[0]


@app.post("/tasks/", response_model=Task)
async def add_tasks(task: Task):
    if [t for t in tasks if t.id == task.id]:
        raise HTTPException(status_code=409, detail="Task already exist")
    tasks.append(task)
    logger.info('Отработал POST запрос.')
    return task


@app.put("/tasks/{id}", response_model=Task)
async def put_tasks(id: int, task: Task):
    for i in range(len(tasks)):
        if tasks[i].id == task.id:
            tasks[i] = task
            return tasks[i]
    raise HTTPException(status_code=404, detail='Task not found')


@app.delete("/tasks/{id}")
async def delete_tasks(id: int):
    for i in range(len(tasks)):
        if tasks[i].id == id:
            tasks.pop(i)
            return {'message': 'Task deleted'}
    return HTTPException(status_code=404, detail="Task not found")
