# coding:utf-8
"""
Warning Block
警告区块组件
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFileDialog, QPushButton
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtSvgWidgets import QSvgWidget
from pathlib import Path
from qfluentwidgets import (
    GroupHeaderCardWidget, BodyLabel, PrimaryToolButton, ToolButton, PlainTextEdit,
    FluentIcon as FIF, isDarkTheme, TransparentToolButton, LineEdit
)
from ..common.language import lang
from ..common.config import cfg


class WarningImageUploadWidget(QWidget):
    """警告图像上传控件"""
    imageChanged = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = ""
        self.is_hovered = False
        self.setObjectName("WarningImageUploadWidget")
        self._initUI()
        self._setupStyle()
        self._setupAnimation()
    
    def _initUI(self):
        """初始化界面"""
        self.setFixedSize(400, 225)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel = QLabel("+")
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageLabel.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #666;
                border: none;
                background: transparent;
            }
        """)

        layout.addWidget(self.imageLabel)
        self.hintLabel = QLabel(lang.get_text("warning_upload_hint"))
        self.hintLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hintLabel.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #999;
                border: none;
                background: transparent;
            }
        """)

        layout.addWidget(self.hintLabel)

        self.formatLabel = QLabel("JPG, PNG, WEBP")
        self.formatLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.formatLabel.setStyleSheet("""
            QLabel {
                font-size: 10px;
                color: #aaa;
                border: none;
                background: transparent;
            }
        """)

        layout.addWidget(self.formatLabel)

        self.clearBtn = ToolButton(FIF.CLOSE, self)
        self.clearBtn.setFixedSize(24, 24)
        self.clearBtn.setToolTip(lang.get_text("clear_image"))
        self.clearBtn.hide()
        self.clearBtn.clicked.connect(self.clearImage)
    
    def _setupStyle(self):
        """设置样式"""
        from qfluentwidgets import isDarkTheme
        from ..common.config import cfg

        if isDarkTheme():
            self.normal_color = "rgba(255, 255, 255, 0.3)"
            self.hover_color = "rgba(255, 255, 255, 0.6)"
        else:
            self.normal_color = "rgba(0, 0, 0, 0.3)"
            self.hover_color = "rgba(0, 0, 0, 0.6)"
        
        self._updateStyleSheet()

        cfg.configChanged.connect(self._onConfigChanged)
    
    def _setupAnimation(self):
        """设置动画"""
        from PySide6.QtCore import QPropertyAnimation, QEasingCurve

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    
    def _onConfigChanged(self, key, value):
        """配置变化时更新样式"""
        if key == "theme_mode":
            self._setupStyle()
    
    def _updateStyleSheet(self):
        """更新样式表"""
        border_color = self.hover_color if self.is_hovered else self.normal_color
        
        self.setStyleSheet(f"""
            WarningImageUploadWidget {{
                border: 2px dashed {border_color};
                border-radius: 12px;
                background-color: transparent;
            }}
            WarningImageUploadWidget > QLabel {{
                border: none;
                background: transparent;
            }}
        """)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        self.is_hovered = True
        self._updateStyleSheet()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        self.is_hovered = False
        self._updateStyleSheet()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._selectImage()
    
    def _selectImage(self):
        """选择图像"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            lang.get_text("select_image"),
            "",
            "Images (*.jpg *.jpeg *.png *.webp)"
        )
        
        if file_path:
            self.image_path = file_path
            self._displayImage(file_path)
            self.imageChanged.emit(file_path)
    
    def _displayImage(self, file_path):
        """显示图像"""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            target_size = self.size()
            target_size.setWidth(target_size.width() - 20)
            target_size.setHeight(target_size.height() - 20)
            
            scaled_pixmap = pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.imageLabel.setPixmap(scaled_pixmap)
            self.hintLabel.hide()
            self.formatLabel.hide()
            self.clearBtn.show()
            self._positionClearButton()
    
    def clearImage(self):
        """清除图像"""
        self.image_path = ""
        self.imageLabel.clear()
        self.imageLabel.setText("+")
        self.hintLabel.show()
        self.formatLabel.show()
        self.clearBtn.hide()
        self.imageChanged.emit("")
    
    def _positionClearButton(self):
        """定位清除按钮到右上角"""
        self.clearBtn.move(self.width() - 30, 6)
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        if self.image_path:
            self._positionClearButton()
    
    def getImagePath(self):
        """获取图像路径"""
        return self.image_path
    
    def updateTexts(self):
        """更新文本"""
        if not self.image_path:
            self.hintLabel.setText(lang.get_text("warning_upload_hint"))
            self.hintLabel.show()
            self.formatLabel.show()


