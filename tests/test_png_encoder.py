import os
import tempfile
from documark.png_encoder import encode_png, decode_png


def test_binary_encode_decode_roundtrip():
    md_content = "# Test\n\nHello, DocUmark! Binary encoding roundtrip.\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = os.path.join(tmpdir, "test.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        png_paths = encode_png(md_path, tmpdir, mode="binary")
        assert len(png_paths) == 1
        assert png_paths[0].endswith("_binary.png")

        recovered_dir = os.path.join(tmpdir, "recovered")
        recovered_path = decode_png(png_paths[0], recovered_dir)

        with open(recovered_path, encoding="utf-8") as f:
            recovered = f.read()

        assert recovered == md_content


def test_visual_encode_creates_png():
    md_content = "# Visual Test\n\nRendered page.\n"
    with tempfile.TemporaryDirectory() as tmpdir:
        md_path = os.path.join(tmpdir, "visual.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        png_paths = encode_png(md_path, tmpdir, mode="visual")
        assert len(png_paths) >= 1
        assert all(p.endswith(".png") for p in png_paths)
        assert all(os.path.exists(p) for p in png_paths)
