from fastapi import FastAPI

from app.routes import auth, courses, enrollments
from app.database.db import Base, engine
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Enrollment API"
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(enrollments.router)


@app.get("/")
def root():
    return {
        "message": "API Running"
    }