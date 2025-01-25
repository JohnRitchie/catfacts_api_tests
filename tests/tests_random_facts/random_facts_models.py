from pydantic import BaseModel


class StatusModel(BaseModel):
    verified: bool | None
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
