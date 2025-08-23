from cyclopts import App

from foodtruck_cli.commands.setup.command import (
    setup_all_command,
    setup_api_command,
    setup_website_command,
)

setup_app = App(
    name="setup", help="Setup the complete Food Truck development environment"
)


@setup_app.command
def api(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    target_dir: str = ".",
):
    """Setup only the API project"""
    setup_api_command(api_repo, target_dir)


@setup_app.command
def website(
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
):
    """Setup only the website project"""
    setup_website_command(website_repo, target_dir)


@setup_app.command
def setup_all(
    api_repo: str = "https://github.com/foodtruck-project/foodtruck-api.git",
    website_repo: str = "https://github.com/foodtruck-project/foodtruck-website.git",
    target_dir: str = ".",
):
    """Setup both API and website projects"""
    setup_all_command(api_repo, website_repo, target_dir)


def setup_command() -> None:
    """Setup the complete Food Truck development environment"""
    setup_app()
