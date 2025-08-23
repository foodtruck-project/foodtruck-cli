from .models import SetupOptions
from .setup import setup_environment


def setup_api_command(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    target_dir: str = ".",
) -> None:
    """Setup only the API project"""
    options = SetupOptions(api_repo=api_repo, target_dir=target_dir, skip_website=True)
    setup_environment(options)


def setup_website_command(
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
) -> None:
    """Setup only the website project"""
    options = SetupOptions(
        website_repo=website_repo, target_dir=target_dir, skip_api=True
    )
    setup_environment(options)


def setup_all_command(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
) -> None:
    """Setup both API and website projects"""
    options = SetupOptions(
        api_repo=api_repo, website_repo=website_repo, target_dir=target_dir
    )
    setup_environment(options)
