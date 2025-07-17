# coding:utf-8
"""
File Display Widget
文件展示组件
"""

import os
import subprocess
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QFileDialog, QApplication, QSizePolicy
)
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve, QRect, QSize
from PySide6.QtGui import QAction, QIcon

from qfluentwidgets import (
    PushButton, FluentIcon as FIF, RoundMenu, Action, TransparentToolButton,
    MessageBoxBase, SubtitleLabel, LineEdit, CaptionLabel, SplitPushButton
)

class RenameDialog(MessageBoxBase):
    """重命名对话框"""
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.current_name = current_name

        from ..common.language import lang
        self.lang_manager = lang
        self.titleLabel = SubtitleLabel(self.lang_manager.get_text("rename_dialog_title"), self)
        self.nameLineEdit = LineEdit(self)
        self.nameLineEdit.setPlaceholderText(self.lang_manager.get_text("rename_placeholder"))
        self.nameLineEdit.setText(current_name)
        self.nameLineEdit.setClearButtonEnabled(True)
        self.warningLabel = CaptionLabel(self.lang_manager.get_text("name_cannot_be_empty"))
        self.warningLabel.setTextColor("#cf1010", "#ff1c20")
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.warningLabel)
        self.warningLabel.hide()
        self.yesButton.setText(self.lang_manager.get_text("confirm"))
        self.cancelButton.setText(self.lang_manager.get_text("cancel"))
        self.widget.setMinimumWidth(350)
        self.setWindowTitle(self.lang_manager.get_text("rename_dialog_title"))
        self.yesButton.clicked.connect(self.validate)
        self.lang_manager.languageChanged.connect(self._updateTexts)
        self.nameLineEdit.selectAll()
    
    def _updateTexts(self):
        """更新文本"""
        self.titleLabel.setText(self.lang_manager.get_text("rename_dialog_title"))
        self.nameLineEdit.setPlaceholderText(self.lang_manager.get_text("rename_placeholder"))
        self.warningLabel.setText(self.lang_manager.get_text("name_cannot_be_empty"))
        self.yesButton.setText(self.lang_manager.get_text("confirm"))
        self.cancelButton.setText(self.lang_manager.get_text("cancel"))
        self.setWindowTitle(self.lang_manager.get_text("rename_dialog_title"))
    
    def validate(self):
        """验证输入"""
        name = self.nameLineEdit.text().strip()
        if not name:
            self.warningLabel.show()
            return False
        else:
            self.warningLabel.hide()
            return True
    
    def getNewName(self):
        """获取新名称"""
        return self.nameLineEdit.text().strip()


