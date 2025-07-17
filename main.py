# coding:utf-8
"""
FMMxMOD Creator - Main Entry Point
基于Fluent Design的FMM MOD创作工具主入口
"""

import os
import sys
from pathlib import Path

# 设置工作目录
os.chdir(Path(__file__).resolve().parent)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from app.common.application import FMMApplication
from app.view.main_window import MainWindow
from PySide6.QtGui import QIcon


def main():
    """主函数"""
    # 启用高DPI缩放
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    
    # 创建应用程序
    app = FMMApplication(sys.argv)
    
    # 设置应用程序图标
    icon_path = app.getResourcePath("FMMxModCreator_Icon_512.png")
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()