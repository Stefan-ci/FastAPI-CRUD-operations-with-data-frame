from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class Track(BaseModel):
    id: Optional[int] = None
    title: str
    artist: str
    duration: float
    last_play: datetime
