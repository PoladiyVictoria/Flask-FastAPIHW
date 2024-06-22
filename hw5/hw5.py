import uvicorn
import logging
from enum import Enum
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

"""
Необходимо создать API для управления списком задач. Каждая задача должна
содержать заголовок и описание. Для каждой задачи должна быть возможность
указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
○ GET /tasks - возвращает список всех задач.
○ GET /tasks/{id} - возвращает задачу с указанным идентификатором.
○ POST /tasks - добавляет новую задачу.
○ PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
○ DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и
ответа. Для этого использовать библиотеку Pydantic.
"""

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StatusEnum(str, Enum):
    done = "выполнена"
    not_done = "не выполнена"


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: StatusEnum


tasks = [
    Task(
        id=1,
        title="Learn More",
        description="try to learn Faster and better",
        status=StatusEnum.not_done,
    ),
    Task(
        id=2,
        title="Clean Home",
        description="clean bathroom and kitchen",
        status=StatusEnum.done,
    ),
]


@app.get("/")
@app.get("/tasks/", response_model=list[Task])
@app.get("/tasks/{task_id}", response_model=list[Task])
async def get_tasks(task_id: int = None):
    if task_id:
        return [task for task in tasks if task.id == task_id]
    return tasks


@app.post("/tasks/", response_model=Task)
async def create_task(task: Task):
    if [t for t in tasks if t.id == task.id]:
        raise HTTPException(status_code=403, detail="This id is already in use")
    tasks.append(task)
    logger.info(f"Task id={task.id} {task.title} - успешно добавлен")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i] = task
            logger.info(f"Task id={task.id} - успешно изменен")
            return tasks[i]
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            logger.info(f"Task id={task.id} {task.title} - успешно удален")
            return {"message": f"Task id={task_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/status/")
async def get_items(status: StatusEnum = Query(None)):
    return [task for task in tasks if task.status == status]

if __name__ == '__main':
    uvicorn.run("hw5:app", host="127.0.0.1", port=8000, reload=True)
