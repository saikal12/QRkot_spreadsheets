from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.config import INITIAL_AMOUNT


class BaseModel:
    __table_args__ = (
        CheckConstraint(f'invested_amount >= {INITIAL_AMOUNT}', name='check_invested_amount_positive'),
        CheckConstraint('full_amount >= invested_amount', name='check_invested_gte_full_amount')
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=INITIAL_AMOUNT, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)

    class Meta:
        abstract = True
