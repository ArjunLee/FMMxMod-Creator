# coding:utf-8
"""
Configuration
应用程序配置管理
"""

import json
import os
import sys
import winreg
from pathlib import Path
from typing import Any, Dict
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from .config_utils import get_path_manager, initialize_config_system

def get_desktop_path():
    """获取用户真实的桌面路径，支持自定义桌面位置"""
    try:
        # Try to get the user's desktop path from regedit
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                           r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
            desktop_path, _ = winreg.QueryValueEx(key, "Desktop")
            return Path(desktop_path)
    except (OSError, FileNotFoundError):
        # If the registry read fails, fallback to the default method
        return Path.home() / "Desktop"

class Config(QObject):
    """配置管理器"""
    configChanged = Signal(str, object)  # Configuration item change signal
    
    def __init__(self):
        super().__init__()
        # Initialize the configuration system
        initialize_config_system()
        
        # Use the configuration path manager
        self.path_manager = get_path_manager()
        self.config_file = self.path_manager.get_config_file("app_config.json")
        
        # Load the configuration
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        # Get the user's desktop as the default construction directory (support custom desktop position)
        desktop_path = get_desktop_path()
        default_build_dir = str(desktop_path)
        
        # Get %appdata%\FMM x MOD Creator\.cache\ as the default cache directory
        appdata_path = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
        default_cache_dir = str(appdata_path / "FMM x MOD Creator" / ".cache")
        default_config = {
            "theme_mode": "Dark",
            "window_width": 1600,
            "window_height": 950,
            "window_position": None,
            "mica_enabled": True,
            "language": "zh_CN",
            "theme_color": "bichun_green",
            "theme_color_hex": "#10893E",
            "last_output_dir": "",
            "mod_name": "",
            "mod_version": "",
            "mod_author": "",
            "mod_category": "",
            "build_directory": default_build_dir,
            "cache_directory": default_cache_dir,
            "cache_enabled": True,
            "build_type": "zip",
            "edit_tips_shown": False,
            "qfluent_theme_color": "#ff10893E",
            "qfluent_theme_mode": "Dark"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                default_config.update(loaded_config)
            except Exception as e:
                print(f"加载配置文件失败: {e}，使用默认配置")
        
        return default_config
    
    def _save_config(self):
        """保存配置文件"""
        try:
            self.config_file.parent.mkdir(exist_ok=True)
            # Create a serializable copy of the configuration
            serializable_config = {}
            for key, value in self._config.items():
                # Check if it is an OptionsConfigItem object
                if hasattr(value, 'value'):
                    serializable_config[key] = value.value
                else:
                    serializable_config[key] = value
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default=None) -> Any:
        """获取配置项"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置项"""
        old_value = self._config.get(key)
        if old_value != value:
            self._config[key] = value
            self._save_config()
            self.configChanged.emit(key, value)
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self._config.copy()
    
    def reset(self):
        """重置配置"""
        if self.config_file.exists():
            self.config_file.unlink()
        self._config = self._load_config()
        self.configChanged.emit("reset", None)
    
    # Configuration Item Property Accessor
    @property
    def windowWidth(self):
        return self.get("window_width", 1000)
    
    @property
    def windowHeight(self):
        return self.get("window_height", 800)
    
    @windowHeight.setter
    def windowHeight(self, value):
        self.set("window_height", value)
    
    @property
    def buildDirectory(self):
        build_dir = self.get("build_directory", "")
        if not build_dir or not build_dir.strip():
            # If the configuration is empty, return to the user's desktop folder
            desktop_path = get_desktop_path()
            return str(desktop_path)
        return build_dir
    
    @buildDirectory.setter
    def buildDirectory(self, value):
        self.set("build_directory", value)
    
    @property
    def cacheDirectory(self):
        cache_dir = self.get("cache_directory", "")
        if not cache_dir or not cache_dir.strip():
            # If configured as null, return% appdata%\ FMM x MOD Creator\ .cache\ folder
            appdata_path = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            return str(appdata_path / "FMM x MOD Creator" / ".cache")
        return cache_dir
    
    @cacheDirectory.setter
    def cacheDirectory(self, value):
        self.set("cache_directory", value)
    
    @property
    def cacheEnabled(self):
        return self.get("cache_enabled", True)
    
    @cacheEnabled.setter
    def cacheEnabled(self, value):
        self.set("cache_enabled", value)
    
    @property
    def buildType(self):
        return self.get("build_type", "zip")
    
    @buildType.setter
    def buildType(self, value):
        self.set("build_type", value)
    
    @property
    def micaEnabled(self):
        return self.get("mica_enabled", True)
    
    @property
    def themeMode(self):
        return self.get("theme_mode", "Auto")
    
    @property
    def language(self):
        return self.get("language", "zh_CN")
    
    @property
    def themeColor(self):
        return self.get("theme_color", "turquoise")
    
    @property
    def editTipsShown(self):
        return self.get("edit_tips_shown", False)
    
    @editTipsShown.setter
    def editTipsShown(self, value):
        self.set("edit_tips_shown", value)

cfg = Config()