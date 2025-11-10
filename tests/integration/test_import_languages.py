import re
import json
from unittest.mock import patch
import responses
import config
from importer.execute import main

dojo_url = "https://defectdojo.example.test"
mock_url = re.compile(f"{dojo_url}/api/v2/.*")
args = ["-f", "tests/reports/cloc.json", "--import-type", "languages"]


@patch("sys.argv", ["defectdojo-importer"] + args)
@responses.activate
def test_import_languages(mock_env):
    with patch.object(config, "env", mock_env):
        generic_response = json.dumps(
            {"count": 1, "results": [{"id": 1, "name": "Test Item"}]}
        ).encode()
        responses.add(responses.GET, mock_url, body=generic_response, status=200)
        responses.add(
            responses.POST, f"{dojo_url}/api/v2/import-languages/", status=200
        )
        main()
