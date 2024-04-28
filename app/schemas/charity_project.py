from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field

from app.core.config import MAX_STRING_NAME, MIN_STRING_NAME


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        min_length=MIN_STRING_NAME, max_length=MAX_STRING_NAME
    )
    description: Optional[str] = Field(min_length=MIN_STRING_NAME)
    full_amount: Optional[int] = Field(gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=MIN_STRING_NAME, max_length=MAX_STRING_NAME)
    description: str = Field(..., min_length=MIN_STRING_NAME)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
