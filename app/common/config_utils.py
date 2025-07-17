# coding:utf-8
"""
Configuration Utilities
配置文件处理工具
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional, Union


class ConfigPathManager:
    """配置路径管理器 - 处理单文件模式下的配置文件路径"""
    
    def __init__(self):
        self._app_root = self._get_app_root()
        self._config_dir = self._get_config_dir()
        self._cache_dir = self._get_cache_dir()
    
    def _get_app_root(self) -> Path:
        """获取应用程序根目录"""
        if getattr(sys, 'frozen', False):
            # production environment
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller temporary directory (if using PyInstaller)
                return Path(sys.executable).parent
            else:
                # Nuitka single file mode
                return Path(sys.executable).parent
        else:
            # development environment
            return Path(__file__).parent.parent.parent
    
    def _get_config_dir(self) -> Path:
        """获取配置文件目录"""
        if getattr(sys, 'frozen', False):
            config_dir = self._app_root / "app" / "config"
            if not config_dir.exists():
                legacy_config_dir = self._app_root / "config"
                if legacy_config_dir.exists():
                    return legacy_config_dir
            
            return config_dir
        else:
            return self._app_root / "app" / "config"
    
    def _get_cache_dir(self) -> Path:
        """获取缓存目录"""
        if getattr(sys, 'frozen', False):
            return self._app_root / "app" / ".cache"
        else:
            return self._app_root / "app" / ".cache"
    
    @property
    def app_root(self) -> Path:
        """应用程序根目录"""
        return self._app_root
    
    @property
    def config_dir(self) -> Path:
        """配置文件目录"""
        return self._config_dir
    
    @property
    def cache_dir(self) -> Path:
        """缓存目录"""
        return self._cache_dir
    
    def get_config_file(self, filename: str) -> Path:
        """获取配置文件路径"""
        return self.config_dir / filename
    
    def get_cache_file(self, filename: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / filename
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def is_frozen(self) -> bool:
        """检查是否为打包后的环境"""
        return getattr(sys, 'frozen', False)
    
    def get_resource_path(self, resource_name: str) -> Path:
        """获取资源文件路径"""
        if self.is_frozen():
            if hasattr(sys, '_MEIPASS'):
                # PyInstaller
                return Path(sys._MEIPASS) / "Resources" / resource_name
            else:
                # Nuitka
                relative_path = Path("Resources") / resource_name
                if relative_path.exists():
                    return relative_path
                # If the relative path does not exist, try the absolute path
                return self.app_root / "Resources" / resource_name
        else:
            # Development environment
            return self.app_root / "app" / "Resources" / resource_name


class ConfigMigrator:
    """配置迁移工具 - 处理配置文件的迁移和兼容性"""
    
    def __init__(self, path_manager: ConfigPathManager):
        self.path_manager = path_manager
    
    def migrate_legacy_config(self) -> bool:
        """迁移旧版本的配置文件"""
        if not self.path_manager.is_frozen():
            return False
        
        legacy_config_dir = self.path_manager.app_root / "config"
        new_config_dir = self.path_manager.config_dir
        
        if legacy_config_dir.exists() and legacy_config_dir != new_config_dir:
            print(f"检测到旧版本配置目录: {legacy_config_dir}")
            print(f"迁移到新目录: {new_config_dir}")
            
            try:
                new_config_dir.mkdir(parents=True, exist_ok=True)
                migrated_files = []
                for config_file in legacy_config_dir.glob("*.json"):
                    target_file = new_config_dir / config_file.name
                    if not target_file.exists():  # Only copy files that do not exist
                        shutil.copy2(config_file, target_file)
                        migrated_files.append(config_file.name)
                
                if migrated_files:
                    print(f"已迁移配置文件: {', '.join(migrated_files)}")
                    return True
                else:
                    print("没有需要迁移的配置文件")
                    return False
                    
            except Exception as e:
                print(f"配置迁移失败: {e}")
                return False
        
        return False
    
    def create_default_config_if_missing(self, config_filename: str, default_content: str):
        """如果配置文件不存在，创建默认配置"""
        config_file = self.path_manager.get_config_file(config_filename)
        
        if not config_file.exists():
            try:
                self.path_manager.ensure_directories()
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write(default_content)
                print(f"已创建默认配置文件: {config_file}")
            except Exception as e:
                print(f"创建默认配置文件失败: {e}")

_path_manager = None
_config_migrator = None

def get_path_manager() -> ConfigPathManager:
    """获取路径管理器实例（单例）"""
    global _path_manager
    if _path_manager is None:
        _path_manager = ConfigPathManager()
    return _path_manager

def get_config_migrator() -> ConfigMigrator:
    """获取配置迁移器实例（单例）"""
    global _config_migrator
    if _config_migrator is None:
        _config_migrator = ConfigMigrator(get_path_manager())
    return _config_migrator

def initialize_config_system():
    """初始化配置系统"""
    path_manager = get_path_manager()
    migrator = get_config_migrator()
    path_manager.ensure_directories()
    migrator.migrate_legacy_config()
    
    print(f"配置系统初始化完成:")
    print(f"  应用根目录: {path_manager.app_root}")
    print(f"  配置目录: {path_manager.config_dir}")
    print(f"  缓存目录: {path_manager.cache_dir}")
    print(f"  运行模式: {'打包模式' if path_manager.is_frozen() else '开发模式'}")

if __name__ == "__main__":
    initialize_config_system()