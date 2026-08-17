#!/usr/bin/env bash
# Configure Redrix HI556 (H8B5) full-res raw pipeline and bridge to v4l2loopback.
set -e
media-ctl -d /dev/media0 -V '"hi556 2-0020":0[fmt:SGRBG10_1X10/2592x1944]'
media-ctl -d /dev/media0 -V '"Intel IPU6 CSI2 2":0[fmt:SGRBG10_1X10/2592x1944]'
media-ctl -d /dev/media0 -V '"Intel IPU6 CSI2 2":1[fmt:SGRBG10_1X10/2592x1944]'
exec /usr/bin/gst-launch-1.0 v4l2src device=/dev/video16 ! video/x-bayer,format=grbg10le,width=2592,height=1944,framerate=30/1 ! bayer2rgb ! videoconvert ! videoscale ! video/x-raw,format=YUY2,width=640,height=480 ! v4l2sink device=/dev/video42 sync=false
