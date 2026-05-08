from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String,
        nullable=False
    )

    code = Column(
        String,
        unique=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )