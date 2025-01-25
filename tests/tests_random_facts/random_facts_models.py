from pydantic import BaseModel
from typing import Optional


class StatusModel(BaseModel):
    verified: Optional[bool]
    sentCount: int

class RandomFactsModel(BaseModel):
    status: StatusModel
    _id: str
    __v: int
    user: str
    text: str
    type: str
    deleted: bool
    createdAt: str
    updatedAt: str
