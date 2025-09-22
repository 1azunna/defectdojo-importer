from importer import Importer
from models.exceptions import ConfigurationError
import pytest


class TestImporter:
    def test_no_args(self, capsys):
        with pytest.raises(SystemExit) as exc_info:
            Importer.run([])
        captured = capsys.readouterr()
        assert "usage:" in captured.out
        assert exc_info.value.code == 0

    def test_invalid_config_no_file(self, capsys, caplog):
        """Test that invalid config (missing file) causes SystemExit with error message."""
        import logging

        args = ["-v"]
        with caplog.at_level(logging.ERROR):
            with pytest.raises(SystemExit) as exc_info:
                Importer.run(args)

        captured = capsys.readouterr()
        # The error should be logged
        assert "Configuration error: File is required for import." in caplog.text
        assert caplog.records[0].levelname == "ERROR"
        # Help should be printed to stdout
        assert "usage:" in captured.out
        assert exc_info.value.code == 1
