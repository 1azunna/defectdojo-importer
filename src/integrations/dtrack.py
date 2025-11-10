import json
from models.dtrack import Project, ProjectProperty
from models.config import Config
from http_client import HttpClient


class Dtrack:
    """Handler for Dependency Track Projects."""

    def __init__(self, client: HttpClient, api_key: str):
        self.client = client
        self.client.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Api-Key": api_key,
        }
        self.logger = client.logger

    def get_integration(self) -> bool:
        """Check if the Dependency Track integration is enabled."""

        enabled = None
        endpoint = self.client.url + "/api/v1/configProperty"
        response = self.client.request("GET", endpoint)
        try:
            config_data = json.loads(response)
        except Exception as err:
            self.logger.error("An error occured while checking the integration status.")
            raise err

        for config_property in config_data:
            if config_property["groupName"] == "integrations":
                if config_property["propertyName"] == "defectdojo.enabled":
                    enabled = config_property["propertyValue"].lower()
                    break
        if enabled != "true":
            self.logger.warning("Dependency Track integration is not enabled.")
            return False
        self.logger.info("Dependency Track integration is enabled.")
        return True

    def update_integration(self, config: Config) -> bool:
        """Enable or disable the Dependency Track integration."""
        endpoint = self.client.url + "/api/v1/configProperty/aggregate"
        payload = [
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.apiKey",
                "propertyValue": config.api_key,
                "propertyType": "STRING",
            },
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.enabled",
                "propertyValue": "true",
                "propertyType": "BOOLEAN",
            },
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.reimport.enabled",
                "propertyValue": "true",
                "propertyType": "BOOLEAN",
            },
            {
                "groupName": "integrations",
                "propertyName": "defectdojo.url",
                "propertyValue": config.api_url,
                "propertyType": "URL",
            },
        ]
        try:
            self.client.request("POST", endpoint, data=json.dumps(payload))
        except Exception as err:
            self.logger.error(
                "An error occured while updating the integration config. Check API key permissions or enable the integration manually"
            )
            raise err
        self.logger.info("Dependency Track integration has been enabled.")
        return True

    def get_project_uuid(self, project: Project) -> str:
        """Get a dependency track project uuid."""
        endpoint = self.client.url + "/api/v1/project/lookup"
        response = self.client.request("GET", endpoint, params=project.to_dict())
        try:
            project_data = json.loads(response)
            uuid = project_data["uuid"]
        except Exception as err:
            self.logger.error(
                "An error occured while getting the dependency track project %s.",
                project.name,
            )
            raise err
        self.logger.info("Dependency Track project found, uuid: %s", uuid)
        return uuid

    def get_project_properties(self, properties: ProjectProperty):
        """Get Dependency Track project properties"""
        endpoint = self.client.url + f"/api/v1/project/{properties.uuid}/property"
        response = self.client.request("GET", endpoint)
        try:
            properties_data = json.loads(response)
        except Exception as err:
            self.logger.error(
                "An error occured while getting the dependency track properties for project %s.",
                properties.uuid,
            )
            raise err
        return properties_data

    def update_project_properties(self, properties: ProjectProperty):
        """Update Dependency Track project properties"""
        endpoint = self.client.url + f"/api/v1/project/{properties.uuid}/property"
        do_not_reactivate = False
        if not properties.reactivate:
            do_not_reactivate = True
        payload = [
            {
                "propertyType": "STRING",
                "groupName": "integrations",
                "propertyName": "defectdojo.engagementId",
                "propertyValue": str(properties.engagement),
            },
            {
                "propertyType": "BOOLEAN",
                "groupName": "integrations",
                "propertyName": "defectdojo.reimport",
                "propertyValue": str(properties.reimport).lower(),
            },
            {
                "propertyType": "BOOLEAN",
                "groupName": "integrations",
                "propertyName": "defectdojo.doNotReactivate",
                "propertyValue": str(do_not_reactivate).lower(),
            },
        ]

        existing_properties = self.get_project_properties(properties)

        for item in payload:
            property_name = item["propertyName"]

            # Check if the property with the same "propertyName" exists
            property_exists = any(
                prop["propertyName"] == property_name for prop in existing_properties
            )

            if property_exists:
                # Perform the update for the existing property
                self.client.request("POST", endpoint, data=json.dumps(item))
            else:
                # Create a new property
                self.logger.info(
                    "Creating Dependency Track project property: %s", property_name
                )
                self.client.request("PUT", endpoint, data=json.dumps(item))
        return self.logger.info(
            "Dependency Track project properties updated successfully"
        )
