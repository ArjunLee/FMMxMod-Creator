# coding:utf-8
"""
Application
应用程序主类
"""

import os
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from qfluentwidgets import setTheme, Theme, setThemeColor, FluentThemeColor

from .config import cfg
from .language import lang
from . import version_info


class FMMApplication(QApplication):
    """FMM应用程序类"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        self.setApplicationName(version_info.APP_NAME)
        self.setApplicationVersion(version_info.VERSION_STRING)
        self.setOrganizationName("FMM Tools")
        self.setOrganizationDomain("fmm-tools.com")
        self._initTheme()
        self._initLanguage()
        self._initFont()
    
    @staticmethod
    def getResourcePath(*paths):
        """获取资源文件路径"""
        if getattr(sys, 'frozen', False):
            # The production environment
            app_root = Path(sys.executable).parent
            return app_root / "Resources" / Path(*paths)
        else:
            # The development environment
            app_root = Path(__file__).parent.parent.parent
            return app_root / "app" / "Resources" / Path(*paths)
    
    @staticmethod
    def getConfigPath(*paths):
        """获取配置文件路径"""
        if getattr(sys, 'frozen', False):
            # For a production environment, use exe with/app/config
            if hasattr(sys, '_MEIPASS') or os.environ.get('NUITKA_ONEFILE_PARENT'):
                # PyInstaller or Nuitka single-file mode support
                if os.environ.get('NUITKA_ONEFILE_PARENT'):
                    app_root = Path(os.environ['NUITKA_ONEFILE_PARENT'])
                else:
                    app_root = Path(sys.argv[0]).parent
            else:
                app_root = Path(sys.executable).parent
            return app_root / "app" / "config" / Path(*paths)
        else:
            # The development environment
            app_root = Path(__file__).parent.parent.parent
            return app_root / "app" / "config" / Path(*paths)
    
    def _initTheme(self):
        """初始化主题"""
        # Use the merged configuration, no longer rely on qfluent_config.json
        # Directly use setTheme() and setThemeColor() to set the theme, avoid qconfig automatically saving the configuration file
        
        theme_mode = cfg.get("theme_mode", "Auto")
        # Apply the theme
        if theme_mode == "Auto":
            setTheme(Theme.AUTO)
        elif theme_mode == "Light":
            setTheme(Theme.LIGHT)
        elif theme_mode == "Dark":
            setTheme(Theme.DARK)
        
        # Set the theme color
        theme_color = cfg.get("theme_color", "default")
        
        # Dark mode theme color mapping
        dark_color_map = {
            "haitang_red": "#FF5F91",    # 海棠红
            "jingtai_blue": "#29F7FF",            # 景泰蓝
            "wheat_yellow": "#F9DF70",      # 麦桔黄
            "bichun_green": "#10893E",            # 碧春绿
            "qinglian_purple": "#9583CD",     # 青莲紫
            "lotus_white": "#EFF4F7",       # 莲瓣白
            "default": "#10893E"                  # 默认碧春绿
        }
        # Light mode theme color mapping
        light_color_map = {
            "camellia_red": "#EE3F4E",      # 茶花红
            "gem_blue": "#3946AF",            # 宝石蓝
            "cangshan_yellow": "#FF8C0B",         # 苍山黄
            "mint_green": "#217F4D",        # 薄荷绿
            "lilac_purple": "#635282",      # 丁香紫
            "xuandai_black": "#36353B",       # 玄黛黑
            "default": "#EE3F4E"            # 默认茶花红
        }
        
        # Select the color according to the theme mode
        if theme_mode == "Dark":
            color_hex = dark_color_map.get(theme_color, "#10893E")
        elif theme_mode == "Light":
            color_hex = light_color_map.get(theme_color, "#EE3F4E")
        else:
            color_hex = dark_color_map.get(theme_color, "#10893E")
        
        setThemeColor(color_hex)
    
    def _initLanguage(self):
        """初始化语言"""
        saved_language = cfg.get("language", "zh_CN")
        lang.set_language(saved_language)
    
    def _initFont(self):
        """初始化字体"""
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        self.setFont(font)