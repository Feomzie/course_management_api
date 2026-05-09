from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.dependencies.auth import get_current_student, get_current_admin
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User
from app.schemas.enrollment import EnrollmentResponse


router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"]
)


@router.post(
    "/{course_id}",
    response_model=EnrollmentResponse
)

def enroll(
    course_id: int,
    db: Session = Depends(get_db),
    student: User = Depends(get_current_student)
):
    
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code = 404,
            detail = "Course not found"
        )
    
    if not course.is_active:
        raise HTTPException(
            status_code = 400,
            detail = "Course is not active"
        )
    
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == student.id,
        Enrollment.course_id == course_id
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code = 400,
            detail = "Already enrolled in this course"
        )

    total_enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id
    ).count()

    if total_enrollments >= course.capacity:
        raise HTTPException(
            status_code = 400,
            detail = "Course is full"
        )

    new_enrollment = Enrollment(
        user_id=student.id,
        course_id=course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


@router.delete("/{course_id}")
def deregister(
    course_id: int,
    db: Session = Depends(get_db),
    student: User = Depends(get_current_student)
):

    enrollment = db.query(Enrollment).filter(
        Enrollment.user_id == student.id,
        Enrollment.course_id == course_id
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Enrollment does not exist"
        )

    db.delete(enrollment)
    db.commit()

    return {
        "message": "Successfully deregistered from course"
    }


@router.get(
    "/me",
    response_model=list[EnrollmentResponse]
)

def get_my_enrollments(
    db: Session = Depends(get_db),
    student: User = Depends(get_current_student)
):

    return db.query(Enrollment).filter(
        Enrollment.user_id == student.id
    ).all()


@router.get(
    "/",
    response_model=list[EnrollmentResponse]
)

def get_all_enrollments(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    
    return db.query(Enrollment).all()