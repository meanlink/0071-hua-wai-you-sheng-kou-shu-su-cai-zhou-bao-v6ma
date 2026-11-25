from typing import Literal
from pydantic import BaseModel,Field,model_validator

class Cue(BaseModel):
    code: str=Field(pattern=r"^[A-Z0-9-]{3,24}$")
    film: str=Field(pattern=r"^[A-Z0-9-]{3,24}$")
    in_sec: int=Field(ge=0)
    out_sec: int=Field(gt=0)
    cue_text: str=Field(min_length=3,max_length=200)
    weight: int=Field(ge=1,le=5)

    @model_validator(mode="after")
    def length(self):
        if self.out_sec<=self.in_sec:
            raise ValueError("入点须早于出点")
        return self

class Recording(BaseModel):
    cue_text: str=Field(min_length=3,max_length=200)

class Review(BaseModel):
    result: Literal["approve","redo"]
    note: str=Field(min_length=4,max_length=240)
