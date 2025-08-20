from sqlalchemy import Table, Column, DateTime, Boolean, Integer, String
from sqlalchemy.sql import func
from src.database.database import metadata

tasks = Table(
    "tasks", metadata,
    Column("id", Integer, primary_key=True),
    Column("description", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("due_at", DateTime(timezone=True), nullable=True),
    Column("done", Boolean, server_default="false", nullable=False),
)