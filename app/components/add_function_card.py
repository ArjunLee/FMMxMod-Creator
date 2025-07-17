# coding:utf-8
"""
Add Function Card
添加功能卡片组件
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Signal, QSize, Qt, QTimer

from qfluentwidgets import (
    GroupHeaderCardWidget, PushButton, PrimaryPushButton, BodyLabel,
    FluentIcon as FIF, TeachingTip, TeachingTipTailPosition, InfoBarIcon,
    TransparentPushButton
)

from ..common.language import lang
from ..common.application import FMMApplication


class AddFunctionCard(GroupHeaderCardWidget):
    """添加功能卡片"""
    
    addCoverRequested = Signal()  # cover signal
    addWarningRequested = Signal()  # warning signal
    addSeparatorRequested = Signal()  # separator signal
    addModFilesRequested = Signal()  # mod files signal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(lang.get_text("add_function"))
        
        # Create button
        self.addCoverBtn = PrimaryPushButton(lang.get_text("add_cover"), self, FIF.PHOTO)
        self.addWarningBtn = PushButton(lang.get_text("add_warning"), self, FIF.INFO)
        self.addSeparatorBtn = PushButton(lang.get_text("add_separator"), self, FIF.REMOVE)
        self.addModFilesBtn = PushButton(lang.get_text("add_mod_files"), self, FIF.FOLDER_ADD)
        
        # Question button
        self.questionBtn = TransparentPushButton(FIF.QUESTION, lang.get_text("sorting_tips"), self)
        self.questionBtn.setFixedSize(120, 28)  # Button fixed width and height
        
        # Create a delayed positioning timer
        self.positionTimer = QTimer()
        self.positionTimer.setSingleShot(True)
        self.positionTimer.timeout.connect(self._positionQuestionButton)
        
        self._initWidgets()
        self._connectSignals()
    
    def _initWidgets(self):
        """初始化组件"""
        self.setBorderRadius(8)
        button_style = """
            PushButton {
                min-width: 120px;
                min-height: 32px;
                margin: 2px;
            }
        """
        cover_button_style = """
            PrimaryPushButton {
                min-width: 120px;
                min-height: 32px;
                margin: 2px;
            }
        """
        
        self.addCoverBtn.setStyleSheet(cover_button_style)
        self.addWarningBtn.setStyleSheet(button_style)
        self.addSeparatorBtn.setStyleSheet(button_style)
        self.addModFilesBtn.setStyleSheet(button_style)
        
        # Create button container
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(10)
        
        buttonLayout.addWidget(self.addCoverBtn)
        buttonLayout.addWidget(self.addWarningBtn)
        buttonLayout.addWidget(self.addSeparatorBtn)
        buttonLayout.addWidget(self.addModFilesBtn)
        buttonLayout.addStretch()
        
        # Add to card
        self.functionGroup = self.addGroup(
            icon=FIF.ADD,
            title=lang.get_text("add_function"),
            content=lang.get_text("add_function_desc"),
            widget=buttonWidget
        )
        
        # Customize header after addGroup
        self._customizeHeader()
    
    def _connectSignals(self):
        """连接信号"""
        self.addCoverBtn.clicked.connect(self.addCoverRequested.emit)
        self.addWarningBtn.clicked.connect(self.addWarningRequested.emit)
        self.addSeparatorBtn.clicked.connect(self.addSeparatorRequested.emit)
        self.addModFilesBtn.clicked.connect(self.addModFilesRequested.emit)
        self.questionBtn.clicked.connect(self._showTeachingTip)
        
        # Language change signal
        lang.languageChanged.connect(self._updateTexts)
    
    def _updateTexts(self):
        """更新文本"""
        # Update card title
        self.setTitle(lang.get_text("add_function"))
        
        # Update button text
        self.addCoverBtn.setText(lang.get_text("add_cover"))
        self.addWarningBtn.setText(lang.get_text("add_warning"))
        self.addSeparatorBtn.setText(lang.get_text("add_separator"))
        self.addModFilesBtn.setText(lang.get_text("add_mod_files"))
        self.questionBtn.setText(lang.get_text("sorting_tips"))
        
        # Update group title and description
        self.functionGroup.setTitle(lang.get_text("add_function"))
        self.functionGroup.setContent(lang.get_text("add_function_desc"))
        
        # Ensure Question button is visible and correctly positioned after language change
        self.questionBtn.show()
        self.questionBtn.raise_()
        self._positionQuestionButton()
    
    def _customizeHeader(self):
        """自定义标题区域，统一使用布局管理"""
        try:
            main_layout = self.layout()
            if main_layout and main_layout.count() > 0:
                title_item = main_layout.itemAt(0)
                if title_item and title_item.widget():
                    title_widget = title_item.widget()
                    title_layout = title_widget.layout()
                    if title_layout:
                        title_widget.setFixedHeight(60)
                        title_layout.addStretch()
                        title_layout.addWidget(self.questionBtn)
                        title_layout.setAlignment(self.questionBtn, Qt.AlignmentFlag.AlignVCenter)
                        self._using_layout_positioning = True
                        return
            
            # If the layout method fails, the markup uses manual positioning
            self._using_layout_positioning = False
            self._fallbackCustomizeHeader()
            
        except Exception as e:
            print(f"自定义添设功能标题失败: {e}")
            self._using_layout_positioning = False
            self._fallbackCustomizeHeader()
    
    def _fallbackCustomizeHeader(self):
        """备用的标题自定义方法"""
        self.questionBtn.setParent(self)
        self.questionBtn.show()
        self.questionBtn.raise_()
        self._positionQuestionButton()
    
    def _positionQuestionButton(self):
        """定位Question按钮（仅在手动定位模式下执行）"""
        if hasattr(self, 'questionBtn') and self.questionBtn:
            # Coordinate calculation is only performed in manual positioning mode.
            if hasattr(self, '_using_layout_positioning') and not self._using_layout_positioning:
                x = self.width() - self.questionBtn.width() - 10
                y = 16
                self.questionBtn.move(x, y)
                
                # Ensure the button is always in the top layer
                self.questionBtn.raise_()
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        if hasattr(self, '_using_layout_positioning') and not self._using_layout_positioning:
            self.positionTimer.start(50)  # 50ms延迟
    
    def showEvent(self, event):
        """显示事件"""
        super().showEvent(event)
        if hasattr(self, 'questionBtn'):
            self.questionBtn.show()
            if hasattr(self, '_using_layout_positioning') and not self._using_layout_positioning:
                self.questionBtn.raise_()
                self.positionTimer.start(100)  # Add display delay
    
    def _showTeachingTip(self):
        """显示拖拽排序技巧教学提示"""
        TeachingTip.create(
            target=self.questionBtn,
            image=str(FMMApplication.getResourcePath("Drag_and_Drop_Example_Video.gif")),
            title=lang.get_text("drag_and_drop_sorting_tips_title"),
            content=lang.get_text("drag_and_drop_sorting_tips_content"),
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=-1,  # Disable auto-close
            parent=self
        )