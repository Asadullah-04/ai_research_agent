import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from unittest.mock import patch, MagicMock
from agent import run_agent, _dispatch_tool, TOOL_MAP


class TestToolDispatch:
    def test_calculator_dispatch(self):
        result = _dispatch_tool("calculator", {"expression": "5 * 8"})
        assert result == "40"

    def test_unknown_tool(self):
        result = _dispatch_tool("nonexistent_tool", {})
        assert "Error" in result

    def test_file_reader_dispatch_missing(self):
        result = _dispatch_tool("file_reader", {"path": "nowhere.txt"})
        assert "Error" in result


class TestAgentLoop:
    @patch("agent.client")
    def test_simple_end_turn(self, mock_client):
        mock_response = MagicMock()
        mock_response.stop_reason = "end_turn"
        text_block = MagicMock()
        text_block.text = "The capital of France is Paris."
        mock_response.content = [text_block]
        mock_client.messages.create.return_value = mock_response

        result = run_agent("What is the capital of France?", verbose=False)
        assert "Paris" in result

    @patch("agent.client")
    def test_tool_use_then_end(self, mock_client):
        # first response: tool_use
        tool_block = MagicMock()
        tool_block.type = "tool_use"
        tool_block.name = "calculator"
        tool_block.input = {"expression": "3 + 4"}
        tool_block.id = "tool_abc"

        first_response = MagicMock()
        first_response.stop_reason = "tool_use"
        first_response.content = [tool_block]

        # second response: end_turn
        text_block = MagicMock()
        text_block.text = "3 + 4 equals 7."
        second_response = MagicMock()
        second_response.stop_reason = "end_turn"
        second_response.content = [text_block]

        mock_client.messages.create.side_effect = [first_response, second_response]

        result = run_agent("What is 3 + 4?", verbose=False)
        assert "7" in result

    @patch("agent.client")
    def test_no_text_block(self, mock_client):
        mock_response = MagicMock()
        mock_response.stop_reason = "end_turn"
        empty_block = MagicMock(spec=[])  # no .text attribute
        mock_response.content = [empty_block]
        mock_client.messages.create.return_value = mock_response

        result = run_agent("test", verbose=False)
        assert result == "(no text response)"
