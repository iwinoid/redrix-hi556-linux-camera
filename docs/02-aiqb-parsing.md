# Extracting Color Calibration from Intel AIQB

## Background

Intel ships per-sensor calibration data in proprietary `.aiqb` files. The HI556 H8B5 module uses:

```text
HI556_H8B5_ADL.aiqb
```

This file contains CCMs and AWB chromaticity data needed for correct colors.

## Parser

Use the included script:

```bash
python3 tools/parse_aiqb.py calibration/HI556_H8B5_ADL.aiqb --sensor-name hi556-h8b5
```

It walks the AIQB record chain and prints:

- Sensor resolution and bit depth
- Base ISO
- Advanced color matrices (record id=25)
- AWB gain limits

It also writes a libcamera Simple IPA YAML file.

## Result

The generated file is:

```text
calibration/hi556-h8b5.yaml
```

It contains 7 CCM entries from 2375K to 14445K and matching AWB colour gains.

## Source

The parser is based on:

- https://patchwork.libcamera.org/patch/26716/
- https://jetm.github.io/blog/posts/ipu6-aiqb-calibration/
