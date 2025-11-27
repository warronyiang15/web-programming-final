from pydantic import BaseModel, ConfigDict, Field
from models.course import CourseModel


class CourseResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "course": {
                    "id": "course-123",
                    "name": "Web Programming",
                    "owner_id": "user-123",
                    "created_at": "2025-01-01T00:00:00.000000+00:00",
                    "updated_at": "2025-01-01T00:00:00.000000+00:00"
                }
            }
        }
    )

    status: str = Field(..., description="Response status", example="success")
    course: CourseModel = Field(..., description="Course data")

class MultipleCourseResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "courses": [
                    {
                        "id": "course-123",
                        "name": "Web Programming",
                        "owner_id": "user-123",
                        "created_at": "2025-01-01T00:00:00.000000+00:00",
                        "updated_at": "2025-01-01T00:00:00.000000+00:00"
                    },
                    {
                        "id": "course-456",
                        "name": "Data Structures",
                        "owner_id": "user-123",
                        "created_at": "2025-01-01T00:00:00.000000+00:00",
                        "updated_at": "2025-01-01T00:00:00.000000+00:00"
                    }
                ]
            }
        }
    )

    status: str = Field(..., description="Response status", example="success")
    courses: list[CourseModel] = Field(..., description="List of courses")