from pydantic import BaseModel


class MoveRequest(BaseModel):

    from_pos: list[int]
    to_pos: list[int]
    captures: list[list[int]] = []