from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dependencies.auth import get_current_admin
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseResponse


router = APIRouter(
    prefix="/courses",
    tags=["courses"]
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


@router.get(
    "/{course_id}",
    response_model=CourseResponse
)

def get_course_by_id(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@router.post(
    "/",
    response_model=CourseResponse
)

def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    
    existing_course = db.query(Course).filter(
        Course.code == course.code
    ).first()

    if existing_course:
        raise HTTPException(
            status_code = 400,
            detail = "Course code already exists"
        )

    new_course = Course(
        title=course.title,
        code=course.code,
        capacity=course.capacity
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


@router.put(
    "/{course_id}",
    response_model=CourseResponse
)

def update_course(
    course_id: int,
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # check duplicate code (excluding current course)
    existing_code = db.query(Course).filter(
        Course.code == course_data.code,
        Course.id != course_id
    ).first()

    if existing_code:
        raise HTTPException(
            status_code=400,
            detail="Course code already exists"
        )

    course.title = course_data.title
    course.code = course_data.code
    course.capacity = course_data.capacity

    db.commit()
    db.refresh(course)

    return course


@router.delete(
    "/{course_id}"
)

def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return {
        "message": "Course deleted successfully"
    }