# coding:utf-8
"""
MOD Info Card
MOD信息卡片组件
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from qfluentwidgets import (
    GroupHeaderCardWidget, LineEdit, BodyLabel,
    FluentIcon as FIF
)
from ..common.config import cfg
from ..common.language import lang


class ModInfoCard(GroupHeaderCardWidget):
    """MOD信息卡片"""
    modInfoChanged = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(lang.get_text("mod_info"))
        
        # Create input fields
        self.modNameEdit = LineEdit()
        self.versionEdit = LineEdit()
        self.authorEdit = LineEdit()
        self.categoryEdit = LineEdit()
        self._initWidgets()
        self._connectSignals()
    
    def _initWidgets(self):
        """初始化组件"""
        self.setBorderRadius(8)
        
        # MOD name input
        self.modNameEdit.setText(cfg.get("mod_name", ""))
        self.modNameEdit.setPlaceholderText(lang.get_text("mod_name_placeholder"))
        self.modNameEdit.setClearButtonEnabled(True)
        self.modNameEdit.setFixedWidth(400)
        
        # Version number input
        self.versionEdit.setText(cfg.get("mod_version", ""))
        self.versionEdit.setPlaceholderText(lang.get_text("version_placeholder"))
        self.versionEdit.setClearButtonEnabled(True)
        self.versionEdit.setFixedWidth(400)
        
        # Author information input
        self.authorEdit.setText(cfg.get("mod_author", ""))
        self.authorEdit.setPlaceholderText(lang.get_text("author_placeholder"))
        self.authorEdit.setClearButtonEnabled(True)
        self.authorEdit.setFixedWidth(400)
        
        # MOD category input
        self.categoryEdit.setText(cfg.get("mod_category", ""))
        self.categoryEdit.setPlaceholderText(lang.get_text("mod_category_placeholder"))
        self.categoryEdit.setClearButtonEnabled(True)
        self.categoryEdit.setFixedWidth(400)
        
        # Add components to the card
        self.modNameGroup = self.addGroup(
            icon=FIF.TAG,
            title=lang.get_text("mod_name"),
            content=lang.get_text("mod_name_desc"),
            widget=self.modNameEdit
        )
        
        self.versionGroup = self.addGroup(
            icon=FIF.UPDATE,
            title=lang.get_text("version"),
            content=lang.get_text("version_desc"),
            widget=self.versionEdit
        )
        
        self.authorGroup = self.addGroup(
            icon=FIF.PEOPLE,
            title=lang.get_text("author"),
            content=lang.get_text("author_desc"),
            widget=self.authorEdit
        )
        
        self.categoryGroup = self.addGroup(
            icon=FIF.FOLDER,
            title=lang.get_text("mod_category"),
            content=lang.get_text("mod_category_desc"),
            widget=self.categoryEdit
        )

        self._customizeHeader()
    
    def _connectSignals(self):
        """连接信号"""
        self.modNameEdit.textChanged.connect(self._onModNameChanged)
        self.versionEdit.textChanged.connect(self._onVersionChanged)
        self.authorEdit.textChanged.connect(self._onAuthorChanged)
        self.categoryEdit.textChanged.connect(self._onCategoryChanged)

        lang.languageChanged.connect(self._updateTexts)
    
    def _onModNameChanged(self, text: str):
        """MOD名称变化处理"""
        cfg.set("mod_name", text.strip())
        self.modInfoChanged.emit()
    
    def _onVersionChanged(self, text: str):
        """版本号变化处理"""
        cfg.set("mod_version", text.strip())
        self.modInfoChanged.emit()
    
    def _onAuthorChanged(self, text: str):
        """作者信息变化处理"""
        cfg.set("mod_author", text.strip())
        self.modInfoChanged.emit()
    
    def _onCategoryChanged(self, text: str):
        """MOD类别变化处理"""
        cfg.set("mod_category", text.strip())
        self.modInfoChanged.emit()
    
    def _updateTexts(self):
        """更新文本"""
        self.setTitle(lang.get_text("mod_info"))
        self.modNameEdit.setPlaceholderText(lang.get_text("mod_name_placeholder"))
        self.versionEdit.setPlaceholderText(lang.get_text("version_placeholder"))
        self.authorEdit.setPlaceholderText(lang.get_text("author_placeholder"))
        self.categoryEdit.setPlaceholderText(lang.get_text("mod_category_placeholder"))
        self.modNameGroup.setTitle(lang.get_text("mod_name"))
        self.modNameGroup.setContent(lang.get_text("mod_name_desc"))
        self.versionGroup.setTitle(lang.get_text("version"))
        self.versionGroup.setContent(lang.get_text("version_desc"))
        self.authorGroup.setTitle(lang.get_text("author"))
        self.authorGroup.setContent(lang.get_text("author_desc"))
        self.categoryGroup.setTitle(lang.get_text("mod_category"))
        self.categoryGroup.setContent(lang.get_text("mod_category_desc"))
    
    def _customizeHeader(self):
        """自定义标题区域，增加标题栏高度"""
        try:
            main_layout = self.layout()
            if main_layout and main_layout.count() > 0:
                title_item = main_layout.itemAt(0)
                if title_item and title_item.widget():
                    title_widget = title_item.widget()
                    title_widget.setFixedHeight(60) # Increase the title bar height
        except Exception as e:
            print(f"自定义MOD信息卡片标题失败: {e}")
    
    def getModInfo(self) -> dict:
        """获取MOD信息"""
        return {
            "name": self.modNameEdit.text().strip(),
            "version": self.versionEdit.text().strip(),
            "author": self.authorEdit.text().strip(),
            "category": self.categoryEdit.text().strip()
        }