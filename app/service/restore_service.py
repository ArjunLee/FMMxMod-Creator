# coding:utf-8
"""
Restore Service
还原服务 - 实现【再度编撰】功能
"""
from PySide6.QtCore import QObject, Signal
from ..components.cover_block import CoverBlock
from ..components.warning_block import WarningBlock
from ..components.separator_block import SeparatorBlock
from ..components.mod_file_block import ModFileBlock
from ..common.language import lang

class RestoreService(QObject):
    """还原服务类"""
    
    # signal definition
    restoreStarted = Signal()    # Restore start signal
    restoreCompleted = Signal()  # Restore complete signal
    restoreFailed = Signal(str)  # Restore failure signal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.home_interface = None
    
    def setHomeInterface(self, home_interface):
        """设置主页界面引用"""
        self.home_interface = home_interface
    
    def restoreFromRecord(self, record_data: dict):
        """
        从记录数据还原编辑器布局
        
        Args:
            record_data: 构建记录数据
        """
        try:
            self.restoreStarted.emit()
            
            if not self.home_interface:
                raise Exception(lang.get_text("home_interface_not_set"))
            
            # Clear current layout
            self._clearCurrentLayout()
            
            # Restore MOD basic information
            self._restoreModInfo(record_data.get("mod_info", {}))
            
            # Restore cover block
            self._restoreCoverBlock(record_data.get("cover_block", {}))
            
            # Restore content blocks (in order)
            self._restoreContentBlocks(record_data.get("content_blocks", []))
            
            # Add stretch spacing to the layout end
            self.home_interface.vBoxLayout.addStretch(1)
            
            self.restoreCompleted.emit()
            
        except Exception as e:
            self.restoreFailed.emit(str(e))
    
    def _clearCurrentLayout(self):
        """清空当前布局"""
        for block in self.home_interface.sortable_blocks[:]:
            if block in self.home_interface.warning_blocks:
                self.home_interface.warning_blocks.remove(block)
            elif block in self.home_interface.separator_blocks:
                self.home_interface.separator_blocks.remove(block)
            elif block in self.home_interface.mod_file_blocks:
                self.home_interface.mod_file_blocks.remove(block)
            
            self.home_interface.vBoxLayout.removeWidget(block)
            block.deleteLater()
        
        self.home_interface.sortable_blocks.clear()
        
        if self.home_interface.cover_block:
            self.home_interface.vBoxLayout.removeWidget(self.home_interface.cover_block)
            self.home_interface.cover_block.deleteLater()
            self.home_interface.cover_block = None
        
        layout = self.home_interface.vBoxLayout

        for i in range(layout.count() - 1, -1, -1):
            item = layout.itemAt(i)
            if item and item.spacerItem():
                layout.removeItem(item)
    
    def _restoreModInfo(self, mod_info: dict):
        """还原MOD基本信息"""
        if not mod_info:
            return
        
        mod_info_card = self.home_interface.modInfoCard
        
        if "name" in mod_info:
            mod_info_card.modNameEdit.setText(mod_info["name"])
        
        if "version" in mod_info:
            mod_info_card.versionEdit.setText(mod_info["version"])
        
        if "author" in mod_info:
            mod_info_card.authorEdit.setText(mod_info["author"])
        
        if "category" in mod_info:
            mod_info_card.categoryEdit.setText(mod_info["category"])
    
    def _restoreCoverBlock(self, cover_data: dict):
        """还原封面区块"""
        if not cover_data:
            return
        
        cover_block = CoverBlock(self.home_interface.scrollWidget)
        cover_block.deleteRequested.connect(self.home_interface._removeCoverBlock)
        
        self._setCoverBlockData(cover_block, cover_data)
        
        insert_index = 2
        self.home_interface.vBoxLayout.insertWidget(insert_index, cover_block)
        self.home_interface.cover_block = cover_block
    
    def _setCoverBlockData(self, cover_block, cover_data: dict):
        """设置封面区块数据"""
        cover_block.setCoverData(cover_data)
    
    def _restoreContentBlocks(self, content_blocks: list):
        """还原内容区块"""
        base_insert_index = 3
        
        for i, block_data in enumerate(content_blocks):
            block_type = block_data.get("type", "")
            current_insert_index = base_insert_index + i
            
            if block_type == "warning":
                self._restoreWarningBlock(block_data, current_insert_index)
            elif block_type == "separator":
                self._restoreSeparatorBlock(block_data, current_insert_index)
            elif block_type == "mod_file":
                self._restoreModFileBlock(block_data, current_insert_index)
    
    def _restoreWarningBlock(self, warning_data: dict, insert_index: int):
        """还原警告区块"""
        warning_block = WarningBlock(self.home_interface.scrollWidget)
        
        # connection signal
        warning_block.deleteRequested.connect(lambda: self.home_interface._removeWarningBlock(warning_block))
        warning_block.copyRequested.connect(lambda: self.home_interface._copyWarningBlock(warning_block))
        warning_block.moveRequested.connect(lambda: self.home_interface._moveWarningBlock(warning_block))
        warning_block.dragStarted.connect(self.home_interface._onDragStarted)
        warning_block.dragMoved.connect(self.home_interface._onDragMoved)
        warning_block.dragEnded.connect(self.home_interface._onDragEnded)
        
        self._setWarningBlockData(warning_block, warning_data)
        self.home_interface.warning_blocks.append(warning_block)
        self.home_interface.sortable_blocks.append(warning_block)
        self.home_interface.vBoxLayout.insertWidget(insert_index, warning_block)
    
    def _setWarningBlockData(self, warning_block, warning_data: dict):
        """设置警告区块数据"""
        # Set the warning text (using the description field in JSON)
        description = warning_data.get("description", "")
        if description:
            warning_block.descriptionEdit.setPlainText(description)
        
        # Set the block tag (using the block_tag field in JSON)
        block_tag = warning_data.get("block_tag", "")
        if block_tag:
            warning_block.areaMarkEdit.setText(block_tag)
        
        # Set the image path
        image_path = warning_data.get("image_path", "")
        if image_path:
            warning_block.imageUpload._displayImage(image_path)
            warning_block.imageUpload.image_path = image_path
    
    def _restoreSeparatorBlock(self, separator_data: dict, insert_index: int):
        """还原分割线区块"""
        separator_block = SeparatorBlock(self.home_interface.scrollWidget)
        
        # connection signal
        separator_block.deleteRequested.connect(lambda: self.home_interface._removeSeparatorBlock(separator_block))
        separator_block.copyRequested.connect(lambda: self.home_interface._copySeparatorBlock(separator_block))
        separator_block.moveRequested.connect(lambda: self.home_interface._moveSeparatorBlock(separator_block))
        separator_block.dragStarted.connect(self.home_interface._onDragStarted)
        separator_block.dragMoved.connect(self.home_interface._onDragMoved)
        separator_block.dragEnded.connect(self.home_interface._onDragEnded)
        
        self._setSeparatorBlockData(separator_block, separator_data)
        self.home_interface.separator_blocks.append(separator_block)
        self.home_interface.sortable_blocks.append(separator_block)
        self.home_interface.vBoxLayout.insertWidget(insert_index, separator_block)
    
    def _setSeparatorBlockData(self, separator_block, separator_data: dict):
        """设置分割线区块数据"""
        separator_name = separator_data.get("separator_name", "")
        if separator_name:
            separator_block.separatorNameEdit.setText(separator_name)
        
        area_mark = separator_data.get("area_mark", "")
        if area_mark and hasattr(separator_block, 'areaMarkEdit'):
            separator_block.areaMarkEdit.setText(area_mark)
    
    def _restoreModFileBlock(self, mod_file_data: dict, insert_index: int):
        """还原MOD文件区块"""
        mod_file_block = ModFileBlock(self.home_interface.scrollWidget)
        
        # connection signal
        mod_file_block.deleteRequested.connect(lambda: self.home_interface._removeModFileBlock(mod_file_block))
        mod_file_block.copyRequested.connect(lambda: self.home_interface._copyModFileBlock(mod_file_block))
        mod_file_block.moveRequested.connect(lambda: self.home_interface._moveModFileBlock(mod_file_block))
        mod_file_block.dragStarted.connect(self.home_interface._onDragStarted)
        mod_file_block.dragMoved.connect(self.home_interface._onDragMoved)
        mod_file_block.dragEnded.connect(self.home_interface._onDragEnded)
        
        self._setModFileBlockData(mod_file_block, mod_file_data)
        self.home_interface.mod_file_blocks.append(mod_file_block)
        self.home_interface.sortable_blocks.append(mod_file_block)
        self.home_interface.vBoxLayout.insertWidget(insert_index, mod_file_block)
    
    def _setModFileBlockData(self, mod_file_block, mod_file_data: dict):
        """设置MOD文件区块数据"""
        module_name = mod_file_data.get("module_name", "")
        if module_name:
            mod_file_block.moduleNameEdit.setText(module_name)
        
        area_mark = mod_file_data.get("area_mark", "")
        if area_mark:
            mod_file_block.areaMarkEdit.setText(area_mark)
        
        image_path = mod_file_data.get("image_path", "")
        if image_path:
            mod_file_block.imageUpload._displayImage(image_path)
            mod_file_block.imageUpload.image_path = image_path
        
        description = mod_file_data.get("description", "")
        if description:
            mod_file_block.descriptionEdit.setPlainText(description)
        
        files = mod_file_data.get("files", [])
        if files:
            mod_file_block.filesDisplayWidget.clearFiles()
            
            file_paths = [file_info.get("file_path", "") for file_info in files if file_info.get("file_path", "")]
            if file_paths:
                mod_file_block.filesDisplayWidget.addFiles(file_paths)