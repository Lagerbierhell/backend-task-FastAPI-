from fastapi import FastAPI, HTTPException
from typing import List
from contextlib import asynccontextmanager
import logging
from src.database.database import database, sync_engine, metadata
from src.schemas.schemas import Task , TaskCreate
from src.crud.crud import  mark_task_done_bool,create_task,list_tasks, delete_task, update_task_description, list_done_tasks



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Creating database tables if they do not exist...")
        metadata.create_all(sync_engine)   # only creates tables
        await database.connect()
        logger.info("Database connected successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        await database.disconnect()
        logger.info("Database disconnected successfully")


app = FastAPI(title="Task API with PostgreSQL", lifespan=lifespan)

@app.post("/tasks", response_model=Task)
async def add_task(task: TaskCreate):
    
    
    return await create_task(task)

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return await list_tasks()


@app.delete("/tasks/{task_id}")
async def remove_task(task_id: int):
    success = await delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}



@app.put("/tasks/{task_id}/description", response_model=Task)
async def edit_task_description(task_id: int, new_description: str):
    task = await update_task_description(task_id, new_description)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task



@app.get("/tasks/done", response_model=List[Task])
async def get_done_tasks():
    return await list_done_tasks()



@app.patch("/tasks/{task_id}/done", response_model=Task)
async def mark_task_done(task_id: int): #type: ignore
    task = await mark_task_done_bool(task_id)#type: ignore
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task # type: ignore




