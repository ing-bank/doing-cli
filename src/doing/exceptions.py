from rich.console import Console

console = Console()


class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message


class InputError(Exception):
    def __init__(self, message):
        self.message = message


def devops_error_tips(error: str) -> None:
    """
    Prints user-friendly hints to solve certain errors.

    Azure devops can have quite technical errors where the solution is not immediately obvious.
    """
    if (
        "The conditional access policy defined by your Azure Active Directory administrator has failed"
        in str(error)
    ):
        console.print(
            f"[doing]: You might not be logged into azure. Try visiting dev.azure.com and signing in first."
        )
