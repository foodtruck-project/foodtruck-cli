from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from ...utils.fs import create_dir


class ProjectSetupResult(BaseModel):
    """Result of a project setup operation."""

    success: bool = Field(description="Whether the setup was successful")
    message: str = Field(default="", description="Optional error or info message")
    project_path: Path | None = Field(
        default=None, description="Path to the project if created"
    )


class SetupOptions(BaseModel):
    """Configuration options for the Food Truck development environment setup."""

    api_repo: str = Field(
        default="https://github.com/foodtruck-project/foodtruck-api.git",
        description="API repository URL",
    )
    website_repo: str = Field(
        default="https://github.com/foodtruck-project/foodtruck-website.git",
        description="Website repository URL",
    )
    target_dir: str = Field(
        default="foodtruck-projects",
        description="Target directory to clone repositories",
    )
    skip_api: bool = Field(default=False, description="Skip API repository setup")
    skip_website: bool = Field(
        default=False, description="Skip website repository setup"
    )

    @field_validator("target_dir")
    @classmethod
    def validate_target_dir(cls, value: str) -> str:
        """Validate and normalize target directory path."""
        if not value or value.strip() == "":
            return "foodtruck-projects"
        return value.strip()

    def get_target_path(self) -> Path:
        """Get the resolved target directory path."""
        return create_dir(self.target_dir)

    def should_setup_api(self) -> bool:
        """Check if API setup should be performed."""
        return not self.skip_api

    def should_setup_website(self) -> bool:
        """Check if website setup should be performed."""
        return not self.skip_website
