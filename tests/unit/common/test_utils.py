import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from common.utils import (
    get_files,
    get_service_keys,
    get_pull_request_id,
    get_build_id,
    get_commit_hash,
    get_scm_uri,
    get_branch_tag,
)


class TestGetFiles:
    """Test cases for the get_files function."""

    def test_get_files_with_none_filename(self):
        """Test get_files when filename is None."""
        result = get_files(filename=None)

        expected = [
            (
                "file",
                (
                    None,
                    None,
                    "application/octet-stream",
                ),
            )
        ]

        assert result == expected

    def test_get_files_with_none_filename_and_payload(self):
        """Test get_files when filename is None but payload is provided."""
        payload = b"test payload"
        result = get_files(filename=None, payload=payload)

        expected = [
            (
                "file",
                (
                    None,
                    None,
                    "application/octet-stream",
                ),
            )
        ]

        assert result == expected

    @patch("builtins.open", new_callable=mock_open, read_data=b"file contents")
    def test_get_files_with_valid_filename(self, mock_file):
        """Test get_files with a valid filename."""
        filename = "/path/to/testfile.txt"

        result = get_files(filename=filename)

        expected = [
            (
                "file",
                (
                    "testfile.txt",
                    b"file contents",
                    "application/octet-stream",
                ),
            )
        ]

        assert result == expected
        mock_file.assert_called_once_with(Path(filename).expanduser().absolute(), "rb")

    @patch("builtins.open", new_callable=mock_open, read_data=b"original contents")
    def test_get_files_with_payload_override(self, mock_file):
        """Test get_files when payload overrides file contents."""
        filename = "/path/to/testfile.txt"
        payload = b"custom payload"

        result = get_files(filename=filename, payload=payload)

        expected = [
            (
                "file",
                (
                    "testfile.txt",
                    b"custom payload",
                    "application/octet-stream",
                ),
            )
        ]

        assert result == expected
        mock_file.assert_called_once_with(Path(filename).expanduser().absolute(), "rb")

    @patch("builtins.open", new_callable=mock_open, read_data=b"file contents")
    def test_get_files_with_relative_path(self, mock_file):
        """Test get_files with a relative path."""
        filename = "~/documents/testfile.txt"

        result = get_files(filename=filename)

        expected = [
            (
                "file",
                (
                    "testfile.txt",
                    b"file contents",
                    "application/octet-stream",
                ),
            )
        ]

        assert result == expected
        # Verify that expanduser() and absolute() were applied
        mock_file.assert_called_once_with(Path(filename).expanduser().absolute(), "rb")

    @patch("builtins.open", side_effect=FileNotFoundError("File not found"))
    def test_get_files_with_nonexistent_file(self, mock_file):
        """Test get_files with a non-existent file."""
        filename = "/path/to/nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            get_files(filename=filename)

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    def test_get_files_with_permission_error(self, mock_file):
        """Test get_files when file cannot be read due to permissions."""
        filename = "/path/to/restricted.txt"

        with pytest.raises(PermissionError):
            get_files(filename=filename)

    @patch("builtins.open", new_callable=mock_open, read_data=b"")
    def test_get_files_with_empty_file(self, mock_file):
        """Test get_files with an empty file."""
        filename = "/path/to/empty.txt"

        result = get_files(filename=filename)

        expected = [
            (
                "file",
                (
                    "empty.txt",
                    b"",
                    "application/octet-stream",
                ),
            )
        ]

        assert result == expected


