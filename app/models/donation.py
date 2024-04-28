from sqlalchemy import Column, ForeignKey, Integer, Text

from ..core.db import Base
from .base import BaseModel


class Donation(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('user.id', name='fk_donation_user_id_user'))
    comment = Column(Text)
