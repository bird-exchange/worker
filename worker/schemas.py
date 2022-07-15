from pydantic import BaseModel


class Image(BaseModel):
    uid: int
    name: str
    type: int
    was_fitted: int
