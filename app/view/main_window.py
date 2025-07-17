# coding:utf-8
"""
Main Window
主窗口模块
"""
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from pathlib import Path
from qfluentwidgets import (
    FluentIcon as FIF, NavigationItemPosition,
    FluentWindow, SplashScreen, setTheme, Theme
)
from .home_interface import HomeInterface
from .mod_list_interface import ModListInterface
from .settings_interface import SettingsInterface
from ..common.config import cfg
from ..common.language import lang

class MainWindow(FluentWindow):
    """主窗口"""
    def __init__(self):
        super().__init__()
        
        # Create subinterface
        self.homeInterface = HomeInterface(self)
        self.modListInterface = ModListInterface(self)
        self.settingsInterface = SettingsInterface(self)

        # navigation item
        self.home_item = None
        self.mod_list_item = None
        self.settings_item = None
        
        self._initWindow()
        self._initNavigation()
        self._connectSignals()
        
        # Create a splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()
        
        self.show()
        
        # Close the splash screen
        QApplication.processEvents()
        self.splashScreen.finish()
        
        # Initialize language settings
        saved_language = cfg.get("language", "zh_CN")
        lang.set_language(saved_language)
        
        # Initialize theme settings
        self._initTheme()
    
    def _initWindow(self):
        """初始化窗口"""
        self.resize(cfg.windowWidth, cfg.windowHeight)
        self.setWindowTitle(lang.get_text("main_window_title"))
        
        # Set Icon
        from ..common.application import FMMApplication
        icon_path = FMMApplication.getResourcePath("FMMxModCreator_Icon_512.png")
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Set minimum size
        self.setMinimumSize(800, 600)
        
        # Center display
        desktop = QApplication.primaryScreen().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        
        # Set mica style
        self.setMicaEffectEnabled(cfg.get("mica_enabled", True))
    
    def _initNavigation(self):
        """初始化导航"""
        # Top navigation item
        self.home_item = self.addSubInterface(self.homeInterface, FIF.HOME, lang.get_text("home"))
        self.navigationInterface.addSeparator()
        self.mod_list_item = self.addSubInterface(self.modListInterface, FIF.FOLDER, lang.get_text("mod_list"))

        # Bottom navigation item
        self.settings_item = self.addSubInterface(
            self.settingsInterface,
            FIF.SETTING,
            lang.get_text("settings"),
            position=NavigationItemPosition.BOTTOM
        )
        
        # Set navigation menu width (default not expanded)
        self.navigationInterface.setExpandWidth(250)
        
        # Remove navigation background color
        self.navigationInterface.setStyleSheet("""
            NavigationInterface {
                background-color: transparent;
                border: none;
            }
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
        
        # Set default interface
        self.switchTo(self.homeInterface)
    
    def _connectSignals(self):
        """连接信号"""
        lang.languageChanged.connect(self._updateNavigationTexts)
    
    def _updateNavigationTexts(self):
        """更新导航文本"""
        self.setWindowTitle(lang.get_text("main_window_title"))

        # Update navigation item text
        if self.home_item:
            self.home_item.setText(lang.get_text("home"))
        if self.mod_list_item:
            self.mod_list_item.setText(lang.get_text("mod_list"))
        if self.settings_item:
            self.settings_item.setText(lang.get_text("settings"))
    
    def resizeEvent(self, e):
        """窗口大小改变事件"""
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())
    
    def focusOutEvent(self, event):
        """窗口失去焦点事件"""
        if hasattr(self.homeInterface, 'dragging_block') and self.homeInterface.dragging_block:
            self.homeInterface.dragging_block.setStyleSheet("")
            self.homeInterface.dragging_block.is_dragging = False
            self.homeInterface.dragging_block.drag_start_pos = None
            self.homeInterface.dragging_block.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self.homeInterface._cleanupDrag()
        super().focusOutEvent(event)
    
    def _initTheme(self):
        """初始化主题设置"""
        theme_mode = cfg.get("theme_mode", "Auto")
        
        # Apply theme
        if theme_mode == "Auto":
            setTheme(Theme.AUTO)
        elif theme_mode == "Light":
            setTheme(Theme.LIGHT)
        elif theme_mode == "Dark":
            setTheme(Theme.DARK)
    
    def closeEvent(self, e):
        """关闭事件"""
        # Save window size
        cfg.set("window_width", self.width())
        cfg.set("window_height", self.height())
        
        super().closeEvent(e)