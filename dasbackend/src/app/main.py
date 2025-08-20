from fastapi import FastAPI
from typing import List
from contextlib import asynccontextmanager
import logging
from src.database.database import database, sync_engine, metadata
from src.schemas.schemas import Task, TaskCreate
from src.crud.crud import create_task, list_tasks


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

@app.get("/tasks", response_model=List[TaskCreate])
async def get_tasks():
    return await list_tasks()








