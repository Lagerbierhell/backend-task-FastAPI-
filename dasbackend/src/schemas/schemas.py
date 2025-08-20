from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional


class TaskBase(BaseModel):
    description: str
    due_at: Optional[datetime] = None
    
    
class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    done: bool

    class Config:
        orm_mode = True

        @staticmethod
        def datetime_encoder(v: datetime) -> str:
            return v.astimezone(timezone.utc).isoformat()

        json_encoders = {datetime: datetime_encoder}



