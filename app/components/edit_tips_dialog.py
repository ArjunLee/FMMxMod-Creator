# coding:utf-8
"""
Edit Tips Dialog
编辑提示对话框组件
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from qfluentwidgets import (
    Flyout, FlyoutView, FlyoutAnimationType, PushButton, PrimaryPushButton, 
    InfoBarIcon, FluentIcon as FIF
)
from PySide6.QtWidgets import QHBoxLayout
from ..common.language import lang
from ..common.config import cfg
from ..common.application import FMMApplication


class EditTipsDialog:
    """编辑提示对话框"""
    
    @staticmethod
    def show(target, parent):
        """显示编辑提示对话框
        
        Args:
            target: 目标控件（弹出位置参考）
            parent: 父控件
        """
        # Use FlyoutView component
        view = FlyoutView(
            title=lang.get_text("edit_tips_title"),
            content=lang.get_text("edit_tips_content"),
            image=str(FMMApplication.getResourcePath("modlist_editing_tips.gif")),
        )
        title_font = QFont()
        title_font.setPointSize(16)
        view.titleLabel.setFont(title_font)
        
        # Set content font
        content_font = QFont()
        content_font.setPointSize(14)  # 正文字号
        view.contentLabel.setFont(content_font)
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 15, 0, 0)
        button_layout.addStretch()
        
        # OK button
        got_it_button = PushButton(lang.get_text("edit_tips_got_it"))
        button_layout.addWidget(got_it_button)
        button_layout.addSpacing(10)
        
        # Do not show again button, supports theme color
        no_more_tips_button = PrimaryPushButton(lang.get_text("edit_tips_dont_show"))
        button_layout.addWidget(no_more_tips_button)
        
        # Add button layout to view
        view.widgetLayout.addLayout(button_layout)
        
        # Adjust layout spacing
        view.widgetLayout.insertSpacing(0, 5)
        view.widgetLayout.addSpacing(5)
        
        # Show Flyout
        flyout = Flyout.make(
            view, 
            target, 
            parent, 
            FlyoutAnimationType.SLIDE_RIGHT
        )
        
        # Connect button signals
        def on_got_it_clicked():
            """知道了按钮点击处理"""
            flyout.close()
        
        def on_no_more_tips_clicked():
            """不再提示按钮点击处理"""
            cfg.editTipsShown = True
            flyout.close()
        
        got_it_button.clicked.connect(on_got_it_clicked)
        no_more_tips_button.clicked.connect(on_no_more_tips_clicked)
        
        # Connect view close signal
        view.closed.connect(flyout.close)
        
        return flyout