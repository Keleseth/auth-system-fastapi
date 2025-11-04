from functools import partial
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampMixin:
    """
    Миксин, предоставляющий поля created_at и updated_at.
    """
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=partial(datetime.now, timezone.utc),
        onupdate=partial(datetime.now, timezone.utc),
        nullable=False
    )
