from sqlmodel import SQLModel

from src.schemas.PlaceSchema import WeightedPlaceSchema


class TaskSchema(SQLModel):
    task_id: str


class TaskResultWPlaceSchema(SQLModel):
    task_id: str
    task_status: str
    task_result: WeightedPlaceSchema
