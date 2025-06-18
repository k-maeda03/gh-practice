#!/usr/bin/env python3
"""
Tests for hello.py script
"""
import io
import logging
import sys
from unittest.mock import MagicMock, patch

import pytest

from hello import main, setup_logging


class TestHelloScript:
    """Test cases for hello.py script"""

    def test_main_default_behavior(self, capsys):
        """Test main function with default arguments"""
        with patch.object(sys, "argv", ["hello.py"]):
            main()

        captured = capsys.readouterr()
        assert "Hello, GitHub CLI!" in captured.out
        assert "This is an improved practice repository." in captured.out

    def test_main_with_custom_name(self, capsys):
        """Test main function with custom name argument"""
        with patch.object(sys, "argv", ["hello.py", "--name", "World"]):
            main()

        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out
        assert "This is an improved practice repository." in captured.out

    def test_main_with_verbose_flag(self, capsys, caplog):
        """Test main function with verbose logging enabled"""
        with patch.object(sys, "argv", ["hello.py", "--verbose"]):
            with caplog.at_level(logging.INFO):
                main()

        captured = capsys.readouterr()
        assert "Hello, GitHub CLI!" in captured.out

        # Check if logging messages were captured
        assert "Starting hello script" in caplog.text
        assert "Script completed successfully" in caplog.text

    def test_main_with_custom_name_and_verbose(self, capsys, caplog):
        """Test main function with both custom name and verbose flag"""
        with patch.object(sys, "argv", ["hello.py", "--name", "Test", "--verbose"]):
            with caplog.at_level(logging.INFO):
                main()

        captured = capsys.readouterr()
        assert "Hello, Test!" in captured.out
        assert "Starting hello script" in caplog.text

    def test_setup_logging(self):
        """Test logging setup function"""
        # Clear any existing handlers
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        setup_logging()

        # Check if logging is configured
        logger = logging.getLogger()
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0

    def test_error_handling_with_mock_exception(self, capsys):
        """Test error handling when an exception occurs"""
        with patch.object(sys, "argv", ["hello.py"]):
            with patch("builtins.print", side_effect=Exception("Test error")):
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1

    def test_help_argument(self, capsys):
        """Test help argument functionality"""
        with patch.object(sys, "argv", ["hello.py", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Help should exit with code 0
            assert exc_info.value.code == 0

            captured = capsys.readouterr()
            assert "GitHub CLI practice script" in captured.out
            assert "--name" in captured.out
            assert "--verbose" in captured.out

    @pytest.mark.parametrize(
        "name,expected",
        [
            ("Python", "Hello, Python!"),
            ("世界", "Hello, 世界!"),
            ("123", "Hello, 123!"),
            ("", "Hello, !"),
        ],
    )
    def test_various_names(self, capsys, name, expected):
        """Test main function with various name inputs"""
        with patch.object(sys, "argv", ["hello.py", "--name", name]):
            main()

        captured = capsys.readouterr()
        assert expected in captured.out


class TestArgumentParsing:
    """Test cases for command line argument parsing"""

    def test_invalid_argument(self, capsys):
        """Test behavior with invalid arguments"""
        with patch.object(sys, "argv", ["hello.py", "--invalid-arg"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Invalid arguments should exit with non-zero code
            assert exc_info.value.code != 0


if __name__ == "__main__":
    pytest.main([__file__])
