from fastapi import FastAPI, HTTPException
from typing import List
from contextlib import asynccontextmanager
import logging
from src.database.database import database, sync_engine, metadata
from src.utils.logging_config import setup_logging
from src.schemas.schemas import Task , TaskCreate
from src.crud.crud import  (mark_task_done_bool,
                            create_task,list_tasks,
                            delete_task, 
                            update_task_description, 
                            list_done_tasks)


setup_logging()
logger = logging.getLogger(__name__)  # Logger für dieses Modul

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Creating database tables if they do not exist...")
        metadata.create_all(sync_engine) 
        await database.connect()
        logger.info("Database connected successfully")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        await database.disconnect()
        logger.info("Database disconnected successfully")


app = FastAPI(title="FastAPI mit PostgreSQL", lifespan=lifespan)

@app.post("/tasks", response_model=Task)
async def add_task(task: TaskCreate):
    logger.info(f"Creating task with description: {task.description}")
    return await create_task(task)

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    logger.info(f"Fetching all tasks")
    return await list_tasks()


@app.delete("/tasks/{task_id}")
async def remove_task(task_id: int):
    success = await delete_task(task_id)
    logger.error(f"task mit id: {task_id} wurde gelöscht")
    if not success:
        logger.error(f"Task mit id {task_id} wurde nicht gefunden")
        raise HTTPException(status_code=404, detail="Task wurde nicht gefunden")
    return {"detail": "Erfolgreich gelöscht"}


@app.put("/tasks/{task_id}/description", response_model=Task)
async def edit_task_description(task_id: int, new_description: str):
    task = await update_task_description(task_id, new_description)
    logger.info(f"Task mit id: {task_id} wurde aktualisiert")
    if not task:
        logger.error(f"Task mit id {task_id} wurde nicht gefunden")
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks/done", response_model=List[Task])
async def get_done_tasks():
    logger.info("Alle Positiven Tasks")
    return await list_done_tasks()  


@app.patch("/tasks/{task_id}/done", response_model=Task)
async def mark_task_done(task_id: int): 
    task = await mark_task_done_bool(task_id)
    logger.info(f"Task mit id: {task_id} wurde als erledigt markiert ( TRUE )")
    if not task:
        logger.error(f"Task mit id {task_id} wurde nicht gefunden")
        raise HTTPException(status_code=404, detail="Task not found")
    return task 




