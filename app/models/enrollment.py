from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.db import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    user = relationship(
        "User",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )