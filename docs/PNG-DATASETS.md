# PNG Datasets

DocUmark can package `.md` files as PNG images for use in AI/ML training pipelines.

## Why PNG?

- PNG is lossless and universally supported across all platforms and OS
- Images are natively understood by multimodal AI models
- PNG files can be organized, versioned, and batched easily
- Binary-encoded PNGs store text compactly without format overhead
- No special reader required — standard image tools work on visual PNGs

## Visual Mode

### What it does
Renders each `.md` file as text on a white canvas using Pillow.
Multi-page documents produce numbered PNGs: `report_visual_001.png`, `report_visual_002.png`, etc.

### Use cases
- Training vision-language models (LLaVA, GPT-4V style, Claude Vision)
- OCR training datasets
- Document layout analysis
- Human-readable dataset inspection

### Example

```bash
documark png ./markdown/ --mode visual --output ./dataset/
```

Output: `dataset/report_visual_001.png` (rendered text at 1200×1600px)

## Binary Mode

### What it does
Encodes the raw UTF-8 bytes of the `.md` file directly into PNG pixel RGB values.
- Each pixel stores 3 bytes (R=byte1, G=byte2, B=byte3)
- Pixel `(0,0)` is a header encoding the total byte length as a 24-bit integer
- Image dimensions are calculated to fit all bytes in a square image
- Remaining pixels padded with black `(0, 0, 0)`

### Use cases
- Lossless text storage in image format
- Binary dataset archives for ML pipelines
- Compact format for large text corpora
- Interoperability with image-native storage systems

### Decoding

```bash
documark decode ./dataset/report_binary.png --output ./recovered/
```

This recovers the **exact** original `.md` file, byte-for-byte.

### Technical Details

For a file of `N` UTF-8 bytes:
- `side = ceil(sqrt((N + 3) / 3)) + 1`  (square image)
- `pixels[0] = (N >> 16, (N >> 8) & 0xFF, N & 0xFF)`  (header)
- `pixels[1 + i//3] = (byte_i, byte_{i+1}, byte_{i+2})`  (data)

Maximum file size: `(side² - 1) * 3` bytes per image (~16 TB theoretical max for a 65535×65535 PNG).

## Both Modes

```bash
documark png ./markdown/ --mode both --output ./dataset/
```

Produces both a visual and a binary PNG for each `.md` file:
- `report_visual_001.png` — rendered image
- `report_binary.png` — pixel-encoded text

## Security Note

PNG encoding does **not** bypass the security layer.
All input `.md` files must have previously passed `check_file()` during conversion.
