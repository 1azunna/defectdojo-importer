import json
from http_client import HttpClient
from models.engagement import Engagement


class Engagements:

    def __init__(self, client: HttpClient):
        self.client = client
        self.logger = self.client.logger
        self.endpoint = self.client.url + "/api/v2/engagements/"

    def get(self, engagement: Engagement) -> int | None:
        """Fetch an engagement by name."""
        response = self.client.request(
            "GET",
            self.endpoint,
            params={
                "name": engagement.name,
                "product": engagement.product,
                "status": engagement.status.value,
            },
        )
        try:
            engagement_data = json.loads(response)
            count = engagement_data["count"]
        except Exception as err:
            self.logger.error(
                f"An error occured while getting engagement for name {engagement.name}.",
                exc_info=True,
            )
            raise err
        if count < 1:
            self.logger.warning(f"Engagement not found for name {engagement.name}.")
            return None
        result = max(engagement_data["results"], key=lambda ev: ev["id"])
        engagement_id = result["id"]
        self.logger.info(f"Engagement found, id: {engagement_id}")
        return engagement_id

    def create(self, engagement: Engagement) -> int:
        """Create an engagement."""
        response = self.client.request("POST", self.endpoint, data=engagement.to_dict())
        try:
            engagement_data = json.loads(response)
            engagement_id = engagement_data["id"]
        except Exception as err:
            self.logger.error(
                f"An error occured while creating engagement for name {engagement.name}.",
                exc_info=True,
            )
            raise err
        self.logger.info(f"Engagement created, id: {engagement_id}")
        return engagement_id

    def get_or_create(self, engagement: Engagement) -> int:
        """Get or create an engagement."""
        engagement_id = self.get(engagement)
        if engagement_id is None:
            engagement_id = self.create(engagement)
        return engagement_id
