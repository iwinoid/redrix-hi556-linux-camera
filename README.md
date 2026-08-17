# Redrix HI556 Linux Camera

Enable the Intel IPU6 HI556 camera on an HP Elite Dragonfly Chromebook (Redrix) running Linux.

This repository documents a working path from a camera that outputs garbage/color-shifted frames to a usable V4L2 camera, using:

- The OEM Windows driver as a source of sensor initialization registers.
- `parse_aiqb.py` to extract color calibration from Intel's proprietary AIQB tuning file.
- A raw V4L2 + `bayer2rgb` pipeline to bypass broken libcamera software ISP behavior.
- A small tray application to start/stop the camera bridge on demand.

## What's inside

```
docs/                   Detailed write-ups
tools/                  Helper scripts
drivers/                Patched Linux hi556 driver source and prebuilt module
calibration/            AIQB file, generated YAML, register tables
windows-driver/         Original OEM Windows driver package (renamed)
camera-service/         On-demand camera bridge service and tray app
```

## Quick start

1. Install the patched `hi556` module (see `docs/03-patching-linux-driver.md`).
2. Set up the bridge (see `docs/04-bridge-setup.md`).
3. Use the tray app to start/stop the camera on demand (see `docs/05-camera-service.md`).

## Credits

- `tools/parse_aiqb.py` is based on the libcamera patch by Javier Tia:
  https://patchwork.libcamera.org/patch/26716/
- Blog write-up:
  https://jetm.github.io/blog/posts/ipu6-aiqb-calibration/
- Original Intel IPU6 camera HAL and drivers:
  https://github.com/intel/ipu6-camera-hal
  https://github.com/intel/ipu6-drivers

## License

Respect the licenses of individual components:

- Linux kernel driver code: GPL-2.0
- `parse_aiqb.py`: GPL-2.0-or-later
- OEM Windows driver: proprietary, included for interoperability research
