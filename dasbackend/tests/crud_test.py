import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone
from src.schemas.schemas import TaskCreate
from src.crud.crud import (
    create_task,
    list_tasks,
    delete_task,
    update_task_description,
    list_done_tasks,
    mark_task_done_bool
)

@pytest.mark.asyncio
async def test_create_task():
    task = TaskCreate(description="Test Task", due_at=None)

    fake_id = 1
    now_utc = datetime.now(timezone.utc)

    with patch("src.crud.crud.database.execute", new_callable=AsyncMock) as mock_execute:
        mock_execute.return_value = fake_id
        result = await create_task(task)

    assert result["id"] == fake_id
    assert result["description"] == "Test Task"
    assert result["done"] is False

@pytest.mark.asyncio
async def test_list_tasks():
    fake_tasks = [{"id": 1, "description": "Task1", "created_at": datetime.now(), "due_at": None, "done": False}]
    
    with patch("src.crud.crud.database.fetch_all", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = fake_tasks
        results = await list_tasks()

    assert len(results) == 1
    assert results[0]["description"] == "Task1"

@pytest.mark.asyncio
async def test_delete_task_exists():
    with patch("src.crud.crud.database.fetch_one", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = {"id": 1}
        with patch("src.crud.crud.database.execute", new_callable=AsyncMock) as mock_execute:
            result = await delete_task(1)
    
    assert result is True

@pytest.mark.asyncio
async def test_delete_task_not_exists():
    with patch("src.crud.crud.database.fetch_one", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = None
        result = await delete_task(999)
    
    assert result is False

@pytest.mark.asyncio
async def test_update_task_description_found():
    fake_task = {"id": 1, "description": "Updated", "created_at": datetime.now(), "due_at": None, "done": False}
    
    with patch("src.crud.crud.database.fetch_one", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = fake_task
        result = await update_task_description(1, "Updated")

    assert result["description"] == "Updated"

@pytest.mark.asyncio
async def test_update_task_description_not_found():
    with patch("src.crud.crud.database.fetch_one", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = None
        result = await update_task_description(999, "Updated")

    assert result is None

@pytest.mark.asyncio
async def test_list_done_tasks():
    fake_tasks = [{"id": 1, "description": "Done Task", "created_at": datetime.now(), "due_at": None, "done": True}]
    
    with patch("src.crud.crud.database.fetch_all", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = fake_tasks
        results = await list_done_tasks()

    assert len(results) == 1
    assert results[0]["done"] is True

@pytest.mark.asyncio
async def test_mark_task_done_bool():
    fake_task = {"id": 1, "description": "Task", "created_at": datetime.now(), "due_at": None, "done": True}

    with patch("src.crud.crud.database.execute", new_callable=AsyncMock) as mock_execute:
        with patch("src.crud.crud.database.fetch_one", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = fake_task
            result = await mark_task_done_bool(1)

    assert result["done"] is True
