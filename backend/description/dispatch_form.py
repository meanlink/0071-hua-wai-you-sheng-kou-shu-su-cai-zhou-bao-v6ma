from datetime import datetime
from pydantic import BaseModel,Field,model_validator

class Dispatch(BaseModel):
    channel: str=Field(pattern=r"^[A-Z0-9-]{3,24}$")
    release_at: datetime

    @model_validator(mode="after")
    def use_zone(self):
        if self.release_at.utcoffset() is None:
            raise ValueError("计划发送时间需要时区")
        return self
