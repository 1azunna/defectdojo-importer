import json
from http_client import HttpClient


class ToolConfigurations:

    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/tool_configurations/"

    def get(self, name: str) -> int | None:
        """Fetch tool configuration details by name."""

        response = self.client.request("GET", self.endpoint, params={"name": name})
        try:
            tool_config_data = json.loads(response)
            count = tool_config_data["count"]
        except Exception as err:
            self.logger.error(
                f"An error occured while getting tool configuration details for {name}.",
                exc_info=True,
            )
            raise err
        if count < 1:
            self.logger.warning("Tool configuration %s not found", name)
            return None
        result = max(tool_config_data["results"], key=lambda ev: ev["id"])
        tool_config_id = result["id"]
        self.logger.info("Tool configuration found, id: %s", tool_config_id)
        return tool_config_id
