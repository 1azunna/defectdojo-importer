import re
import responses
import json
from unittest.mock import patch
from execute import main

dojo_url = "https://defectdojo.example.test"
dtrack_url = "https://dtrack.example.test"
mock_url = re.compile(dojo_url + "/api/v2/(?!import-scan|reimport-scan).*")
dtrack_url_property = re.compile(dtrack_url + "/api/v1/project/(.*)/property")
dtrack_url_config_property = re.compile(dtrack_url + "/api/v1/configProperty(.*)")
dtrack_args = ["-v", "integration", "dtrack"]


@patch("sys.argv", ["defectdojo-importer"] + dtrack_args)
class TestDtrackIntegration:

    @responses.activate
    def test_dtrack_with_existing_integration(self):

        get_response = json.dumps({"count": 0, "results": []}).encode()
        create_response = json.dumps({"id": 1, "name": "Test Item"}).encode()
        dtrack_uuid_response = json.dumps({"uuid": "18841bb6-8f30-47a6-9fe2-caa4336e10d5"}).encode()
        dtrack_config_property_response = json.dumps(
            [
                {
                    "groupName": "integrations",
                    "propertyName": "defectdojo.enabled",
                    "propertyValue": "true",
                    "propertyType": "BOOLEAN",
                },
            ]
        ).encode()
        dtrack_project_property_response = json.dumps(
            [
                {
                    "groupName": "integrations",
                    "propertyName": "defectdojo.engagementId",
                    "propertyValue": "1",
                    "propertyType": "STRING",
                }
            ]
        ).encode()
        responses.add(responses.POST, mock_url, body=create_response, status=201)
        responses.add(responses.GET, mock_url, body=get_response, status=200)
        responses.add(
            responses.GET,
            dtrack_url_config_property,
            body=dtrack_config_property_response,
            status=200,
        )
        responses.add(
            responses.GET,
            re.compile(dtrack_url + "/api/v1/project/lookup(.*)"),
            body=dtrack_uuid_response,
            status=200,
        )
        responses.add(
            responses.GET, dtrack_url_property, body=dtrack_project_property_response, status=200
        )
        responses.add(responses.POST, dtrack_url_property, status=201)
        responses.add(responses.PUT, dtrack_url_property, status=201)
        main()
