# coding:utf-8
"""
Cover Block
封面区块组件
"""

import os
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


class ImageUploadWidget(QWidget):
    """图像上传控件"""
    
    imageChanged = Signal(str)  # Image Path Change Signal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = ""
        self.is_hovered = False
        self.setObjectName("ImageUploadWidget")  # Set the object name for stylesheet recognition
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
        
        # widget prompt text
        self.hintLabel = QLabel(lang.get_text("click_to_upload"))
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
        
        # widget formatting prompt
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
        
        # widget clear button
        self.clearBtn = ToolButton(FIF.CLOSE, self)
        self.clearBtn.setFixedSize(24, 24)
        self.clearBtn.setToolTip(lang.get_text("clear_image"))
        self.clearBtn.hide()
        self.clearBtn.clicked.connect(self.clearImage)
    
    def _setupStyle(self):
        """设置样式"""
        from qfluentwidgets import isDarkTheme
        from ..common.config import cfg
        
        # Set the color according to the theme mode
        if isDarkTheme():
            self.normal_color = "rgba(255, 255, 255, 0.3)"
            self.hover_color = "rgba(255, 255, 255, 0.6)"
        else:
            self.normal_color = "rgba(0, 0, 0, 0.3)"
            self.hover_color = "rgba(0, 0, 0, 0.6)"
        
        self._updateStyleSheet()
        
        # Monitor theme changes
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
            ImageUploadWidget {{
                border: 2px dashed {border_color};
                border-radius: 12px;
                background-color: transparent;
            }}
            ImageUploadWidget > QLabel {{
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
            # Scale the image to fit the control
            target_size = self.size()
            target_size.setWidth(target_size.width() - 20)  # leave margins
            target_size.setHeight(target_size.height() - 20)
            
            scaled_pixmap = pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.imageLabel.setPixmap(scaled_pixmap)
            self.hintLabel.hide()
            self.formatLabel.hide()
            
            # Show the clear button and position it to the top right corner
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
    
    def setImagePath(self, image_path: str):
        """设置图像路径"""
        if image_path and os.path.exists(image_path):
            self.image_path = image_path
            self._displayImage(image_path)
            self.imageChanged.emit(image_path)
        else:
            self.clearImage()
    
    def updateTexts(self):
        """更新文本"""
        if not self.image_path:
            self.hintLabel.setText(lang.get_text("click_to_upload"))
            self.hintLabel.show()
            self.formatLabel.show()

class CoverBlock(GroupHeaderCardWidget):
    """封面区块"""
    
    deleteRequested = Signal()          # Delete request signal
    copyRequested = Signal()            # Copy request signal
    dragStarted = Signal(object)        # Drag start signal
    dragMoved = Signal(object, object)  # Drag move signal
    dragEnded = Signal(object)          # Drag end signal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(lang.get_text("cover_area"))
        self.is_collapsed = False
        self.is_dragging = False
        self.drag_start_pos = None
        self._initWidgets()
        self._connectSignals()
    
    def _initWidgets(self):
        """初始化组件"""
        self.setBorderRadius(8)
        self._setupCustomHeader()
        self._setupContent()
        
        # Add to card
        self.coverGroup = self.addGroup(
            icon=FIF.PHOTO,
            title=lang.get_text("cover_area"),
            content=lang.get_text("cover_area_desc"),
            widget=self.contentWidget
        )
        
        # In addGroup after customizing the title area
        self._customizeHeader()
    
    def _setupCustomHeader(self):
        """设置自定义标题区域"""
        self.collapseBtn = TransparentToolButton(FIF.CHEVRON_DOWN_MED, self)
        self.collapseBtn.setFixedSize(12, 12)
        self.collapseBtn.setToolTip(lang.get_text("collapse_expand"))
        
        # Create block marker text boxes - help users identify and manage multiple blocks
        self.areaMarkEdit = LineEdit(self)
        self.areaMarkEdit.setPlaceholderText(lang.get_text("area_mark"))
        self.areaMarkEdit.setFixedWidth(180)
        self.areaMarkEdit.setFixedHeight(32)
        
        # Create operation buttons
        self.moveBtn = TransparentToolButton(self)
        self._updateMoveButtonIcon()
        self.moveBtn.setFixedSize(28, 28)
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
        
        self.copyBtn = TransparentToolButton(FIF.COPY, self)
        self.copyBtn.setFixedSize(28, 28)
        self.copyBtn.setToolTip(lang.get_text("copy_cover_block"))
        
        self.deleteBtn = PrimaryToolButton(FIF.DELETE, self)
        self.deleteBtn.setFixedSize(28, 28)
        self.deleteBtn.setToolTip(lang.get_text("delete_cover_block"))
    
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

            # Increase the title bar height
            title_widget.setFixedHeight(60)

            # Subcontainer 1: Expand/Collapse button; title text; block marker text box (left-aligned)
            title_layout.insertWidget(0, self.collapseBtn)
            
            # Find the title label and insert the block mark text box after it
            title_text = lang.get_text("cover_area")
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

            # Sub-container 2: Operation button [Drag, Copy, Delete] (align to the right)
            title_layout.addStretch()
            
            # Create operation button container, uniform button layout and spacing
            title_layout.addWidget(self.moveBtn)
            title_layout.addSpacing(4)
            title_layout.addWidget(self.copyBtn)
            title_layout.addSpacing(4)
            title_layout.addWidget(self.deleteBtn)
            
            # Mark using layout manager to locate buttons
            self._using_fallback_positioning = False

        except Exception as e:
            print(f"自定义标题失败: {e}")
            self._fallback_customizeHeader()
    
    def _fallback_customizeHeader(self):
        """备用的标题自定义方法"""
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
        self.areaMarkEdit.move(50, 13)
        self.moveBtn.move(self.width() - 130, 11)
        self.copyBtn.move(self.width() - 98, 11)
        self.deleteBtn.move(self.width() - 66, 11)
        self._using_fallback_positioning = True
    
    def _setupContent(self):
        """设置内容区域"""
        # Create content container
        self.contentWidget = QWidget()
        contentLayout = QHBoxLayout(self.contentWidget)
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(15)
        
        # image upload control
        self.imageUpload = ImageUploadWidget()
        
        # Description Text Box
        self.descriptionEdit = PlainTextEdit()
        self.descriptionEdit.setPlaceholderText(lang.get_text("cover_description_placeholder"))
        self.descriptionEdit.setFixedHeight(150)
        self.descriptionEdit.setFixedWidth(400)
        
        contentLayout.addWidget(self.imageUpload)
        contentLayout.addWidget(self.descriptionEdit, 1)
    
    def _connectSignals(self):
        """连接信号"""
        self.deleteBtn.clicked.connect(self.deleteRequested.emit)
        self.copyBtn.clicked.connect(self.copyRequested.emit)
        self.collapseBtn.clicked.connect(self._toggleCollapse)
        self.moveBtn.hide()
        self.copyBtn.hide()
        self.moveBtn.mousePressEvent = self._moveBtnMousePressEvent
        self.moveBtn.mouseMoveEvent = self._moveBtnMouseMoveEvent
        self.moveBtn.mouseReleaseEvent = self._moveBtnMouseReleaseEvent
        
        # language change signal
        lang.languageChanged.connect(self._updateTexts)
        
        # configuration change signal (listen to theme change)
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
            self.animation.finished.connect(lambda: self.contentWidget.setMaximumHeight(16777215))  # 恢复默认最大高度
        
        self.animation.start()
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        if hasattr(self, '_using_fallback_positioning') and self._using_fallback_positioning:
            if hasattr(self, 'moveBtn'):
                self.moveBtn.move(self.width() - 130, 11)
            if hasattr(self, 'copyBtn'):
                self.copyBtn.move(self.width() - 98, 11)
            if hasattr(self, 'deleteBtn'):
                self.deleteBtn.move(self.width() - 66, 11)
    
    def _updateTexts(self):
        """更新文本"""
        self.setTitle(lang.get_text("cover_area"))
        self.descriptionEdit.setPlaceholderText(lang.get_text("cover_description_placeholder"))
        self.imageUpload.updateTexts()
        self.deleteBtn.setToolTip(lang.get_text("delete_cover_block"))
        self.coverGroup.setTitle(lang.get_text("cover_upload")) # Update the left group title and description
        self.coverGroup.setContent(lang.get_text("cover_upload_desc"))
    
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
            current_pos = event.globalPosition().toPoint()
            self.dragMoved.emit(self, current_pos - self.drag_start_pos)
    
    def _moveBtnMouseReleaseEvent(self, event):
        """移动按钮鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_dragging:
            self.is_dragging = False
            self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self.dragEnded.emit(self)
    
    def getCoverData(self):
        """获取封面数据"""
        return {
            "image_path": self.imageUpload.getImagePath(),
            "description": self.descriptionEdit.toPlainText().strip(),
            "cover_tag": self.areaMarkEdit.text().strip()
        }
    
    def setCoverData(self, data: dict):
        """设置封面数据"""
        image_path = data.get("image_path", "")
        if image_path:
            self.imageUpload.setImagePath(image_path)
        description = data.get("description", "")
        self.descriptionEdit.setPlainText(description)
        cover_tag = data.get("cover_tag", "")
        self.areaMarkEdit.setText(cover_tag)