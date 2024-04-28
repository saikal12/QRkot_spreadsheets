from sqlalchemy import Column, String, Text

from ..core.config import MAX_STRING_NAME
from ..core.db import Base
from .base import BaseModel


class CharityProject(Base, BaseModel):
    name = Column(String(MAX_STRING_NAME), unique=True, nullable=False)
    description = Column(Text, nullable=False)