class FileItemWidget(QWidget):
    """文件项组件"""
    deleteRequested = Signal(object)
    renameRequested = Signal(object, str)
    
    def __init__(self, file_path, display_name=None, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.display_name = display_name or Path(file_path).name
        self.is_directory = os.path.isdir(file_path)
        self._initUI()
    
    def _initUI(self):
        """初始化界面"""
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 5, 5)
        layout.setSpacing(5)
        icon = FIF.FOLDER if self.is_directory else FIF.DOCUMENT
        
        # Create SplitPushButton
        self.splitButton = SplitPushButton(icon, self._truncateName(self.display_name))
        self.splitButton.setToolTip(self.display_name)
        self.splitButton.setFixedHeight(32)
        self.splitButton.setMinimumWidth(50)
        self.splitButton.setMaximumWidth(300)
        self.splitButton.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.splitButton.clicked.connect(self._openFile)
        self._setupSplitButtonMenu()
        
        layout.addWidget(self.splitButton, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(0)
    
    def _truncateName(self, name, max_length=30):
        """截断文件名"""
        if len(name) <= max_length:
            return name
        return name[:max_length-3] + "..."
    
    def _setupSplitButtonMenu(self):
        """设置SplitButton的下拉菜单"""
        from ..common.language import lang
        self.lang_manager = lang
        self.menu = RoundMenu(parent=self)
        self.renameAction = Action(FIF.EDIT, self.lang_manager.get_text("rename"))
        self.renameAction.triggered.connect(self._showRenameDialog)
        self.menu.addAction(self.renameAction)
        self.deleteAction = Action(FIF.DELETE, self.lang_manager.get_text("delete"))
        self.deleteAction.triggered.connect(lambda: self.deleteRequested.emit(self))
        self.menu.addAction(self.deleteAction)
        self.openLocationAction = Action(FIF.FOLDER, self.lang_manager.get_text("open_file_location"))
        self.openLocationAction.triggered.connect(self._openFileLocation)
        self.menu.addAction(self.openLocationAction)
        self.splitButton.setFlyout(self.menu)
        self.lang_manager.languageChanged.connect(self._updateMenuTexts)
    
    def _updateMenuTexts(self):
        """更新菜单文本"""
        if hasattr(self, 'renameAction'):
            self.renameAction.setText(self.lang_manager.get_text("rename"))
        if hasattr(self, 'deleteAction'):
            self.deleteAction.setText(self.lang_manager.get_text("delete"))
        if hasattr(self, 'openLocationAction'):
            self.openLocationAction.setText(self.lang_manager.get_text("open_file_location"))

    def _showRenameDialog(self):
        """显示重命名对话框"""
        try:
            dialog = RenameDialog(self.display_name, self.window())
            dialog.show()
            if dialog.exec():
                new_name = dialog.getNewName()
                if new_name and new_name != self.display_name:
                    self.renameRequested.emit(self, new_name)
        except Exception as e:
            print(f"重命名对话框错误: {e}")
    
    def _openFileLocation(self):
        """打开文件位置"""
        try:
            if os.path.exists(self.file_path):
                subprocess.run(['explorer', '/select,', os.path.normpath(self.file_path)])
            else:
                parent_dir = os.path.dirname(self.file_path)
                if os.path.exists(parent_dir):
                    subprocess.run(['explorer', os.path.normpath(parent_dir)])
        except Exception as e:
            print(f"打开文件位置失败: {e}")
    
    def _openFile(self):
        """打开文件"""
        try:
            if os.path.exists(self.file_path):
                if self.is_directory:
                    subprocess.run(['explorer', os.path.normpath(self.file_path)])
                else:
                    os.startfile(self.file_path)
        except Exception as e:
            print(f"打开文件失败: {e}")
    
    def updateDisplayName(self, new_name):
        """更新显示名称"""
        self.display_name = new_name
        self.splitButton.setText(self._truncateName(new_name))
        self.splitButton.setToolTip(new_name)
    
    def getFilePath(self):
        """获取文件路径"""
        return self.file_path
    
    def getDisplayName(self):
        """获取显示名称"""
        return self.display_name

class FileDisplayWidget(QWidget):
    """文件展示组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_items = []
        self._initUI()
    
    def _initUI(self):
        """初始化界面"""
        from ..common.language import lang
        self.lang_manager = lang
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(8, 8, 8, 8)
        self.mainLayout.setSpacing(3)
        self.placeholderLabel = QLabel(self.lang_manager.get_text("no_files_selected"))
        self.placeholderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.placeholderLabel.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 14px;
                padding: 20px;
            }
        """)
        self.mainLayout.addWidget(self.placeholderLabel)
        self.mainLayout.addStretch()
        self.lang_manager.languageChanged.connect(self._updateTexts)
    
    def _updateTexts(self):
        """更新文本"""
        self.placeholderLabel.setText(self.lang_manager.get_text("no_files_selected"))
    
    def addFiles(self, file_paths):
        """添加文件"""
        for file_path in file_paths:
            if file_path not in [item.getFilePath() for item in self.file_items]:
                self._addFileItem(file_path)
        self._updatePlaceholderVisibility()
    
    def addFolders(self, folder_paths):
        """添加文件夹"""
        for folder_path in folder_paths:
            if folder_path not in [item.getFilePath() for item in self.file_items]:
                self._addFileItem(folder_path)
        self._updatePlaceholderVisibility()
    
    def _addFileItem(self, file_path):
        """添加文件项"""
        file_item = FileItemWidget(file_path, parent=self)
        file_item.deleteRequested.connect(self._removeFileItem)
        file_item.renameRequested.connect(self._renameFileItem)

        self.mainLayout.insertWidget(len(self.file_items), file_item)
        self.file_items.append(file_item)
    
    def _removeFileItem(self, file_item):
        """移除文件项（带动画效果）"""
        if file_item in self.file_items:
            # Create vanishing animation
            self.animation = QPropertyAnimation(file_item, b"geometry")
            self.animation.setDuration(200)
            self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            
            # Get current geometry information
            current_rect = file_item.geometry()
            target_rect = QRect(current_rect.x(), current_rect.y(), current_rect.width(), 0)
            
            self.animation.setStartValue(current_rect)
            self.animation.setEndValue(target_rect)
            
            # Delete component after animation is complete
            self.animation.finished.connect(lambda: self._finishRemoveFileItem(file_item))
            self.animation.start()
    
    def _finishRemoveFileItem(self, file_item):
        """完成文件项移除"""
        if file_item in self.file_items:
            self.file_items.remove(file_item)
            self.mainLayout.removeWidget(file_item)
            file_item.deleteLater()
            self._updatePlaceholderVisibility()
    
    def _renameFileItem(self, file_item, new_name):
        """重命名文件项"""
        file_item.updateDisplayName(new_name)
    
    def _updatePlaceholderVisibility(self):
        """更新占位符可见性"""
        has_files = len(self.file_items) > 0
        self.placeholderLabel.setVisible(not has_files)
    
    def getFileList(self):
        """获取文件列表"""
        return [(item.getFilePath(), item.getDisplayName()) for item in self.file_items]
    
    def clearFiles(self):
        """清空文件列表"""
        for item in self.file_items[:]:
            self._finishRemoveFileItem(item)