from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str
    code: str
    capacity: int = Field(..., gt=0)


class CourseResponse(BaseModel):
    id: int
    title: str
    code: str
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True