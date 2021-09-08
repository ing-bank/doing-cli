from rich.console import Console

console = Console()


class ConfigurationError(Exception):
    """
    Raise ConfigurationError.
    """

    def __init__(self, message):
        """
        Set message.
        """
        self.message = message


class InputError(Exception):
    """
    Raise InputError.
    """

    def __init__(self, message):
        """
        Set message.
        """
        self.message = message


def devops_error_tips(error: str) -> None:
    """
    Prints user-friendly hints to solve certain errors.

    Azure devops can have quite technical errors where the solution is not immediately obvious.
    """
    if "The conditional access policy defined by your Azure Active Directory administrator has failed" in str(error):
        console.print("doing-cli: You might not be logged into azure. Try visiting dev.azure.com and signing in first.")

    if "ERROR: TF401320: Rule Error for field Story Points." in str(error):
        msg = "doing-cli: This error might be due to a policy enforcing work-items to have story points assigned.\n"
        msg += "See an example how to bulk edit work items with no story points assigned yet in "
        msg += "https://ing-bank.github.io/doing-cli/howto/workflow_bulk_edit_items."
        console.print(msg)
