import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import patch, MagicMock
from tools.web_search import search_web


class TestWebSearchMocked:
    @patch("tools.web_search.DDGS")
    def test_returns_results(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.return_value = [
            {"title": "Python basics", "body": "Python is a popular language."},
            {"title": "Python tutorial", "body": "Learn Python from scratch."},
        ]
        result = search_web("Python programming")
        assert "Python" in result
        assert isinstance(result, str)

    @patch("tools.web_search.DDGS")
    def test_no_results(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.return_value = []
        result = search_web("asdfghjklqwerty")
        assert "No results" in result

    @patch("tools.web_search.DDGS")
    def test_search_error_handled(self, mock_ddgs_class):
        mock_ddgs = MagicMock()
        mock_ddgs_class.return_value.__enter__ = MagicMock(return_value=mock_ddgs)
        mock_ddgs_class.return_value.__exit__ = MagicMock(return_value=False)
        mock_ddgs.text.side_effect = Exception("network error")
        result = search_web("something")
        assert "failed" in result.lower() or "Error" in result

    def test_empty_query(self):
        result = search_web("   ")
        assert "Error" in result
