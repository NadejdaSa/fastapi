from pydantic import BaseModel
from datetime import datetime

class AdvertisementCreate(BaseModel):
    title: str
    description: str
    price: float
    owner: str

class AdvertisementUpdate(BaseModel):
    title: str = None
    description: str = None
    price: float = None
    owner: str = None

class Advertisement(AdvertisementCreate):
    id: int
    created_at: datetime
    