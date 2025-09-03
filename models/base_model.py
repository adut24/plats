#!/usr/bin/env python3
from datetime import datetime
from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.orm import declarative_base, declared_attr
from zoneinfo import ZoneInfo


Base = declarative_base()
PARIS_TZ = ZoneInfo("Europe/Paris")


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            default=lambda: datetime.now(PARIS_TZ)
            )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(PARIS_TZ),
        onupdate=lambda: datetime.now(PARIS_TZ)
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
