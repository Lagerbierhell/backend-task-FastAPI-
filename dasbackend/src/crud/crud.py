from sqlalchemy import select, insert
from src.models.models import tasks
from src.database.database import database
from src.schemas.schemas import TaskCreate
from datetime import datetime, timezone
from typing import Any, Dict, List

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

    # Only return the fields you want
    return [
        {
            "description": row["description"],
            "created_at": row["created_at"],
            "due_at": row["due_at"],
            "done": row["done"]
        }
        for row in results
    ]