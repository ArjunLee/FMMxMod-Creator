# coding:utf-8
"""
Home Interface
主界面模块
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QPixmap, QPainter, QColor, QPalette
from qfluentwidgets import ScrollArea, Flyout, InfoBarIcon, InfoBar, InfoBarPosition, isDarkTheme
from ..components.mod_info_card import ModInfoCard
from ..components.add_function_card import AddFunctionCard
from ..components.cover_block import CoverBlock
from ..components.warning_block import WarningBlock
from ..components.separator_block import SeparatorBlock
from ..components.mod_file_block import ModFileBlock
from ..components.floating_menu_button import FloatingMenuButton
from ..service.build_service import BuildService
from ..common.language import lang

class HomeInterface(ScrollArea):
    """主界面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        
        # dynamic block list
        self.dynamic_blocks = []
        self.cover_block = None             # Cover block (fixed at the top)
        self.warning_blocks = []            # Warning block list (for data retrieval)
        self.separator_blocks = []          # Separator block list (for data retrieval)
        self.mod_file_blocks = []           # MOD file block list (for data retrieval)
        self.sortable_blocks = []           # Sortable block list (warning, separator, mod file blocks)
        
        # Drag related properties
        self.drag_proxy = None              # Drag proxy control
        self.dragging_block = None          # Dragging block
        self.drag_start_index = -1          # Drag start position
        self.drag_insert_indicator = None   # Drag insert indicator
        
        # Sticky add function card related properties
        self.sticky_add_function_card = None          # Sticky AddFunctionCard copy
        self.is_add_function_sticky = False           # AddFunctionCard是否已固定
        
        self._initUI()
        self._initFloatingMenuButton()
        self._initBuildService()
        self._connectSignals()
    
    def focusOutEvent(self, event):
        """窗口失去焦点事件"""
        if self.dragging_block:
            self.dragging_block.setStyleSheet("")
            self.dragging_block.is_dragging = False
            self.dragging_block.drag_start_pos = None
            self.dragging_block.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
            self._cleanupDrag()
        super().focusOutEvent(event)
    
    def _initUI(self):
        """初始化界面"""
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        
        # Create a card component
        self.modInfoCard = ModInfoCard(self.scrollWidget)
        self.addFunctionCard = AddFunctionCard(self.scrollWidget)
        
        # Add to Layout
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addWidget(self.modInfoCard)
        self.vBoxLayout.addWidget(self.addFunctionCard)
        
        # Add Separator
        self.vBoxLayout.addStretch(1)
        
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("homeInterface")
        
        # Connect scrolling events
        self.verticalScrollBar().valueChanged.connect(self._onScrollValueChanged)
        
        # Create a fixed AddFunctionCard copy
        self._createStickyAddFunctionCard()
        
        self.setStyleSheet("""
            HomeInterface {
                background-color: transparent;
                border: none;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QWidget {
                background-color: transparent;
                border: none;
            }
            /* 排除固定卡片，保持其不透明 */
            QWidget#sticky_add_function_card {
                background-color: none;
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
        """)
    
    def _initFloatingMenuButton(self):
        """初始化浮层菜单按钮"""
        self.floatingMenuButton = FloatingMenuButton(self)
        self.floatingMenuButton.startBuildRequested.connect(self._onStartBuild)
        self.floatingMenuButton.clearAllAreaRequested.connect(self._onClearAllArea)
        self.floatingMenuButton.raise_()
    
    def _initBuildService(self):
        """初始化构建服务"""
        self.buildService = BuildService(self)
        self.buildService.buildStarted.connect(self._onBuildStarted)
        self.buildService.progressChanged.connect(self._onBuildProgressChanged)
        self.buildService.statusChanged.connect(self._onBuildStatusChanged)
        self.buildService.buildCompleted.connect(self._onBuildCompleted)
        self.buildService.buildFailed.connect(self._onBuildFailed)
        self.floatingMenuButton.connectBuildService(self.buildService)
    
    def _connectSignals(self):
        """连接信号"""
        lang.languageChanged.connect(self._updateTexts)
        self.addFunctionCard.addCoverRequested.connect(self._addCoverBlock)
        self.addFunctionCard.addWarningRequested.connect(self._addWarningBlock)
        self.addFunctionCard.addSeparatorRequested.connect(self._addSeparatorBlock)
        self.addFunctionCard.addModFilesRequested.connect(self._addModFilesBlock)
    
    def _updateTexts(self):
        """更新文本"""
        pass    # The child component automatically updates the text
    
    def _onStartBuild(self):
        """开始构筑处理"""
        mod_info = self.modInfoCard.getModInfo()
        cover_data = self.getCoverData()
        sorted_blocks = self._getSortedBlocksData()
        
        # Start the build service
        self.buildService.start_build(mod_info, cover_data, sorted_blocks)
    
    def _onClearAllArea(self):
        """清除所有区块处理"""
        if self.cover_block is not None:
            self._removeCoverBlock()
        
        for warning_block in self.warning_blocks.copy():
            self._removeWarningBlock(warning_block)
        
        for separator_block in self.separator_blocks.copy():
            self._removeSeparatorBlock(separator_block)
        
        for mod_file_block in self.mod_file_blocks.copy():
            self._removeModFileBlock(mod_file_block)
        
        self.warning_blocks.clear()
        self.separator_blocks.clear()
        self.mod_file_blocks.clear()
        self.sortable_blocks.clear()
        print("所有区块已清除")
    
    def _addCoverBlock(self):
        """添加封面区块"""
        if self.cover_block is not None:
            self._showCoverExistsWarning()
            return
        
        self.cover_block = CoverBlock(self.scrollWidget)
        self.cover_block.deleteRequested.connect(self._removeCoverBlock)
        insert_index = 2
        self.vBoxLayout.insertWidget(insert_index, self.cover_block)
    
    def _showCoverExistsWarning(self):
        """显示封面已存在的警告"""
        Flyout.create(
            icon=InfoBarIcon.WARNING,
            title=lang.get_text("cover_exists_title"),
            content=lang.get_text("cover_exists_content"),
            target=self.addFunctionCard.addCoverBtn,
            parent=self,
            isClosable=True
        )
    
    def _removeCoverBlock(self):
        """移除封面区块"""
        if self.cover_block is not None:
            self.vBoxLayout.removeWidget(self.cover_block)
            self.cover_block.deleteLater()
            self.cover_block = None
    
    def _addWarningBlock(self):
        """添加警告区块"""
        warning_block = WarningBlock(self.scrollWidget)
        warning_block.deleteRequested.connect(lambda: self._removeWarningBlock(warning_block))
        warning_block.copyRequested.connect(lambda: self._copyWarningBlock(warning_block))
        warning_block.moveRequested.connect(lambda: self._moveWarningBlock(warning_block))
        warning_block.dragStarted.connect(self._onDragStarted)
        warning_block.dragMoved.connect(self._onDragMoved)
        warning_block.dragEnded.connect(self._onDragEnded)
        insert_index = self._getSortableInsertIndex()
        self.warning_blocks.append(warning_block)
        self.sortable_blocks.append(warning_block)
        self.vBoxLayout.insertWidget(insert_index, warning_block)
    
    def _removeWarningBlock(self, warning_block):
        """移除警告区块"""
        if warning_block in self.warning_blocks:
            self.warning_blocks.remove(warning_block)
        if warning_block in self.sortable_blocks:
            self.sortable_blocks.remove(warning_block)
        self.vBoxLayout.removeWidget(warning_block)
        warning_block.deleteLater()
    
    def _copyWarningBlock(self, warning_block):
        """复制警告区块"""
        warning_data = warning_block.getWarningData()
        new_warning_block = WarningBlock(self.scrollWidget)
        new_warning_block.deleteRequested.connect(lambda: self._removeWarningBlock(new_warning_block))
        new_warning_block.copyRequested.connect(lambda: self._copyWarningBlock(new_warning_block))
        new_warning_block.moveRequested.connect(lambda: self._moveWarningBlock(new_warning_block))
        new_warning_block.dragStarted.connect(self._onDragStarted)
        new_warning_block.dragMoved.connect(self._onDragMoved)
        new_warning_block.dragEnded.connect(self._onDragEnded)

        if warning_data["description"]:
            new_warning_block.descriptionEdit.setPlainText(warning_data["description"])

        self.warning_blocks.append(new_warning_block)
        self.sortable_blocks.append(new_warning_block)
        
        original_index = self.vBoxLayout.indexOf(warning_block)
        if original_index >= 0:
            self.vBoxLayout.insertWidget(original_index + 1, new_warning_block)
    
    def _moveWarningBlock(self, warning_block):
        """移动警告区块（暂时实现为提示功能）"""
        # TODO: 待实现
        pass
    
    def _onDragStarted(self, block):
        """拖拽开始处理"""
        self.dragging_block = block
        self.drag_start_index = self.vBoxLayout.indexOf(block)
        move_btn = block.moveBtn
        btn_global_pos = move_btn.mapToGlobal(move_btn.rect().center())
        self._createDragProxy(block, btn_global_pos)
        self._createInsertIndicator()
        block.setStyleSheet("QWidget { opacity: 0.3; }")
    
    def _onDragMoved(self, block, global_pos):
        """拖拽移动处理"""
        if not self.dragging_block or self.dragging_block != block:
            return

        if self.drag_proxy:
            proxy_pos = self.mapFromGlobal(global_pos)
            self.drag_proxy.move(proxy_pos.x() - self.drag_proxy.width() // 2, 
                               proxy_pos.y() - 20)

        local_pos = self.scrollWidget.mapFromGlobal(global_pos)
        target_index = self._findSortableInsertPosition(local_pos.y())
        self._updateInsertIndicator(target_index)
    
    def _onDragEnded(self, block):
        """拖拽结束处理"""
        if not self.dragging_block or self.dragging_block != block:
            return

        if self.drag_proxy:
            proxy_center = self.drag_proxy.geometry().center()
            global_center = self.mapToGlobal(proxy_center)
            local_pos = self.scrollWidget.mapFromGlobal(global_center)
            target_index = self._findSortableInsertPosition(local_pos.y())

            if target_index != self.drag_start_index:
                self._moveSortableBlockToPosition(block, target_index)

        block.setStyleSheet("")
        
        self._cleanupDrag()
    
    def _findSortableInsertPosition(self, y_pos):
        """根据Y坐标查找可排序区块插入位置"""
        base_index = 2

        if self.cover_block is not None:
            base_index += 1

        if not self.sortable_blocks:
            return base_index

        for i, block in enumerate(self.sortable_blocks):
            block_geometry = block.geometry()
            block_top = block_geometry.y()
            
            extended_top = block_top + 10
            if y_pos < extended_top:
                return base_index + i
        
        last_block = self.sortable_blocks[-1]
        last_geometry = last_block.geometry()
        last_bottom = last_geometry.y() + last_geometry.height()
        
        if y_pos > last_bottom - 10:
            return base_index + len(self.sortable_blocks)
        
        return base_index + len(self.sortable_blocks)
    
    def _moveSortableBlockToPosition(self, block, target_index):
        """将可排序区块移动到指定位置"""
        original_index = self.vBoxLayout.indexOf(block)
        
        if target_index == original_index:
            return
        
        self.vBoxLayout.removeWidget(block)
        
        adjusted_target_index = target_index
        if original_index < target_index:
            adjusted_target_index -= 1
        
        self.vBoxLayout.insertWidget(adjusted_target_index, block)
        
        if block in self.sortable_blocks:
            old_list_index = self.sortable_blocks.index(block)
            self.sortable_blocks.remove(block)
            
            base_index = 2
            if self.cover_block is not None:
                base_index += 1
            
            new_list_index = adjusted_target_index - base_index
            new_list_index = max(0, min(new_list_index, len(self.sortable_blocks)))
            
            self.sortable_blocks.insert(new_list_index, block)
        
        if block in self.warning_blocks:
            self.warning_blocks.remove(block)
            warning_new_index = 0
            for i, sortable_block in enumerate(self.sortable_blocks[:new_list_index]):
                if sortable_block in self.warning_blocks:
                    warning_new_index += 1
            self.warning_blocks.insert(warning_new_index, block)
        
        if block in self.separator_blocks:
            self.separator_blocks.remove(block)
            separator_new_index = 0
            for i, sortable_block in enumerate(self.sortable_blocks[:new_list_index]):
                if sortable_block in self.separator_blocks:
                    separator_new_index += 1
            self.separator_blocks.insert(separator_new_index, block)
        
        if block in self.mod_file_blocks:
            self.mod_file_blocks.remove(block)
            mod_file_new_index = 0
            for i, sortable_block in enumerate(self.sortable_blocks[:new_list_index]):
                if sortable_block in self.mod_file_blocks:
                    mod_file_new_index += 1
            self.mod_file_blocks.insert(mod_file_new_index, block)
    
    def _createDragProxy(self, block, initial_pos):
        """创建拖拽代理"""
        pixmap = block.grab()
        
        self.drag_proxy = QLabel(self)
        self.drag_proxy.setPixmap(pixmap)
        
        if isDarkTheme():
            background_color = "rgba(0, 0, 0, 0.6)"
        else:
            background_color = "rgba(255, 255, 255, 0.6)"
        
        self.drag_proxy.setStyleSheet(f"""
            QLabel {{
                background-color: {background_color};
                border: 2px solid #0078d4;
                border-radius: 8px;
            }}
        """)
        self.drag_proxy.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        proxy_pos = self.mapFromGlobal(initial_pos)
        self.drag_proxy.move(proxy_pos.x() - self.drag_proxy.width() // 2, 
                           proxy_pos.y() - self.drag_proxy.height() // 2)
        
        self.drag_proxy.show()
        self.drag_proxy.raise_()
    
    def _createInsertIndicator(self):
        """创建插入位置指示器"""
        self.drag_insert_indicator = QLabel(self.scrollWidget)
        self.drag_insert_indicator.setFixedHeight(3)
        self.drag_insert_indicator.setStyleSheet("""
            QLabel {
                background-color: #0078d4;
                border-radius: 1px;
            }
        """)
        self.drag_insert_indicator.hide()
    
    def _updateInsertIndicator(self, target_index):
        """更新插入位置指示器"""
        if not self.drag_insert_indicator:
            return
        
        if target_index < self.vBoxLayout.count():
            target_widget = self.vBoxLayout.itemAt(target_index).widget()
            if target_widget:
                indicator_y = target_widget.y() - 2
            else:
                indicator_y = 0
        else:
            last_widget = self.vBoxLayout.itemAt(self.vBoxLayout.count() - 1).widget()
            if last_widget:
                indicator_y = last_widget.y() + last_widget.height() + 2
            else:
                indicator_y = 0
        
        self.drag_insert_indicator.setGeometry(20, indicator_y, 
                                             self.scrollWidget.width() - 40, 3)
        self.drag_insert_indicator.show()
        self.drag_insert_indicator.raise_()
    
    def _cleanupDrag(self):
        """清理拖拽相关对象"""
        if self.drag_proxy:
            self.drag_proxy.hide()
            self.drag_proxy.setParent(None)
            self.drag_proxy = None
        
        if self.drag_insert_indicator:
            self.drag_insert_indicator.hide()
            self.drag_insert_indicator.setParent(None)
            self.drag_insert_indicator = None
        
        if self.dragging_block:
            self.dragging_block.is_dragging = False
            self.dragging_block.drag_start_pos = None
            self.dragging_block.moveBtn.setCursor(Qt.CursorShape.OpenHandCursor)
        
        self.dragging_block = None
        self.drag_start_index = -1
    
    def _getSortableInsertIndex(self):
        """获取可排序区块插入位置索引"""
        base_index = 2
        
        if self.cover_block is not None:
            base_index += 1
        
        if self.sortable_blocks:
            last_sortable_block = self.sortable_blocks[-1]
            last_index = self.vBoxLayout.indexOf(last_sortable_block)
            return last_index + 1
        else:
            return base_index
    
    def _addSeparatorBlock(self):
        """添加分割线区块"""
        separator_block = SeparatorBlock(self.scrollWidget)
        separator_block.deleteRequested.connect(lambda: self._removeSeparatorBlock(separator_block))
        separator_block.copyRequested.connect(lambda: self._copySeparatorBlock(separator_block))
        separator_block.moveRequested.connect(lambda: self._moveSeparatorBlock(separator_block))
        separator_block.dragStarted.connect(self._onDragStarted)
        separator_block.dragMoved.connect(self._onDragMoved)
        separator_block.dragEnded.connect(self._onDragEnded)
        insert_index = self._getSortableInsertIndex()
        self.separator_blocks.append(separator_block)
        self.sortable_blocks.append(separator_block)
        self.vBoxLayout.insertWidget(insert_index, separator_block)
    
    def _removeSeparatorBlock(self, separator_block):
        """移除分割线区块"""
        if separator_block in self.separator_blocks:
            self.separator_blocks.remove(separator_block)
        if separator_block in self.sortable_blocks:
            self.sortable_blocks.remove(separator_block)
        self.vBoxLayout.removeWidget(separator_block)
        separator_block.deleteLater()
    
    def _copySeparatorBlock(self, separator_block):
        """复制分割线区块"""
        separator_data = separator_block.getSeparatorData()
        new_separator_block = SeparatorBlock(self.scrollWidget)
        new_separator_block.deleteRequested.connect(lambda: self._removeSeparatorBlock(new_separator_block))
        new_separator_block.copyRequested.connect(lambda: self._copySeparatorBlock(new_separator_block))
        new_separator_block.moveRequested.connect(lambda: self._moveSeparatorBlock(new_separator_block))
        new_separator_block.dragStarted.connect(self._onSeparatorDragStarted)
        new_separator_block.dragMoved.connect(self._onSeparatorDragMoved)
        new_separator_block.dragEnded.connect(self._onSeparatorDragEnded)
        new_separator_block.setSeparatorData(separator_data)
        self.separator_blocks.append(new_separator_block)
        self.sortable_blocks.append(new_separator_block)

        original_index = self.vBoxLayout.indexOf(separator_block)
        if original_index >= 0:
            self.vBoxLayout.insertWidget(original_index + 1, new_separator_block)
    
    def _moveSeparatorBlock(self, separator_block):
        """移动分割线区块（暂时实现为提示功能）"""
        # TODO: 待实现
        # 这里可以显示一个提示，告诉用户如何移动区块
        pass    
    
    def _addModFilesBlock(self):
        """添加MOD文件区块"""
        mod_file_block = ModFileBlock(self.scrollWidget)
        mod_file_block.deleteRequested.connect(lambda: self._removeModFileBlock(mod_file_block))
        mod_file_block.copyRequested.connect(lambda: self._copyModFileBlock(mod_file_block))
        mod_file_block.moveRequested.connect(lambda: self._moveModFileBlock(mod_file_block))
        mod_file_block.dragStarted.connect(self._onDragStarted)
        mod_file_block.dragMoved.connect(self._onDragMoved)
        mod_file_block.dragEnded.connect(self._onDragEnded)
        insert_index = self._getSortableInsertIndex()
        self.mod_file_blocks.append(mod_file_block)
        self.sortable_blocks.append(mod_file_block)
        self.vBoxLayout.insertWidget(insert_index, mod_file_block)
    
    def _removeModFileBlock(self, mod_file_block):
        """移除MOD文件区块"""
        if mod_file_block in self.mod_file_blocks:
            self.mod_file_blocks.remove(mod_file_block)
        if mod_file_block in self.sortable_blocks:
            self.sortable_blocks.remove(mod_file_block)
        self.vBoxLayout.removeWidget(mod_file_block)
        mod_file_block.deleteLater()
    
    def _copyModFileBlock(self, mod_file_block):
        """复制MOD文件区块"""
        mod_file_data = mod_file_block.getModFileData()
        new_mod_file_block = ModFileBlock(self.scrollWidget)
        new_mod_file_block.deleteRequested.connect(lambda: self._removeModFileBlock(new_mod_file_block))
        new_mod_file_block.copyRequested.connect(lambda: self._copyModFileBlock(new_mod_file_block))
        new_mod_file_block.moveRequested.connect(lambda: self._moveModFileBlock(new_mod_file_block))
        new_mod_file_block.dragStarted.connect(self._onDragStarted)
        new_mod_file_block.dragMoved.connect(self._onDragMoved)
        new_mod_file_block.dragEnded.connect(self._onDragEnded)
        new_mod_file_block.setModFileData(mod_file_data)
        self.mod_file_blocks.append(new_mod_file_block)
        self.sortable_blocks.append(new_mod_file_block)
        original_index = self.vBoxLayout.indexOf(mod_file_block)
        if original_index >= 0:
            self.vBoxLayout.insertWidget(original_index + 1, new_mod_file_block)
    
    def _moveModFileBlock(self, mod_file_block):
        """移动MOD文件区块（暂时实现为提示功能）"""
        # TODO: 待实现
        pass
    
    def getCoverData(self):
        """获取封面数据"""
        if self.cover_block:
            return self.cover_block.getCoverData()
        return None
    
    def getWarningData(self):
        """获取所有警告区块数据"""
        warning_data = []
        for warning_block in self.warning_blocks:
            warning_data.append(warning_block.getWarningData())
        return warning_data
    
    def getSeparatorData(self):
        """获取所有分割线区块数据"""
        separator_data = []
        for separator_block in self.separator_blocks:
            separator_data.append(separator_block.getSeparatorData())
        return separator_data
    
    def getModFileData(self):
        """获取所有MOD文件区块数据"""
        mod_file_data = []
        for mod_file_block in self.mod_file_blocks:
            mod_file_data.append(mod_file_block.getModFileData())
        return mod_file_data
    
    def _getSortedBlocksData(self):
        """获取排序后的区块数据"""
        sorted_blocks = []
        
        # Traverse the sortable block list to get the data in the current order
        for block in self.sortable_blocks:
            if block in self.warning_blocks:
                warning_data = block.getWarningData()
                warning_data["type"] = "warning"
                sorted_blocks.append(warning_data)
            elif block in self.separator_blocks:
                separator_data = block.getSeparatorData()
                separator_data["type"] = "separator"
                sorted_blocks.append(separator_data)
            elif block in self.mod_file_blocks:
                mod_file_data = block.getModFileData()
                mod_file_data["type"] = "mod_file"
                sorted_blocks.append(mod_file_data)
        
        return sorted_blocks
    
    def _onBuildStarted(self):
        """构建开始处理"""
        print("构建开始")
    
    def _onBuildProgressChanged(self, progress: int):
        """构建进度变化处理"""
        print(f"构建进度: {progress}%")
    
    def _onBuildStatusChanged(self, status: str):
        """构建状态变化处理"""
        print(f"构建状态: {status}")
    
    def _onBuildCompleted(self, output_path: str):
        """构建完成处理"""
        InfoBar.success(
            title=lang.get_text("build_success_title"),
            content=f"{lang.get_text('build_success_content')}: {output_path}",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=5000,
            parent=self
        )
        print(f"构建完成: {output_path}")
    
    def _onBuildFailed(self, error_msg: str):
        """构建失败处理"""
        InfoBar.error(
            title=lang.get_text("build_failed_title"),
            content=f"{lang.get_text('build_failed_content')}: {error_msg}",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=8000,
            parent=self
        )
        print(f"构建失败: {error_msg}")
    
    def resizeEvent(self, event):
        """窗口大小变化事件"""
        super().resizeEvent(event)
        if hasattr(self, 'floatingMenuButton'):
            self.floatingMenuButton.updatePosition()
        if self.sticky_add_function_card and self.is_add_function_sticky:
            self._updateStickyAddFunctionCardGeometry()
    
    def _createStickyAddFunctionCard(self):
        """创建固定在顶部的AddFunctionCard副本"""
        self.sticky_add_function_card = AddFunctionCard(self)
        self.sticky_add_function_card.hide()
        self.sticky_add_function_card.setObjectName("sticky_add_function_card")
        self.sticky_add_function_card.addCoverRequested.connect(self._addCoverBlock)
        self.sticky_add_function_card.addWarningRequested.connect(self._addWarningBlock)
        self.sticky_add_function_card.addSeparatorRequested.connect(self._addSeparatorBlock)
        self.sticky_add_function_card.addModFilesRequested.connect(self._addModFilesBlock)

        self._addAcrylicEffect()
        self._updateStickyCardStyle()

        from qfluentwidgets import qconfig
        qconfig.themeChanged.connect(self._updateStickyCardStyle)
    
    def _onScrollValueChanged(self, value):
        """滚动值变化处理"""
        if not self.addFunctionCard or not self.sticky_add_function_card:
            return

        add_function_rect = self.addFunctionCard.geometry()
        scroll_area_rect = self.viewport().rect()
        scroll_offset = self.verticalScrollBar().value()
        add_function_top = add_function_rect.top() - scroll_offset
        should_be_sticky = add_function_top <= 0
        
        if should_be_sticky and not self.is_add_function_sticky:
            self._showStickyAddFunctionCard()
        elif not should_be_sticky and self.is_add_function_sticky:
            self._hideStickyAddFunctionCard()
    
    def _showStickyAddFunctionCard(self):
        """显示固定的AddFunctionCard"""
        if not self.sticky_add_function_card:
            return
        
        self.is_add_function_sticky = True
        self._updateStickyAddFunctionCardGeometry()
        self.sticky_add_function_card.show()
        self.sticky_add_function_card.raise_()
    
    def _hideStickyAddFunctionCard(self):
        """隐藏固定的AddFunctionCard"""
        if not self.sticky_add_function_card:
            return
        
        self.is_add_function_sticky = False
        self.sticky_add_function_card.hide()
    
    def _updateStickyAddFunctionCardGeometry(self):
        """更新固定AddFunctionCard的几何位置"""
        if not self.sticky_add_function_card or not self.addFunctionCard:
            return
        
        original_size = self.addFunctionCard.size()
        viewport_rect = self.viewport().rect()
        margins = self.vBoxLayout.contentsMargins()
        x = margins.left()
        y = 10
        width = viewport_rect.width() - margins.left() - margins.right()
        height = original_size.height()
        
        self.sticky_add_function_card.setGeometry(x, y, width, height)
    
    def _updateStickyCardStyle(self):
        """更新固定卡片的样式（支持主题切换）"""
        if not self.sticky_add_function_card:
            return
        
        if isDarkTheme():
            background_color = "rgba(32, 32, 32, 200)"
            border_color = "rgba(255, 255, 255, 0.2)"
        else:
            background_color = "rgba(255, 255, 255, 200)"
            border_color = "rgba(0, 0, 0, 0.15)"
        
        style = f"""
            QWidget#sticky_add_function_card {{
                background-color: {background_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
            QWidget#sticky_add_function_card > QWidget {{
                background-color: transparent;
            }}
            QWidget#sticky_add_function_card GroupHeaderCardWidget {{
                background-color: transparent;
            }}
        """
        
        self.sticky_add_function_card.setStyleSheet(style)
    
    def _addAcrylicEffect(self):
        """为固定卡片添加亚克力模糊效果"""
        if not self.sticky_add_function_card:
            return
        
        self.sticky_add_function_card.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)        
        self._createAcrylicBackground()
    
    def _createAcrylicBackground(self):
        """创建亚克力背景效果"""
        original_paint_event = self.sticky_add_function_card.paintEvent
        
        def acrylic_paint_event(event):
            from PySide6.QtGui import QPainter, QBrush, QColor
            from PySide6.QtCore import QRect
            
            painter = QPainter(self.sticky_add_function_card)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            rect = self.sticky_add_function_card.rect()
            if isDarkTheme():
                bg_color = QColor(32, 32, 32, 200)
                border_color = QColor(255, 255, 255, 10)
            else:
                bg_color = QColor(255, 255, 255, 200)
                border_color = QColor(0, 0, 0, 38)
            
            painter.setBrush(QBrush(bg_color))
            painter.setPen(border_color)
            painter.drawRoundedRect(rect, 12, 12)
            painter.end()
            original_paint_event(event)
        
        self.sticky_add_function_card.paintEvent = acrylic_paint_event