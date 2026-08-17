#!/usr/bin/env bash
# Clean IPU6/HI556 camera diagnostic - run after reboot, before any hacks.
# Goal: capture raw Bayer directly from the IPU6 ISYS node and verify the data.
set -euo pipefail

echo "==> 1. Check modules"
lsmod | grep -E 'hi556|ipu6' || true

echo "==> 2. Show media topology for hi556"
media-ctl -d /dev/media0 -p 2>&1 | sed -n '/hi556 2-0020/,/^$/p'

echo "==> 3. Set a known raw format (GRBG 1296x972)"
# Adjust entity names if needed.
media-ctl -d /dev/media0 -V '"hi556 2-0020":0[fmt:SRGGB10_1X10/1296x972]' || true
media-ctl -d /dev/media0 -V '"hi556 2-0020":0[fmt:SGRBG10_1X10/1296x972]' || true

echo "==> 4. Capture raw frame from the ISYS node linked to hi556"
# The node is usually video16 on Redrix; find it dynamically.
NODE=$(media-ctl -d /dev/media0 -p 2>&1 | awk '/Intel IPU6 ISYS Capture 16/{print "video16"; exit}')
echo "Using /dev/$NODE"
rm -f /tmp/raw_bayer.raw
timeout 10 v4l2-ctl -d /dev/$NODE --set-fmt-video=width=1296,height=972,pixelformat=BG10 --stream-mmap --stream-count=1 --stream-to=/tmp/raw_bayer.raw 2>&1 || true
ls -lh /tmp/raw_bayer.raw 2>&1 || true

echo "==> 5. If capture failed, try video16 directly with common Bayer formats"
for fmt in BG10 GR10 RG10 GB10; do
  echo "--- try $fmt ---"
  timeout 5 v4l2-ctl -d /dev/video16 --set-fmt-video=width=1296,height=972,pixelformat=$fmt --stream-mmap --stream-count=1 --stream-to=/tmp/raw_$fmt.raw 2>&1 | head -5 && ls -lh /tmp/raw_$fmt.raw 2>/dev/null || true
done

echo "==> Done. Send me /tmp/raw_bayer.raw or the output above."
