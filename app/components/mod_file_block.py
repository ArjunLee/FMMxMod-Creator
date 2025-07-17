# coding:utf-8
"""
MOD File Block
MOD文件区块组件
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QFileDialog, QPushButton, QFrame
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtSvgWidgets import QSvgWidget
from pathlib import Path
from qfluentwidgets import (
    CardWidget, BodyLabel, CaptionLabel, PrimaryToolButton, ToolButton, PlainTextEdit,
    FluentIcon as FIF, isDarkTheme, TransparentToolButton, LineEdit, PushButton,
    RoundMenu, Action, DropDownPushButton
)
from ..common.language import lang
from ..common.config import cfg
from .file_display_widget import FileDisplayWidget

class ModFileImageUploadWidget(QWidget):
    """MOD文件图像上传控件"""
    imageChanged = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_path = ""
        self.is_hovered = False
        self.setObjectName("ModFileImageUploadWidget")
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
        
        self.hintLabel = QLabel(lang.get_text("mod_file_upload_hint"))
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

        # Create a floating clear button
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

        # Create border color animations (simulated by transparency changes)
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
            ModFileImageUploadWidget {{
                border: 2px dashed {border_color};
                border-radius: 12px;
                background-color: transparent;
            }}
            ModFileImageUploadWidget > QLabel {{
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
            self.hintLabel.setText(lang.get_text("mod_file_upload_hint"))
            self.hintLabel.show()
            self.formatLabel.show()
        self.clearBtn.setToolTip(lang.get_text("clear_image"))

class ModFileBlock(CardWidget):
    """MOD文件区块"""
    deleteRequested = Signal()          # Signal emitted when a delete request is made
    copyRequested = Signal()            # Signal emitted when a copy request is made
    moveRequested = Signal()            # Signal emitted when a move request is made
    dragStarted = Signal(object)        # Signal emitted when dragging starts, passing the dragged object
    dragMoved = Signal(object, object)  # Signal emitted during dragging, passing the dragged object and current position
    dragEnded = Signal(object)          # Signal emitted when dragging ends, passing the dragged object
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dragging = False
        self.drag_start_pos = None
        self.is_collapsed = False
        self._initWidgets()
        self._connectSignals()
        self._updateMoveButtonIcon()
    
    def _initWidgets(self):
        """初始化组件"""
        self.setBorderRadius(8)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self._setupHeader()
        self._setupContent()
        self.mainLayout.addWidget(self.headerWidget)
        self._setupHeaderSeparator()
        self.mainLayout.addWidget(self.headerSeparatorWidget)
        self.mainLayout.addWidget(self.contentWidget)
    
    def _setupHeader(self):
        """设置标题区域"""
        self.headerWidget = QWidget()
        self.headerWidget.setFixedHeight(60)
        headerLayout = QHBoxLayout(self.headerWidget)
        headerLayout.setContentsMargins(24, 10, 15, 10)
        headerLayout.setSpacing(5)
        self.collapseBtn = TransparentToolButton(FIF.CHEVRON_DOWN_MED, self)
        self.collapseBtn.setFixedSize(12, 12)
        self.collapseBtn.setToolTip(lang.get_text("collapse_expand"))
        self.titleLabel = BodyLabel(lang.get_text("mod_file_area"))
        self.titleLabel.setStyleSheet("font-size: 15px;font-weight: 600;")
        self.areaMarkEdit = LineEdit()
        self.areaMarkEdit.setPlaceholderText(lang.get_text("area_mark"))
        self.areaMarkEdit.setFixedWidth(180)
        self.areaMarkEdit.setFixedHeight(32)
        self.moveBtn = TransparentToolButton()
        self._updateMoveButtonIcon()
        self.moveBtn.setFixedSize(28, 28)
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
        self.copyBtn = TransparentToolButton(FIF.COPY)
        self.copyBtn.setFixedSize(28, 28)
        self.copyBtn.setToolTip(lang.get_text("copy_mod_file_block"))
        self.deleteBtn = PrimaryToolButton(FIF.DELETE)
        self.deleteBtn.setFixedSize(28, 28)
        self.deleteBtn.setToolTip(lang.get_text("delete_mod_file_block"))

        headerLayout.addWidget(self.collapseBtn)
        headerLayout.addWidget(self.titleLabel)
        headerLayout.addWidget(self.areaMarkEdit)
        headerLayout.addStretch()
        headerLayout.addWidget(self.moveBtn)
        headerLayout.addSpacing(4)
        headerLayout.addWidget(self.copyBtn)
        headerLayout.addSpacing(4)
        headerLayout.addWidget(self.deleteBtn)
    
    def _setupHeaderSeparator(self):
        """设置标题下方的分割线"""
        self.headerSeparatorWidget = QWidget()
        self.headerSeparatorWidget.setFixedHeight(21)
        
        separatorLayout = QHBoxLayout(self.headerSeparatorWidget)
        separatorLayout.setContentsMargins(0, 10, 0, 10)
        separatorLayout.setSpacing(0)
        
        self.headerSeparatorLabel = QLabel()
        self.headerSeparatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.headerSeparatorLabel.setFixedHeight(1)
        self._updateHeaderSeparatorStyle()
        
        separatorLayout.addWidget(self.headerSeparatorLabel)
    
    def _setupContent(self):
        """设置内容区域"""
        self.contentWidget = QWidget()
        contentLayout = QVBoxLayout(self.contentWidget)
        contentLayout.setContentsMargins(20, 15, 20, 15)
        contentLayout.setSpacing(20)
        
        # Container 3: Main content area (divided into three columns: 46% + 8% + 46%)
        mainContainer = QWidget()
        mainLayout = QHBoxLayout(mainContainer)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(10)
        
        # Column 1: Sub-container 1 (46% width)
        leftColumn = QWidget()
        leftColumnLayout = QVBoxLayout(leftColumn)
        leftColumnLayout.setContentsMargins(0, 0, 0, 0)
        leftColumnLayout.setSpacing(15)
        
        # Module name text box (width is adaptive according to the interface)
        self.moduleNameEdit = LineEdit()
        self.moduleNameEdit.setFixedHeight(33)
        self.moduleNameEdit.setPlaceholderText(lang.get_text("module_name_placeholder"))
        clearAction = QAction(FIF.CLOSE.qicon(), "", triggered=lambda: self.moduleNameEdit.clear())
        self.moduleNameEdit.addAction(clearAction, LineEdit.ActionPosition.TrailingPosition)
        leftColumnLayout.addWidget(self.moduleNameEdit)
        imageContainer = QWidget()
        imageLayout = QHBoxLayout(imageContainer)
        imageLayout.setContentsMargins(0, 0, 0, 0)
        self.imageUpload = ModFileImageUploadWidget()
        imageLayout.addStretch()
        imageLayout.addWidget(self.imageUpload)
        imageLayout.addStretch()
        leftColumnLayout.addWidget(imageContainer)
        self.descriptionEdit = PlainTextEdit()
        self.descriptionEdit.setPlaceholderText(lang.get_text("mod_file_description_placeholder"))
        self.descriptionEdit.setFixedHeight(150)
        leftColumnLayout.addWidget(self.descriptionEdit)
        
        # Column 2: Sub-container 2 (5% width)
        separatorColumn = QWidget()
        separatorColumnLayout = QVBoxLayout(separatorColumn)
        separatorColumnLayout.setContentsMargins(0, 0, 0, 0)
        separatorColumnLayout.setSpacing(0)
        self.verticalSeparatorLabel = QLabel()
        self.verticalSeparatorLabel.setFixedWidth(1)
        self.verticalSeparatorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._updateVerticalSeparatorStyle()
        separatorContainer = QWidget()
        separatorContainerLayout = QHBoxLayout(separatorContainer)
        separatorContainerLayout.setContentsMargins(0, 0, 0, 0)
        separatorContainerLayout.addStretch()
        separatorContainerLayout.addWidget(self.verticalSeparatorLabel)
        separatorContainerLayout.addStretch()
        separatorColumnLayout.addWidget(separatorContainer)
        
        # Column 3: Sub-container 3 (47.5% width)
        rightColumn = QWidget()
        rightColumnLayout = QVBoxLayout(rightColumn)
        rightColumnLayout.setContentsMargins(0, 0, 0, 0)
        rightColumnLayout.setSpacing(15)
        self.addFilesBtn = DropDownPushButton(lang.get_text("add_files"))   # Add files button
        self.addFilesBtn.setIcon(FIF.FOLDER_ADD)
        self.addFilesBtn.setFixedWidth(135)
        self.filesMenu = RoundMenu(parent=self)  # Create menu
        self.filesMenu.addAction(Action(FIF.DOCUMENT, lang.get_text("add_files")))
        self.filesMenu.addAction(Action(FIF.FOLDER, lang.get_text("add_folders")))
        self.addFilesBtn.setMenu(self.filesMenu)    # Set menu
        rightColumnLayout.addWidget(self.addFilesBtn, 0, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.filesDisplayWidget = FileDisplayWidget()   # Files display area (left-aligned)
        self.filesDisplayWidget.setMinimumHeight(200)
        rightColumnLayout.addWidget(self.filesDisplayWidget)
        mainLayout.addWidget(leftColumn, 490)
        mainLayout.addWidget(separatorColumn, 20)
        mainLayout.addWidget(rightColumn, 490)
        
        contentLayout.addWidget(mainContainer)  # Add the main container to the content layout
        
        # Debug mode: For fine-tuning element positions
        
        # def print_debug_info():
        #     print(f"[DEBUG] === 重构后布局调试信息 ===")
        #     print(f"[DEBUG] contentLayout 边距: {contentLayout.contentsMargins()}")
        #     print(f"[DEBUG] contentLayout 子项数量: {contentLayout.count()}")
        #     print(f"[DEBUG] 模块名称输入框几何: {self.moduleNameEdit.geometry()}")
        #     print(f"[DEBUG] 图像上传控件几何: {self.imageUpload.geometry()}")
        #     print(f"[DEBUG] 描述文本框几何: {self.descriptionEdit.geometry()}")
        #     print(f"[DEBUG] 按钮几何: {self.addFilesBtn.geometry()}")
        #     print(f"[DEBUG] === 调试信息结束 ===")
        
        # # 使用定时器延迟执行调试信息打印
        # QTimer.singleShot(100, print_debug_info)
        
        # 设置调试样式 - 为不同区域添加不同颜色边框
        # 主卡片区域 - 蓝色边框
        # self.setStyleSheet("QWidget { background-color: rgba(0, 0, 255, 0.05); border: 2px solid blue; }")
        
        # 各个子容器的边框已在创建时设置
        # subContainer1: 黄色边框（模块名称输入框）
        # subContainer2: 青色边框（图像上传+文本输入）
        # subContainer3: 紫色边框（分割线）
        # subContainer4: 红色边框（按钮）
        # subContainer5: 灰色虚线边框（文件展示区域）
    
    def _connectSignals(self):
        """连接信号"""
        self.moveBtn.clicked.connect(self.moveRequested.emit)
        self.copyBtn.clicked.connect(self.copyRequested.emit)
        self.deleteBtn.clicked.connect(self.deleteRequested.emit)
        self.collapseBtn.clicked.connect(self._toggleCollapse)
        for action in self.filesMenu.actions():
            action.triggered.connect(lambda checked, a=action: self._onMenuActionTriggered(a))
        lang.languageChanged.connect(self._updateTexts)
        
        # Monitor theme changes to update divider styles
        from qfluentwidgets import qconfig
        qconfig.themeChanged.connect(self._updateHeaderSeparatorStyle)
        qconfig.themeChanged.connect(self._updateVerticalSeparatorStyle)
        
        # Drag button mouse event
        self.moveBtn.mousePressEvent = self._moveBtnMousePressEvent
        self.moveBtn.mouseMoveEvent = self._moveBtnMouseMoveEvent
        self.moveBtn.mouseReleaseEvent = self._moveBtnMouseReleaseEvent
    
    def _onMenuActionTriggered(self, action):
        """菜单项被触发"""
        if action.text() == lang.get_text("add_files"):
            self._selectFiles()
        elif action.text() == lang.get_text("add_folders"):
            self._selectFolders()
    
    def _selectFiles(self):
        """选择文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            lang.get_text("select_files"),
            "",
            "All Files (*.*)"
        )
        
        if files:
            self.filesDisplayWidget.addFiles(files)
    
    def _selectFolders(self):
        """选择文件夹"""
        folder = QFileDialog.getExistingDirectory(
            self,
            lang.get_text("select_folders")
        )
        
        if folder:
            self.filesDisplayWidget.addFolders([folder])
    
    def _toggleCollapse(self):
        """切换折叠状态"""
        self.is_collapsed = not self.is_collapsed

        if self.is_collapsed:
            self.collapseBtn.setIcon(FIF.CHEVRON_RIGHT_MED)
        else:
            self.collapseBtn.setIcon(FIF.CHEVRON_DOWN_MED)

        if self.is_collapsed:
            self.headerSeparatorWidget.hide()
        else:
            self.headerSeparatorWidget.show()
        
        # Create animation effects
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
    
    def _updateMoveButtonIcon(self):
        """更新移动按钮图标"""
        if isDarkTheme():
            self.moveBtn.setIcon(FIF.MOVE)
        else:
            self.moveBtn.setIcon(FIF.MOVE)
    
    def _updateTexts(self):
        """更新文本"""
        self.titleLabel.setText(lang.get_text("mod_file_area"))
        self.titleLabel.setStyleSheet("font-size: 15px;font-weight: 600;")
        self.addFilesBtn.setText(lang.get_text("add_files"))

        actions = self.filesMenu.actions()
        if len(actions) >= 2:
            actions[0].setText(lang.get_text("add_files"))
            actions[1].setText(lang.get_text("add_folders"))

        self.descriptionEdit.setPlaceholderText(lang.get_text("mod_file_description_placeholder"))  # Update description text box placeholder
        self.moduleNameEdit.setPlaceholderText(lang.get_text("module_name_placeholder"))            # Update module name text box placeholder
        self.imageUpload.updateTexts()                                                              # Update image upload control text
        self.collapseBtn.setToolTip(lang.get_text("collapse_expand"))                               # Update Tooltips
        self.areaMarkEdit.setPlaceholderText(lang.get_text("area_mark"))
        self.moveBtn.setToolTip(lang.get_text("drag_to_move_block"))
        self.copyBtn.setToolTip(lang.get_text("copy_mod_file_block"))
        self.deleteBtn.setToolTip(lang.get_text("delete_mod_file_block"))
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)

        if hasattr(self, '_using_fallback_positioning') and self._using_fallback_positioning:
            self.moveBtn.move(self.width() - 108, 10)
            self.copyBtn.move(self.width() - 72, 10)
            self.deleteBtn.move(self.width() - 36, 10)
        self._updateHeaderSeparatorStyle()
        self._updateVerticalSeparatorStyle()
    
    def getModuleData(self):
        """获取模块数据"""
        return {
            'module_name': self.moduleNameEdit.text(),
            'area_mark': self.areaMarkEdit.text(),
            'image_path': self.imageUpload.getImagePath(),
            'description': self.descriptionEdit.toPlainText(),
            'files': self.filesDisplayWidget.getFileList()
        }
    
    def setModuleData(self, data):
        """设置模块数据"""
        if 'module_name' in data:
            self.moduleNameEdit.setText(data['module_name'])
        if 'area_mark' in data:
            self.areaMarkEdit.setText(data['area_mark'])
        if 'description' in data:
            self.descriptionEdit.setPlainText(data['description'])
        # TODO: 设置图像和文件列表
    
    def getModFileData(self):
        """获取MOD文件数据（兼容home_interface调用）"""
        return self.getModuleData()
    
    def setModFileData(self, data):
        """设置MOD文件数据（兼容home_interface调用）"""
        return self.setModuleData(data)
    
    def _updateHeaderSeparatorStyle(self):
        """更新标题下方分割线样式"""
        if not hasattr(self, 'headerSeparatorLabel'):
            return
            
        container_width = self.width() if self.width() > 0 else 800
        separator_width = int(container_width * 0.95)

        if isDarkTheme():
            color = "rgba(255, 255, 255, 25)"
        else:
            color = "rgba(0, 0, 0, 25)"

        self.headerSeparatorLabel.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border: none;
            }}
        """)

        self.headerSeparatorLabel.setFixedWidth(separator_width)
    
    def _updateVerticalSeparatorStyle(self):
        """更新竖线分割线样式"""
        if not hasattr(self, 'verticalSeparatorLabel'):
            return

        if isDarkTheme():
            color = "rgba(255, 255, 255, 25)"
        else:
            color = "rgba(0, 0, 0, 25)"

        self.verticalSeparatorLabel.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                border: none;
            }}
        """)

        self.verticalSeparatorLabel.setFixedHeight(360)
    
    def _moveBtnMousePressEvent(self, event):
        """拖拽按钮鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = event.globalPosition().toPoint()
            self.moveBtn.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.dragStarted.emit(self)
    
    def _moveBtnMouseMoveEvent(self, event):
        """拖拽按钮鼠标移动事件"""
        if self.is_dragging and (event.buttons() & Qt.MouseButton.LeftButton):
            current_pos = event.globalPosition().toPoint()
            self.dragMoved.emit(self, current_pos)
    
    def _moveBtnMouseReleaseEvent(self, event):
        """拖拽按钮鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_dragging:
            self.is_dragging = False
            self.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self.dragEnded.emit(self)