import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from tools.file_reader import read_file


class TestMissingFile:
    def test_nonexistent_path(self):
        result = read_file("this_file_does_not_exist.txt")
        assert "Error" in result

    def test_directory_as_path(self, tmp_path):
        result = read_file(str(tmp_path))
        assert "Error" in result


class TestTextFile:
    def test_reads_content(self, tmp_path):
        f = tmp_path / "sample.txt"
        f.write_text("Hello from the test file")
        result = read_file(str(f))
        assert "Hello from the test file" in result

    def test_multiline_content(self, tmp_path):
        f = tmp_path / "multi.txt"
        f.write_text("line one\nline two\nline three")
        result = read_file(str(f))
        assert "line one" in result
        assert "line three" in result

    def test_large_file_truncated(self, tmp_path):
        f = tmp_path / "big.txt"
        f.write_text("x" * 5000)
        result = read_file(str(f))
        assert "truncated" in result


class TestCSVFile:
    def test_reads_csv(self, tmp_path):
        f = tmp_path / "data.csv"
        f.write_text("name,age,city\nAlice,30,Riga\nBob,25,Tallinn\n")
        result = read_file(str(f))
        assert "Alice" in result
        assert "Bob" in result

    def test_empty_csv(self, tmp_path):
        f = tmp_path / "empty.csv"
        f.write_text("")
        result = read_file(str(f))
        assert "empty" in result.lower()

    def test_csv_header_present(self, tmp_path):
        f = tmp_path / "students.csv"
        f.write_text("id,name,grade\n1,Zeeshan,A\n2,Maria,B\n")
        result = read_file(str(f))
        assert "id" in result
        assert "grade" in result
