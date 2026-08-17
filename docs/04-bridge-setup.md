# Raw V4L2 to Virtual Camera Bridge

## Why

A V4L2 consumer (e.g. a video conferencing app) expects a standard capture device. The raw sensor node `/dev/video16` is not directly usable.

This bridge converts raw Bayer to YUYV and exposes it through v4l2loopback as `/dev/video42`.

## Pipeline

```text
/dev/video16 raw Bayer (2592x1944 GRBG10)
  -> bayer2rgb
  -> videoconvert
  -> videoscale
  -> YUYV 640x480
  -> /dev/video42
```

## Service file

`camera-service/camera-bridge.service`:

```ini
[Unit]
Description=Clean HI556 H8B5 raw V4L2 to v4l2loopback bridge
After=default.target

[Service]
Type=simple
ExecStart=/usr/local/bin/clean-camera-bridge.sh
Restart=on-failure
RestartSec=3

[Install]
WantedBy=default.target
```

## Script

`camera-service/clean-camera-bridge.sh` configures the media pipeline and starts GStreamer.

## v4l2loopback

Load with:

```bash
sudo modprobe v4l2loopback video_nr=42 card_label="Clean HI556" exclusive_caps=1 max_buffers=8 max_openers=10
```

## Test

```bash
ffplay -f v4l2 -input_format yuyv422 -video_size 640x480 /dev/video42
```