class WarningBlock(GroupHeaderCardWidget):
    """警告区块"""
    
    deleteRequested = Signal()
    copyRequested = Signal()
    moveRequested = Signal()
    dragStarted = Signal(object)
    dragMoved = Signal(object, object)
    dragEnded = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(lang.get_text("warning_area"))
        self.is_dragging = False
        self.drag_start_pos = None
        self.is_collapsed = False
        self._initWidgets()
        self._connectSignals()
        self._updateMoveButtonIcon()
    
    def _initWidgets(self):
        """初始化组件"""
        self.setBorderRadius(8)
        self._setupCustomHeader()
        self._setupContent()

        self.warningGroup = self.addGroup(
            icon=FIF.INFO,
            title=lang.get_text("warning_area"),
            content=lang.get_text("warning_area_desc"),
            widget=self.contentWidget
        )

        self._customizeHeader()
    
    def _setupCustomHeader(self):
        """设置自定义标题区域"""
        self.collapseBtn = TransparentToolButton(FIF.CHEVRON_DOWN_MED, self)
        self.collapseBtn.setFixedSize(12, 12)
        self.collapseBtn.setToolTip(lang.get_text("collapse_expand"))
        self.areaMarkEdit = LineEdit(self)
        self.areaMarkEdit.setPlaceholderText(lang.get_text("area_mark"))
        self.areaMarkEdit.setFixedWidth(180)
        self.areaMarkEdit.setFixedHeight(32)
        self.moveBtn = TransparentToolButton(self)
        self._updateMoveButtonIcon()
        self.moveBtn.setFixedSize(28, 28)
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
        self.copyBtn = TransparentToolButton(FIF.COPY, self)
        self.copyBtn.setFixedSize(28, 28)
        self.copyBtn.setToolTip(lang.get_text("copy_warning_block"))
        self.deleteBtn = PrimaryToolButton(FIF.DELETE, self)
        self.deleteBtn.setFixedSize(28, 28)
        self.deleteBtn.setToolTip(lang.get_text("delete_warning_block"))
    
    def _customizeHeader(self):
        """自定义标题区域，统一容器逻辑"""
        try:
            main_layout = self.layout()
            if not (main_layout and main_layout.count() > 0):
                self._fallback_customizeHeader()
                return

            title_item = main_layout.itemAt(0)
            if not (title_item and title_item.widget()):
                self._fallback_customizeHeader()
                return

            title_widget = title_item.widget()
            title_layout = title_widget.layout()
            if not title_layout:
                self._fallback_customizeHeader()
                return

            title_widget.setFixedHeight(60)
            title_layout.insertWidget(0, self.collapseBtn)
            title_text = lang.get_text("warning_area")

            title_widget_index = -1
            for i in range(title_layout.count()):
                item = title_layout.itemAt(i)
                widget = item.widget()
                if widget and isinstance(widget, (QLabel, BodyLabel)) and widget.text() == title_text:
                    title_widget_index = i
                    break
            
            if title_widget_index != -1:
                title_layout.insertWidget(title_widget_index + 1, self.areaMarkEdit)
                title_layout.insertSpacing(title_widget_index + 2, 15)
            else:
                title_layout.insertWidget(2, self.areaMarkEdit)
                title_layout.insertSpacing(3, 15)

            title_layout.addStretch()
            
            title_layout.addWidget(self.moveBtn)
            title_layout.addSpacing(4)
            title_layout.addWidget(self.copyBtn)
            title_layout.addSpacing(4)
            title_layout.addWidget(self.deleteBtn)
            
            self._using_fallback_positioning = False

        except Exception as e:
            print(f"自定义标题失败: {e}")
            self._fallback_customizeHeader()

    def _fallback_customizeHeader(self):
        """备用方案：手动定位控件"""
        self.collapseBtn.setParent(self)
        self.areaMarkEdit.setParent(self)
        self.moveBtn.setParent(self)
        self.copyBtn.setParent(self)
        self.deleteBtn.setParent(self)
        self.collapseBtn.show()
        self.areaMarkEdit.show()
        self.moveBtn.show()
        self.copyBtn.show()
        self.deleteBtn.show()
        self.collapseBtn.move(10, 10)
        self.areaMarkEdit.move(40, 8) # 调整位置
        self.moveBtn.move(self.width() - 108, 10)
        self.copyBtn.move(self.width() - 72, 10)
        self.deleteBtn.move(self.width() - 36, 10)
        self._using_fallback_positioning = True
    
    def _setupContent(self):
        """设置内容区域"""
        self.contentWidget = QWidget()
        contentLayout = QHBoxLayout(self.contentWidget)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(15)
        self.imageUpload = WarningImageUploadWidget()
        self.descriptionEdit = PlainTextEdit()
        self.descriptionEdit.setPlaceholderText(lang.get_text("warning_description_placeholder"))
        self.descriptionEdit.setFixedHeight(150)
        self.descriptionEdit.setFixedWidth(400)

        contentLayout.addWidget(self.imageUpload)
        contentLayout.addWidget(self.descriptionEdit, 1)
    
    def _connectSignals(self):
        """连接信号"""
        self.collapseBtn.clicked.connect(self._toggleCollapse)
        self.deleteBtn.clicked.connect(self.deleteRequested.emit)
        self.copyBtn.clicked.connect(self.copyRequested.emit)
        self.moveBtn.mousePressEvent = self._moveBtnMousePressEvent
        self.moveBtn.mouseMoveEvent = self._moveBtnMouseMoveEvent
        self.moveBtn.mouseReleaseEvent = self._moveBtnMouseReleaseEvent

        lang.languageChanged.connect(self._updateTexts)
        cfg.configChanged.connect(self._onConfigChanged)
    
    def _toggleCollapse(self):
        """切换折叠状态"""
        self.is_collapsed = not self.is_collapsed

        if self.is_collapsed:
            self.collapseBtn.setIcon(FIF.CHEVRON_RIGHT_MED)
        else:
            self.collapseBtn.setIcon(FIF.CHEVRON_DOWN_MED)

        from PySide6.QtCore import QPropertyAnimation, QEasingCurve
        
        self.animation = QPropertyAnimation(self.contentWidget, b"maximumHeight")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        if self.is_collapsed:
            self.animation.setStartValue(self.contentWidget.height())
            self.animation.setEndValue(0)
            self.animation.finished.connect(lambda: self.contentWidget.hide())
        else:
            self.contentWidget.show()
            self.contentWidget.setMaximumHeight(0)
            content_height = self.contentWidget.sizeHint().height()
            self.animation.setStartValue(0)
            self.animation.setEndValue(content_height)
            self.animation.finished.connect(lambda: self.contentWidget.setMaximumHeight(16777215))
        
        self.animation.start()
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        if hasattr(self, 'moveBtn') and hasattr(self, '_using_fallback_positioning') and self._using_fallback_positioning:
            self.moveBtn.move(self.width() - 108, 10)
            self.copyBtn.move(self.width() - 72, 10)
            self.deleteBtn.move(self.width() - 36, 10)
    
    def _updateTexts(self):
        """更新文本"""
        self.setTitle(lang.get_text("warning_area"))
        self.descriptionEdit.setPlaceholderText(lang.get_text("warning_description_placeholder"))
        self.imageUpload.updateTexts()
        self.areaMarkEdit.setPlaceholderText(lang.get_text("area_mark"))
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.copyBtn.setToolTip(lang.get_text("copy_warning_block"))
        self.deleteBtn.setToolTip(lang.get_text("delete_warning_block"))
        self.warningGroup.setTitle(lang.get_text("warning_area"))
        self.warningGroup.setContent(lang.get_text("warning_area_desc"))
    
    def _onConfigChanged(self, key: str, value):
        """配置变化处理"""
        if key == "theme_mode":
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
            current_pos = event.globalPosition().toPoint()
            self.dragMoved.emit(self, current_pos)
    
    def _moveBtnMouseReleaseEvent(self, event):
        """移动按钮鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_dragging:
            self.is_dragging = False
            self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self.dragEnded.emit(self)
    
    def _updateMoveButtonIcon(self):
        """更新移动按钮图标"""
        theme_mode = cfg.get("theme_mode", "Dark")
        is_dark = (theme_mode == "Dark") or (theme_mode == "Auto" and isDarkTheme())
        
        from ..common.application import FMMApplication
        if is_dark:
            svg_path = FMMApplication.getResourcePath("Drag_and_drop_white.svg")
        else:
            svg_path = FMMApplication.getResourcePath("Drag_and_drop_black.svg")
        
        if svg_path.exists():
            self.moveBtn.setIcon(QIcon(str(svg_path)))
        else:
            print(f"警告：图标文件不存在 - {svg_path}")
    
    def _moveBtnMousePressEvent(self, event):
        """移动按钮鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.globalPosition().toPoint()
            self.moveBtn.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
    
    def _moveBtnMouseMoveEvent(self, event):
        """移动按钮鼠标移动事件"""
        if self.drag_start_pos and event.buttons() == Qt.MouseButton.LeftButton:
            current_pos = event.globalPosition().toPoint()

            if not self.is_dragging:
                move_distance = (current_pos - self.drag_start_pos).manhattanLength()
                if move_distance > 5:
                    self.is_dragging = True
                    self.dragStarted.emit(self)
            
            if self.is_dragging:
                self.dragMoved.emit(self, current_pos)
            
            event.accept()
    
    def _moveBtnMouseReleaseEvent(self, event):
        """移动按钮鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_dragging:
            self.is_dragging = False
            self.drag_start_pos = None
            self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self.dragEnded.emit(self)
            event.accept()
    
    def getWarningData(self):
        """获取警告数据"""
        return {
            "image_path": self.imageUpload.getImagePath(),
            "description": self.descriptionEdit.toPlainText().strip(),
            "block_tag": self.areaMarkEdit.text().strip()
        }