# coding:utf-8
"""
Floating Menu Button
浮层菜单按钮组件
"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QIcon
from qfluentwidgets import (
    PrimaryPushButton, RoundMenu, Action, MenuAnimationType,
    FluentIcon as FIF, isDarkTheme, ProgressBar
)
from ..common.language import lang

class FloatingMenuButton(QWidget):
    """浮层菜单按钮"""
    startBuildRequested = Signal()      # Start building signals
    clearAllAreaRequested = Signal()    # Clear all block signals
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.progressBar = None
        self.is_building = False
        self._initUI()
        self._connectSignals()
        self._updatePosition()
    
    def _initUI(self):
        """初始化界面"""
        self.buildButton = PrimaryPushButton()
        self.buildButton.setIcon(FIF.ZIP_FOLDER)
        self.buildButton.setText(lang.get_text("build_zip"))
        self.buildButton.setFixedSize(140, 40)
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.buildButton)
        
        # Set component properties
        self.setFixedSize(140, 40)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # Set the style to float on top
        self.setStyleSheet("""
            FloatingMenuButton {
                background-color: transparent;
            }
        """)
        self.raise_()
    
    def _connectSignals(self):
        """连接信号"""
        # Connect button click event
        self.buildButton.clicked.connect(self._showMenu)

        # Connecting language change signals
        lang.languageChanged.connect(self._updateTexts)
    
    def _updateTexts(self):
        """更新文本"""
        self.buildButton.setText(lang.get_text("build_zip"))
    
    def _showMenu(self):
        """显示菜单"""
        menu = RoundMenu(parent=self)
        button_width = self.buildButton.width()
        menu_width = button_width - 10
        menu.setFixedWidth(menu_width)
        start_build_action = Action(FIF.ZIP_FOLDER, lang.get_text("start_build"))
        menu.addAction(start_build_action)
        menu.addSeparator()
        clear_all_action = Action(FIF.BROOM, lang.get_text("clear_all_area"))
        menu.addAction(clear_all_action)
        
        # Connect menu item signal
        start_build_action.triggered.connect(self._onStartBuildClicked)
        clear_all_action.triggered.connect(self.clearAllAreaRequested.emit)
        
        # Get the global position and size of the button
        button_rect = self.buildButton.geometry()
        global_pos = self.mapToGlobal(button_rect.topLeft())
        button_center_x = global_pos.x() + button_rect.width() // 2

        menu.show()
        menu_height = menu.sizeHint().height()
        menu_pos = global_pos
        menu_pos.setX(button_center_x - menu_width // 2)
        menu_pos.setY(global_pos.y() - menu_height - 45)
        menu.hide()
        menu.exec(menu_pos, aniType=MenuAnimationType.DROP_DOWN)
    
    def _updatePosition(self):
        """更新位置到右下角"""
        if self.parent_widget:
            parent_size = self.parent_widget.size()
            x = parent_size.width() - self.width() - 50
            y = parent_size.height() - self.height() - 60
            self.move(x, y)
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        self._updatePosition()
        self._updateProgressBarPosition()
    
    def showEvent(self, event):
        """显示事件"""
        super().showEvent(event)
        self._updatePosition()
        self.raise_()
    
    def updatePosition(self):
        """外部调用更新位置的方法"""
        self._updatePosition()
        self._updateProgressBarPosition()
        self.raise_()
    
    def _onStartBuildClicked(self):
        """开始构筑按钮点击处理"""
        if self.is_building:
            return
        
        # Send the start construction signal.
        self.startBuildRequested.emit()
        
        # Show build progress bar
        self._startProgressBar()
    
    def connectBuildService(self, build_service):
        """连接构建服务"""
        build_service.buildStarted.connect(self._onBuildStarted)
        build_service.progressChanged.connect(self._onProgressChanged)
        build_service.buildCompleted.connect(self._onBuildCompleted)
        build_service.buildFailed.connect(self._onBuildFailed)
    
    def _onBuildStarted(self):
        """构建开始处理"""
        pass
    
    def _onProgressChanged(self, progress: int):
        """进度变化处理"""
        if self.progressBar is not None:
            self.progressBar.setValue(progress)
    
    def _onBuildCompleted(self, output_path: str):
        """构建完成处理"""
        self._finishProgress()
    
    def _onBuildFailed(self, error_msg: str):
        """构建失败处理"""
        self._finishProgress()
    
    def _startProgressBar(self):
        """开始显示进度条"""
        if self.progressBar is not None:
            return
        
        self.is_building = True
        self.progressBar = ProgressBar(self.parent_widget)
        button_width = self.buildButton.width()
        self.progressBar.setFixedSize(button_width, 6)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self._updateProgressBarPosition()
        self.progressBar.show()
        self.progressBar.raise_()
    
    def _updateProgressBarPosition(self):
        """更新进度条位置"""
        if self.progressBar is None:
            return

        button_pos = self.pos()
        button_height = self.height()
        progress_x = button_pos.x()
        progress_y = button_pos.y() + button_height + 10
        
        self.progressBar.move(progress_x, progress_y)
    
    def _finishProgress(self):
        """完成进度"""
        QTimer.singleShot(500, self._hideProgressBar)   # Hide progress bar after 500ms delay
    
    def _hideProgressBar(self):
        """隐藏进度条"""
        if self.progressBar is not None:
            self.progressBar.hide()
            self.progressBar.deleteLater()
            self.progressBar = None
        self.is_building = False