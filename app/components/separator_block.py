# coding:utf-8
"""
Separator Block
分割线区块组件
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton
)
from PySide6.QtCore import Signal, Qt, QPoint
from PySide6.QtGui import QIcon, QPainter, QPen
from PySide6.QtSvgWidgets import QSvgWidget
from pathlib import Path
from qfluentwidgets import (
    CardWidget, BodyLabel, PrimaryToolButton, ToolButton, TransparentToolButton, LineEdit,
    FluentIcon as FIF, isDarkTheme
)
from ..common.language import lang
from ..common.config import cfg


class SeparatorBlock(CardWidget):
    """分割线区块"""
    deleteRequested = Signal()
    copyRequested = Signal()
    moveRequested = Signal()
    dragStarted = Signal(object)
    dragMoved = Signal(object, object)
    dragEnded = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_dragging = False
        self.drag_start_pos = None
        self._initWidgets()
        self._connectSignals()
        self._updateMoveButtonIcon()
        self._updateSeparatorLines()
    
    def _initWidgets(self):
        """初始化组件"""
        self.setBorderRadius(8)
        self.setFixedHeight(50)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(20, 0, 15, 0)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.separatorLineLeft = self._createSeparatorLine()
        self.separatorNameEdit = LineEdit(self)
        self.separatorNameEdit.setPlaceholderText(lang.get_text("separator_name_placeholder"))
        self.separatorNameEdit.setFixedHeight(30)
        self.separatorNameEdit.setFixedWidth(200)
        self.separatorNameEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.separatorLineRight = self._createSeparatorLine()
        self._createActionButtons()

        # Create a container to center the divider element
        center_widget = QWidget()
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(10)
        center_layout.addWidget(self.separatorLineLeft)
        center_layout.addWidget(self.separatorNameEdit)
        center_layout.addWidget(self.separatorLineRight)
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add components to the main layout
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(center_widget)
        self.mainLayout.addStretch(1)
        
        # Create action button containers, unify button layout and spacing
        self.mainLayout.addWidget(self.moveBtn)
        self.mainLayout.addSpacing(4)
        self.mainLayout.addWidget(self.copyBtn)
        self.mainLayout.addSpacing(4)
        self.mainLayout.addWidget(self.deleteBtn)

    def _createSeparatorLine(self):
        """创建横杠标签"""
        line = QLabel(self)
        line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        return line
    
    def _updateSeparatorLines(self):
        """更新分割线长度，根据界面宽度自适应"""
        if not hasattr(self, 'separatorLineLeft') or not hasattr(self, 'separatorLineRight'):
            return
            
        # Calculate the available width
        total_width = self.width()
        input_width = self.separatorNameEdit.width()
        button_width = 28 * 3 + 4 * 2
        margins = 20 + 15
        spacing = 10 * 2
        available_width = total_width - input_width - button_width - margins - spacing
        line_width = max(available_width // 2, 50)
        line_count = max(line_width // 8, 6)
        line_text = "-" * line_count
        
        self.separatorLineLeft.setText(line_text)
        self.separatorLineRight.setText(line_text)
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        self._updateSeparatorLines()
    
    def _createActionButtons(self):
        """创建操作按钮"""
        self.moveBtn = TransparentToolButton(self)
        self._updateMoveButtonIcon()
        self.moveBtn.setFixedSize(28, 28)
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
        self.copyBtn = TransparentToolButton(FIF.COPY, self)
        self.copyBtn.setFixedSize(28, 28)
        self.copyBtn.setToolTip(lang.get_text("copy_separator_block"))

        from qfluentwidgets import PrimaryToolButton
        self.deleteBtn = PrimaryToolButton(FIF.DELETE, self)
        self.deleteBtn.setFixedSize(28, 28)
        self.deleteBtn.setToolTip(lang.get_text("delete_separator_block"))
  
    def _connectSignals(self):
        """连接信号"""
        self.deleteBtn.clicked.connect(self.deleteRequested.emit)
        self.copyBtn.clicked.connect(self.copyRequested.emit)
        self.moveBtn.mousePressEvent = self._moveBtnMousePressEvent
        self.moveBtn.mouseMoveEvent = self._moveBtnMouseMoveEvent
        self.moveBtn.mouseReleaseEvent = self._moveBtnMouseReleaseEvent
        lang.languageChanged.connect(self._updateTexts)
        cfg.configChanged.connect(self._onConfigChanged)
    
    def _updateMoveButtonIcon(self):
        """更新移动按钮图标"""
        from ..common.application import FMMApplication
        if isDarkTheme():
            icon_path = FMMApplication.getResourcePath("Drag_and_drop_white.svg")
        else:
            icon_path = FMMApplication.getResourcePath("Drag_and_drop_black.svg")
        
        if icon_path.exists():
            self.moveBtn.setIcon(QIcon(str(icon_path)))
        else:
            self.moveBtn.setIcon(FIF.DRAG)
    
    def _onConfigChanged(self, key):
        """配置变化处理"""
        if key == "themeMode":
            self._updateMoveButtonIcon()
    
    def _moveBtnMousePressEvent(self, event):
        """移动按钮鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = event.globalPosition().toPoint()
            self.moveBtn.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.dragStarted.emit(self)
    
    def _moveBtnMouseMoveEvent(self, event):
        """移动按钮鼠标移动事件"""
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.dragMoved.emit(self, event.globalPosition().toPoint())
    
    def _moveBtnMouseReleaseEvent(self, event):
        """移动按钮鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_dragging:
            self.is_dragging = False
            self.drag_start_pos = None
            self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self.dragEnded.emit(self)
    
    def _updateTexts(self):
        """更新文本"""
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.copyBtn.setToolTip(lang.get_text("copy_separator_block"))
        self.deleteBtn.setToolTip(lang.get_text("delete_separator_block"))
        self.separatorNameEdit.setPlaceholderText(lang.get_text("separator_name_placeholder"))
    
    def getSeparatorData(self):
        """获取分割线数据"""
        return {
            "separator_name": self.separatorNameEdit.text()
        }
    
    def setSeparatorData(self, data):
        """设置分割线数据"""
        if "separator_name" in data:
            self.separatorNameEdit.setText(data["separator_name"])