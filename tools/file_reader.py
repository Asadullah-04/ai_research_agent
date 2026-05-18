import os
import csv

MAX_TEXT_CHARS = 3000
MAX_CSV_ROWS = 60


def read_file(path: str) -> str:
    path = path.strip()

    if not os.path.exists(path):
        return f"Error: file '{path}' does not exist"

    if not os.path.isfile(path):
        return f"Error: '{path}' is not a file"

    _, ext = os.path.splitext(path)
    ext = ext.lower()

    try:
        if ext == ".csv":
            return _read_csv(path)
        else:
            return _read_text(path)
    except PermissionError:
        return f"Error: permission denied for '{path}'"
    except UnicodeDecodeError:
        return f"Error: could not decode file '{path}' as UTF-8"
    except Exception as e:
        return f"Error reading file: {e}"


def _read_text(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        content = f.read(MAX_TEXT_CHARS)
    if len(content) == MAX_TEXT_CHARS:
        content += f"\n... [truncated at {MAX_TEXT_CHARS} characters]"
    return content


def _read_csv(path: str) -> str:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i >= MAX_CSV_ROWS:
                rows.append(f"... [truncated, showing first {MAX_CSV_ROWS} rows]")
                break
            rows.append(", ".join(row))
    if not rows:
        return "File is empty"
    return "\n".join(rows)
