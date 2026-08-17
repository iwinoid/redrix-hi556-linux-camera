#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 摄像头服务托盘程序
# 打开后自动启动 camera-bridge.service，退出时自动停止。

import subprocess
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon, QPainter, QColor, QPixmap
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QMessageBox

SERVICE = "camera-bridge.service"


def run_systemctl(*args):
    subprocess.run(["systemctl", "--user", *args], check=False)


def service_is_active():
    ret = subprocess.run(
        ["systemctl", "--user", "is-active", SERVICE],
        capture_output=True, text=True
    )
    return ret.stdout.strip() == "active"


def make_icon(active: bool) -> QIcon:
    pix = QPixmap(64, 64)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    color = QColor("#2ecc71") if active else QColor("#e74c3c")
    p.setBrush(color)
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(4, 4, 56, 56)
    # 简易摄像头形状
    p.setBrush(QColor("white"))
    p.drawRoundedRect(18, 24, 28, 20, 3, 3)
    p.drawRoundedRect(40, 30, 8, 8, 2, 2)
    p.end()
    return QIcon(pix)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("摄像头服务")
    app.setQuitOnLastWindowClosed(False)

    tray = QSystemTrayIcon()
    tray.setToolTip("摄像头服务")

    menu = QMenu()

    status_action = QAction("状态：未知")
    status_action.setEnabled(False)
    menu.addAction(status_action)

    start_action = QAction("启动摄像头服务")
    stop_action = QAction("停止摄像头服务")
    quit_action = QAction("退出（并停止服务）")

    menu.addAction(start_action)
    menu.addAction(stop_action)
    menu.addSeparator()
    menu.addAction(quit_action)

    tray.setContextMenu(menu)

    def refresh():
        active = service_is_active()
        status_action.setText("状态：运行中" if active else "状态：已停止")
        tray.setIcon(make_icon(active))
        tray.setToolTip("摄像头服务：运行中" if active else "摄像头服务：已停止")

    def start():
        run_systemctl("start", SERVICE)
        refresh()
        tray.showMessage("摄像头服务", "摄像头桥接已启动", QSystemTrayIcon.MessageIcon.Information, 2000)

    def stop():
        run_systemctl("stop", SERVICE)
        refresh()
        tray.showMessage("摄像头服务", "摄像头桥接已停止", QSystemTrayIcon.MessageIcon.Information, 2000)

    def quit_app():
        run_systemctl("stop", SERVICE)
        tray.hide()
        app.quit()

    start_action.triggered.connect(start)
    stop_action.triggered.connect(stop)
    quit_action.triggered.connect(quit_app)

    # 打开后自动启动
    start()
    tray.show()
    refresh()

    # 防止托盘不可用时直接退出
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "摄像头服务", "当前系统没有可用系统托盘。")
        return 1

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
