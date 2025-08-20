from sqlalchemy import select, insert, update, delete
from src.models.models import tasks
from src.database.database import database
from src.schemas.schemas import TaskCreate
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

async def create_task(task: TaskCreate) -> Dict[str, Any]:
    now_utc = datetime.now(timezone.utc)

    # Ensure due_at is timezone-aware if provided
    due_at_aware = None
    if task.due_at:
        if task.due_at.tzinfo is None:
            # Make naive datetime UTC-aware
            due_at_aware = task.due_at.replace(tzinfo=timezone.utc)
        else:
            due_at_aware = task.due_at

    query = insert(tasks).values(
        description=task.description,
        created_at=now_utc,
        due_at=due_at_aware,
        done=False
    )
    task_id = await database.execute(query)  # type: ignore

    return {
        **task.model_dump(),
        "id": task_id,
        "created_at": now_utc,
        "done": False
    }


async def list_tasks() -> List[Dict[str, Any]]:
    query = select(tasks)
    results = await database.fetch_all(query)  # type: ignore
    return [dict(result) for result in results]  # Convert Record to dict


async def delete_task(task_id: int) -> bool:
    # Check if task exists first
    query = select(tasks.c.id).where(tasks.c.id == task_id)
    result = await database.fetch_one(query)  # type: ignore
    if not result:
        return False

    # Delete the task
    query = delete(tasks).where(tasks.c.id == task_id)
    await database.execute(query)  # type: ignore
    return True


async def update_task_description(task_id: int, new_description: str) -> Optional[Dict[str, Any]]:
    query = (
        update(tasks)
        .where(tasks.c.id == task_id)
        .values(description=new_description)
        .returning(tasks)
    )
    result = await database.fetch_one(query)  # type: ignore
    if result:
        return {
            "id": result["id"],
            "description": result["description"],
            "created_at": result["created_at"],
            "due_at": result["due_at"],
            "done": result["done"]
        }
    return None


async def list_done_tasks() -> List[Dict[str, Any]]:
    query = select(tasks).where(tasks.c.done == True)
    results = await database.fetch_all(query)  # type: ignore
    return [
        {
            "id": row["id"],
            "description": row["description"],
            "created_at": row["created_at"],
            "due_at": row["due_at"],
            "done": row["done"]
        }
        for row in results
    ]
    
async def mark_task_done_bool(task_id: int): #type: ignore
    query = update(tasks).where(tasks.c.id == task_id).values(done=True)
    await database.execute(query)  # type: ignore

    # Return the updated task
    query = select(tasks).where(tasks.c.id == task_id)
    task = await database.fetch_one(query)  # type: ignore
    return dict(task) if task else None # type: ignore