from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=1000)
    completed: bool = False
    priority: int = Field(gt=0, lt=6)
