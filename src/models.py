from typing import Optional

from sqlalchemy import Boolean, Integer, PrimaryKeyConstraint, String, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import uuid


class Base(DeclarativeBase):
    pass
