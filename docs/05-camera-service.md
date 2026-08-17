# On-Demand Camera Service

## Purpose

Start the camera bridge only when needed, so the camera is not always powered.

## Tray application

`camera-service/camera-service.py` is a PyQt6 system tray app.

- On launch, it starts `camera-bridge.service`.
- It shows a green/red tray icon for running/stopped state.
- Right-click menu can start/stop the service or quit (which stops it).

## Install

```bash
sudo cp camera-service/camera-service.py /usr/local/bin/camera-service
sudo chmod 755 /usr/local/bin/camera-service
sudo cp camera-service/camera-service.desktop /usr/share/applications/
```

## Usage

Open "Camera Service" (or "摄像头服务" in Chinese locales) from the application menu. The camera bridge starts. Use the tray menu to stop or exit.
