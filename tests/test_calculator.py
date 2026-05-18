import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from tools.calculator import calculate


class TestBasicArithmetic:
    def test_addition(self):
        assert calculate("2 + 3") == "5"

    def test_subtraction(self):
        assert calculate("10 - 4") == "6"

    def test_multiplication(self):
        assert calculate("6 * 7") == "42"

    def test_division(self):
        assert calculate("10 / 4") == "2.5"

    def test_power(self):
        assert calculate("2 ** 10") == "1024"

    def test_modulo(self):
        assert calculate("17 % 5") == "2"


class TestComplexExpressions:
    def test_parentheses(self):
        assert calculate("(3 + 7) * 2") == "20"

    def test_nested_parentheses(self):
        assert calculate("(2 + (3 * 4)) - 1") == "13"

    def test_unary_minus(self):
        assert calculate("-5 + 10") == "5"

    def test_float_result(self):
        assert calculate("1 / 3") == "0.3333333333"

    def test_integer_float(self):
        # 4.0 should display as 4, not 4.0
        assert calculate("8 / 2") == "4"


class TestErrorHandling:
    def test_division_by_zero(self):
        result = calculate("5 / 0")
        assert "Error" in result

    def test_invalid_expression(self):
        result = calculate("hello world")
        assert "Error" in result

    def test_code_injection_attempt(self):
        result = calculate("__import__('os').system('ls')")
        assert "Error" in result

    def test_empty_string(self):
        result = calculate("")
        assert "Error" in result
