from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.dependencies.auth import (
    get_current_admin
)

from app.models.course import Course

from app.schemas.course import (
    CourseCreate,
    CourseResponse
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):

    return db.query(Course).filter(
        Course.is_active == True
    ).all()


@router.post(
    "/",
    response_model=CourseResponse
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    existing_course = db.query(Course).filter(
        Course.code == course.code
    ).first()

    if existing_course:
        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
        )

    new_course = Course(**course.dict())

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course