class TestGetServiceKeys:
    """Test cases for the get_service_keys function."""

    def test_get_service_keys_single_key_default_position(self):
        """Test get_service_keys with single key at default position."""
        service_keys_csv = "key1"
        result = get_service_keys(service_keys_csv)

        assert result == "key1"

    def test_get_service_keys_multiple_keys_default_position(self):
        """Test get_service_keys with multiple keys at default position."""
        service_keys_csv = "key1,key2,key3"
        result = get_service_keys(service_keys_csv)

        assert result == "key1"

    def test_get_service_keys_multiple_keys_position_1(self):
        """Test get_service_keys with multiple keys at position 1."""
        service_keys_csv = "key1,key2,key3"
        result = get_service_keys(service_keys_csv, position=1)

        assert result == "key2"

    def test_get_service_keys_multiple_keys_position_2(self):
        """Test get_service_keys with multiple keys at position 2."""
        service_keys_csv = "key1,key2,key3"
        result = get_service_keys(service_keys_csv, position=2)

        assert result == "key3"

    def test_get_service_keys_position_out_of_range(self):
        """Test get_service_keys when position is out of range."""
        service_keys_csv = "key1,key2"
        result = get_service_keys(service_keys_csv, position=3)

        assert result is None

    def test_get_service_keys_empty_string(self):
        """Test get_service_keys with empty string."""
        service_keys_csv = ""
        result = get_service_keys(service_keys_csv)

        assert result == ""

    def test_get_service_keys_empty_string_position_1(self):
        """Test get_service_keys with empty string at position 1."""
        service_keys_csv = ""
        result = get_service_keys(service_keys_csv, position=1)

        assert result is None

    def test_get_service_keys_single_comma(self):
        """Test get_service_keys with single comma (two empty keys)."""
        service_keys_csv = ","
        result = get_service_keys(service_keys_csv)

        assert result == ""

    def test_get_service_keys_single_comma_position_1(self):
        """Test get_service_keys with single comma at position 1."""
        service_keys_csv = ","
        result = get_service_keys(service_keys_csv, position=1)

        assert result == ""

    def test_get_service_keys_with_spaces(self):
        """Test get_service_keys with keys containing spaces."""
        service_keys_csv = "key with spaces,another key,third key"
        result = get_service_keys(service_keys_csv, position=1)

        assert result == "another key"

    def test_get_service_keys_maxsplit_behavior(self):
        """Test get_service_keys maxsplit behavior with more than 3 parts."""
        # With maxsplit=2, only the first 2 commas are used as separators
        service_keys_csv = "key1,key2,key3,key4,key5"
        result = get_service_keys(service_keys_csv, position=2)

        # Position 2 should return "key3,key4,key5" due to maxsplit=2
        assert result == "key3,key4,key5"

    def test_get_service_keys_exactly_three_parts(self):
        """Test get_service_keys with exactly three parts."""
        service_keys_csv = "key1,key2,key3"

        result_0 = get_service_keys(service_keys_csv, position=0)
        result_1 = get_service_keys(service_keys_csv, position=1)
        result_2 = get_service_keys(service_keys_csv, position=2)

        assert result_0 == "key1"
        assert result_1 == "key2"
        assert result_2 == "key3"

    def test_get_service_keys_negative_position(self):
        """Test get_service_keys with negative position."""
        service_keys_csv = "key1,key2,key3"
        result = get_service_keys(service_keys_csv, position=-1)

        # Should return None since -1 + 1 = 0, and 0 < 1
        assert result == "key3"


@patch.dict(
    "os.environ",
    {
        "PULL_REQUEST_ID": "123",
        "BUILD_ID": "456",
        "COMMIT_HASH": "abcde12345",
        "GIT_BRANCH": "main-branch",
        "CI_PROJECT_URL": "https://gitlab.com/example/repo",
    },
)
class TestBuildSystemFunctionsEnvSet:
    """Test cases for build system environment variable retrieval functions."""

    def test_get_pull_request_id(self):
        """Test get_pull_request_id retrieves the correct PR ID."""

        pr_id = get_pull_request_id()
        assert pr_id == "123"

    def test_get_build_id(self):
        """Test get_build_id retrieves the correct build ID."""

        build_id = get_build_id()
        assert build_id == "456"

    def test_get_commit_hash(self):
        """Test get_commit_hash retrieves the correct commit hash."""

        commit_hash = get_commit_hash()
        assert commit_hash == "abcde12345"

    def test_get_scm_uri(self):
        """Test get_scm_uri retrieves the correct SCM URI."""

        scm_uri = get_scm_uri()
        assert scm_uri == "https://gitlab.com/example/repo"

    def test_get_branch_tag(self):
        """Test get_branch_tag retrieves the correct branch/tag."""
        branch_tag = get_branch_tag()
        assert branch_tag == "main-branch"


@patch.dict("os.environ", {}, clear=True)
class TestBuildSystemFunctionsEnvUnset:

    def test_get_pull_request_id_no_env(self):
        """Test get_pull_request_id returns None when no env vars are set."""

        pr_id = get_pull_request_id()
        assert pr_id is None

    def test_get_build_id_no_env(self):
        """Test get_build_id returns None when no env vars are set."""

        build_id = get_build_id()
        assert build_id is None

    def test_get_commit_hash_no_env(self):
        """Test get_commit_hash returns None when no env vars are set."""

        commit_hash = get_commit_hash()
        assert commit_hash is None

    def test_get_scm_uri_no_env(self):
        """Test get_scm_uri returns None when no env vars are set."""

        scm_uri = get_scm_uri()
        assert scm_uri is None

    def test_get_branch_tag_no_env(self):
        """Test get_branch_tag returns None when no env vars are set."""
        branch_tag = get_branch_tag()
        assert branch_tag is None
