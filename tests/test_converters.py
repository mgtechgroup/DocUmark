import os
import tempfile
from documark.converters.txt import convert as txt_convert
from documark.optimizer import optimize


def test_txt_convert_adds_h1():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("My Title\nSome body text.")
        tmp = f.name
    try:
        result = txt_convert(tmp)
        assert result.startswith("# My Title")
        assert "Some body text." in result
    finally:
        os.unlink(tmp)


def test_txt_convert_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("")
        tmp = f.name
    try:
        result = txt_convert(tmp)
        assert isinstance(result, str)
    finally:
        os.unlink(tmp)
