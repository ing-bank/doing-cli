
# On an error..
# Did you configure the ING project and organization?
# az devops configure -l
# ```bash
# organization=IngEurCDaaS01
# project=IngOne
# az devops configure --defaults organization=https://dev.azure.com/$organization project=$project
# ```


class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message

