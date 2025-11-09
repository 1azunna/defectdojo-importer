import re
import json
import pytest
from unittest.mock import patch
import responses
from models.exceptions import InvalidScanType
from importer.execute import main

dojo_url = "https://defectdojo.example.test"
mock_url = re.compile(dojo_url + "/api/v2/(?!import-scan|reimport-scan).*")
mock_url_except_test_type = re.compile(dojo_url + "/api/v2/(?!test_types).*")
mock_url_except_api_scan = re.compile(
    dojo_url + "/api/v2/(?!product_api_scan_configurations).*"
)
args = ["-f", "tests/reports/eslint-report.json", "--import-type", "findings"]
api_scan_args = [
    "--import-type",
    "findings",
    "--tool-configuration-name",
    "Sonarqube",
    "--tool-configuration-params",
    "Sonar_Project-key,Sonar-org",
]


@patch("sys.argv", ["defectdojo-importer"] + args)
class TestImportFindingsFromFile:
    @responses.activate
    def test_import_existing_test_findings(self):
        response = json.dumps(
            {"count": 1, "results": [{"id": 1, "name": "Test Item"}]}
        ).encode()
        responses.add(responses.GET, mock_url, body=response, status=200)
        responses.add(responses.POST, dojo_url + "/api/v2/reimport-scan/", status=200)
        main()

    @responses.activate
    def test_import_new_test_findings(self):
        response = json.dumps(
            {"count": 1, "results": [{"id": 1, "name": "Test Item"}]}
        ).encode()
        get_response = json.dumps({"count": 0, "results": []}).encode()
        create_response = json.dumps({"id": 1, "name": "Test Type"}).encode()
        responses.add(responses.POST, mock_url, body=create_response, status=201)
        responses.add(
            responses.GET, dojo_url + "/api/v2/test_types/", body=response, status=200
        )
        responses.add(
            responses.GET, mock_url_except_test_type, body=get_response, status=200
        )
        responses.add(responses.POST, dojo_url + "/api/v2/import-scan/", status=200)
        main()

    @responses.activate
    def test_invalid_test_type(self):
        create_response = json.dumps({"id": 1, "name": "Test Type"}).encode()
        get_response = json.dumps({"count": 0, "results": []}).encode()
        responses.add(responses.GET, mock_url, body=get_response, status=200)
        responses.add(responses.POST, mock_url, body=create_response, status=201)
        with pytest.raises(InvalidScanType):
            main()


@patch("sys.argv", ["defectdojo-importer"] + api_scan_args)
class TestApiScanImport:
    @responses.activate
    def test_import_with_existing_configuration(self):
        response = json.dumps(
            {"count": 1, "results": [{"id": 1, "name": "Test Item"}]}
        ).encode()
        get_response = json.dumps({"count": 0, "results": []}).encode()
        create_response = json.dumps(
            {"id": 1, "name": "API Scan Configuration"}
        ).encode()
        responses.add(responses.POST, mock_url, body=create_response, status=201)
        responses.add(
            responses.GET,
            dojo_url + "/api/v2/product_api_scan_configurations/",
            body=get_response,
            status=200,
        )
        responses.add(
            responses.GET, mock_url_except_api_scan, body=response, status=200
        )
        responses.add(responses.POST, dojo_url + "/api/v2/reimport-scan/", status=200)
        main()

    @responses.activate
    def test_import_with_new_configuration(self):
        response = json.dumps(
            {"count": 1, "results": [{"id": 1, "name": "Test Item"}]}
        ).encode()
        create_response = json.dumps(
            {"id": 1, "name": "API Scan Configuration"}
        ).encode()
        responses.add(responses.POST, mock_url, body=create_response, status=201)
        responses.add(responses.GET, mock_url, body=response, status=200)
        responses.add(responses.POST, dojo_url + "/api/v2/reimport-scan/", status=200)
        main()
