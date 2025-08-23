from pydantic import BaseModel, Field


class ApiStatus(BaseModel):
    """Status of the API service."""

    is_running: bool = Field(description="Whether the API service is currently running")
    pid: int | None = Field(
        default=None, description="Process ID of the running API service"
    )
    port: int | None = Field(
        default=None, description="Port on which the API service is running"
    )


class ApiOperationResult(BaseModel):
    """Result of an API operation."""

    success: bool = Field(description="Whether the operation was successful")
    message: str = Field(description="Result message")
    details: str = Field(
        default="", description="Additional details or error information"
    )
