from pydantic import BaseModel


class Bird(BaseModel):
    uid: int
    name: str
    type: int
    was_fitted: int
