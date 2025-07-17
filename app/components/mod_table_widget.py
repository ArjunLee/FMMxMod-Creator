# coding:utf-8
"""
MOD Table Widget
MOD表格组件
"""
import os
import json
from datetime import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QHeaderView, QTableWidgetItem,
    QAbstractItemView, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from qfluentwidgets import (
    TableWidget, MessageBox, FluentIcon as FIF,
    RoundMenu, Action, PrimaryDropDownToolButton, InfoBar, InfoBarPosition
)
from ..common.language import lang
from ..common.application import FMMApplication

class ModTableWidget(QWidget):
    """MOD表格组件"""

    recordDeleted = Signal()
    recordEdited = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_edit_mode = False  # Edit mode status switch
        self._initUI()
        lang.languageChanged.connect(self._updateTexts)
    
    def _initUI(self):
        """初始化界面"""
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self._createTable() # Create table
        self.vBoxLayout.addWidget(self.modTable)

        self.setStyleSheet("""
            ModTableWidget {
                background-color: transparent;
                border: none;
            }
        """)
    
    def _createTable(self):
        """创建表格"""
        self.modTable = TableWidget()
        
        headers = [
            lang.get_text("serial_number"),
            lang.get_text("mod_name"),
            lang.get_text("author"), 
            lang.get_text("category"),
            lang.get_text("cover_image"),
            lang.get_text("version"),
            lang.get_text("create_date"),
            lang.get_text("operations")
        ]
        
        self.modTable.setColumnCount(len(headers))
        self.modTable.setHorizontalHeaderLabels(headers)
        self.modTable.setBorderVisible(True)
        self.modTable.setBorderRadius(8)
        self.modTable.setWordWrap(False)
        self.modTable.setRowCount(0)
        self.modTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.modTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        
        # Set column width - allows users to adjust
        header = self.modTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)        # Serial number
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)      # MOD name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)  # Author
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)  # Category
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)  # Cover image
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Interactive)  # Version
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Interactive)  # Create date
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)        # Operations
        
        # Set default column width
        self.modTable.setColumnWidth(0, 60)       # Serial number
        self.modTable.setColumnWidth(2, 115)      # Author
        self.modTable.setColumnWidth(3, 122)      # Category
        self.modTable.setColumnWidth(4, 294)      # Cover image
        self.modTable.setColumnWidth(5, 128)      # Version
        self.modTable.setColumnWidth(6, 157)      # Create date
        self.modTable.setColumnWidth(7, 160)      # Operations
        
        # Set row height to 150
        self.modTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.modTable.verticalHeader().setDefaultSectionSize(150)
        
        # Hide default row number
        self.modTable.verticalHeader().setVisible(False)
        
        # Set table height
        self._updateTableHeight()

        self.modTable.itemChanged.connect(self._onItemChanged)
        self.modTable.horizontalHeader().sectionResized.connect(self._onColumnResized)
        self.modTable.itemDoubleClicked.connect(self._onItemDoubleClicked)
        self._loadTableConfig()
    
    def loadData(self):
        """加载表格数据"""
        try:
            # Get build log file path
            cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
            record_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
            
            if not os.path.exists(record_file):
                self.modTable.setRowCount(0)
                return
            
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Empty existing data and add new data
            self.modTable.setRowCount(0)
            for i, record in enumerate(data):
                self._addTableRow(i, record)
            
            self._updateTableHeight()
            from PySide6.QtCore import QTimer
            QTimer.singleShot(200, lambda: (
                self._loadTableConfig(),
                self._ensureRowHeight()
            ))
                
        except Exception as e:
            self._updateTableHeight()
    
    def _addTableRow(self, row: int, record: dict):
        """添加表格行"""
        self.modTable.insertRow(row)
        mod_info = record.get("mod_info", {})
        build_info = record.get("build_info", {})
        cover_block = record.get("cover_block", {})
        serial_item = QTableWidgetItem(str(row + 1))
        serial_item.setData(Qt.ItemDataRole.UserRole, record)
        serial_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        serial_item.setFlags(serial_item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        self.modTable.setItem(row, 0, serial_item)
        name_item = QTableWidgetItem(mod_info.get("name", ""))
        name_item.setData(Qt.ItemDataRole.UserRole, record)

        self.modTable.setItem(row, 1, name_item)
        author_item = QTableWidgetItem(mod_info.get("author", ""))
        author_item.setData(Qt.ItemDataRole.UserRole, record)
        author_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.modTable.setItem(row, 2, author_item)
        category_item = QTableWidgetItem(mod_info.get("category", ""))
        category_item.setData(Qt.ItemDataRole.UserRole, record)
        category_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.modTable.setItem(row, 3, category_item)
        self._addCoverImage(row, cover_block, record)
        version_text = mod_info.get("version", "")

        if version_text and (".jpg" in version_text.lower() or ".png" in version_text.lower() or ".gif" in version_text.lower()):
            from ..common import version_info
            version_text = version_info.VERSION_STRING

        version_item = QTableWidgetItem(version_text)
        version_item.setData(Qt.ItemDataRole.UserRole, record)
        version_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.modTable.setItem(row, 5, version_item)
        build_time = build_info.get("build_time", "")

        if build_time:
            try:
                dt = datetime.fromisoformat(build_time)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M")
            except:
                formatted_time = build_time
        else:
            formatted_time = ""

        date_item = QTableWidgetItem(formatted_time)
        date_item.setData(Qt.ItemDataRole.UserRole, record)
        date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.modTable.setItem(row, 6, date_item)
        self._addOperationButtons(row, record)
        
        for col in [1, 2, 3, 5]:  # Columns allowed for editing: MOD name, author, category, version
            item = self.modTable.item(row, col)
            if item:
                if self.is_edit_mode:
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                else:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    
    def _addCoverImage(self, row: int, cover_block: dict, record: dict):
        """添加封面图片"""
        container_widget = QWidget()
        container_layout = QHBoxLayout(container_widget)
        container_layout.setContentsMargins(5, 5, 5, 5)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setStyleSheet("""
            QLabel {
                border: 0px solid #262D32;
                border-radius: 12px;
            }
        """)
        image_path = cover_block.get("image_path", "")
        
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(scaled_pixmap)
                image_label.setFixedSize(scaled_pixmap.size())
            else:
                image_label.setText(lang.get_text("image_load_failed"))
                image_label.setFixedSize(120, 120)
        else:
            image_label.setText(lang.get_text("no_cover"))
            image_label.setFixedSize(120, 120)
        
        container_layout.addStretch()
        container_layout.addWidget(image_label)
        container_layout.addStretch()

        self.modTable.setCellWidget(row, 4, container_widget)
    
    def _addOperationButtons(self, row: int, record: dict):
        """添加操作按钮"""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(5, 2, 5, 2)
        menu = RoundMenu(parent=button_widget)
        revise_action = Action(FIF.EDIT, lang.get_text("revise_again"))
        revise_action.triggered.connect(lambda: self._onEditRecord(record))
        menu.addAction(revise_action)
        delete_action = Action(FIF.DELETE, lang.get_text("delete_record"))
        delete_action.triggered.connect(lambda: self._onDeleteRecord(record, row))
        menu.addAction(delete_action)
        
        edit_dropdown_btn = PrimaryDropDownToolButton(FIF.EDIT, button_widget)
        edit_dropdown_btn.setMenu(menu)
        edit_dropdown_btn.setFixedSize(64, 32)
        edit_dropdown_btn.setToolTip(lang.get_text("operations"))

        button_layout.addStretch()
        button_layout.addWidget(edit_dropdown_btn)
        button_layout.addStretch()
        
        self.modTable.setCellWidget(row, 7, button_widget)
    

    def _onEditRecord(self, record: dict):
        """编辑记录 - 还原工作区功能"""
        try:
            # Import Workspace Layout Restore Service
            from ..service.restore_service import RestoreService
            from qfluentwidgets import InfoBar, InfoBarPosition
            
            # Create a restore service instance
            restore_service = RestoreService(self)
            
            # Get the main window and home interface
            main_window = self.parent.parent  # mod_list_interface -> main_window
            home_interface = main_window.homeInterface
            
            # Set the home interface reference
            restore_service.setHomeInterface(home_interface)
            
            # Connect the restore service signals
            restore_service.restoreCompleted.connect(lambda: self._onRestoreCompleted(main_window))
            restore_service.restoreFailed.connect(self._onRestoreFailed)
            
            # Execute restoration
            restore_service.restoreFromRecord(record)
            
        except Exception as e:
            InfoBar.error(
                title=lang.get_text("error"),
                content=lang.get_text("restore_failed").format(error=str(e)),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
    
    def _onRestoreCompleted(self, main_window):
        """还原完成处理"""
        main_window.switchTo(main_window.homeInterface)
        
        InfoBar.success(
            title=lang.get_text("restore_success_title"),
            content=lang.get_text("restore_success_content"),
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=main_window
        )
    
    def _onRestoreFailed(self, error_msg: str):
        """还原失败处理"""
        InfoBar.error(
            title=lang.get_text("restore_failed_title"),
            content=lang.get_text("restore_failed_content").format(error=str(error_msg)),
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def _onDeleteRecord(self, record: dict, row: int):
        """删除记录"""
        mod_name = record.get("mod_info", {}).get("name", "")
        title = lang.get_text("delete_mod_record_title")
        content = lang.get_text("delete_mod_record_content").format(mod_name=mod_name)
        dialog = MessageBox(title, content, self)
        dialog.yesButton.setText(lang.get_text("confirm"))
        dialog.cancelButton.setText(lang.get_text("cancel"))
        
        if dialog.exec():
            if self._deleteRecordByIndex(row):
                self.refresh()
                self.recordDeleted.emit()
    
    def _deleteRecordByIndex(self, row_index: int) -> bool:
        """根据行索引删除记录"""
        try:
            cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
            record_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
            
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if row_index < 0 or row_index >= len(data):
                return False
            
            data.pop(row_index)
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"删除记录失败: {e}")
            return False
    
    def _deleteRecordFromFile(self, record_to_delete: dict) -> bool:
        """从文件中删除记录（保留用于兼容性）"""
        try:
            record_file = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache", "FMMxMOD-Creator_build-record.json")
            
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            target_build_time = record_to_delete.get("build_info", {}).get("build_time", "")
            
            original_length = len(data)
            data = [record for record in data 
                   if record.get("build_info", {}).get("build_time", "") != target_build_time]
            
            if len(data) == original_length:
                return False
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
                
        except Exception as e:
            return False
    
    def _onItemChanged(self, item: QTableWidgetItem):
        """表格项变化时的处理"""
        if item is None or not self.is_edit_mode:
            return
        
        record = item.data(Qt.ItemDataRole.UserRole)
        if not record:
            return
        
        row = item.row()
        column = item.column()
        new_value = item.text()
        
        if column == 1:
            record["mod_info"]["name"] = new_value
        elif column == 2:
            record["mod_info"]["author"] = new_value
        elif column == 3:
            record["mod_info"]["category"] = new_value
        elif column == 5:
            record["mod_info"]["version"] = new_value
        else:
            return

        self._updateRecordInFile(record)
    
    def _updateRecordInFile(self, updated_record: dict):
        """更新文件中的记录"""
        try:
            record_file = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache", "FMMxMOD-Creator_build-record.json")
            
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            target_build_time = updated_record.get("build_info", {}).get("build_time", "")
            
            for i, record in enumerate(data):
                if record.get("build_info", {}).get("build_time", "") == target_build_time:
                    if "mod_info" in updated_record:
                        if "mod_info" not in record:
                            record["mod_info"] = {}
                        for key in ["name", "author", "category", "version"]:
                            if key in updated_record["mod_info"]:
                                record["mod_info"][key] = updated_record["mod_info"][key]
                    break
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            pass
    
    def _updateTableHeight(self):
        """更新表格高度"""
        try:
            # Read app_config get window height
            config_path = os.path.join(FMMApplication.getConfigPath(), "app_config.json")
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            window_height = config.get("window_height", 800)
            min_height = window_height - 170
            row_count = self.modTable.rowCount()
            cell_height = 150
            content_height = (row_count + 1) * cell_height
            table_height = max(min_height, content_height)
            
            self.modTable.setMinimumHeight(min_height)
            self.modTable.setMaximumHeight(table_height)
            
        except Exception as e:
            # If reading the configuration fails, use the default value
            window_height = 950
            min_height = window_height - 170
            row_count = self.modTable.rowCount()
            cell_height = 150
            content_height = (row_count + 1) * cell_height
            table_height = max(min_height, content_height)
            self.modTable.setMinimumHeight(min_height)
            self.modTable.setMaximumHeight(table_height)
    
    def _updateTexts(self):
        """更新界面文本"""
        headers = [
            lang.get_text("serial_number"),
            lang.get_text("mod_name"),
            lang.get_text("author"), 
            lang.get_text("category"),
            lang.get_text("cover_image"),
            lang.get_text("version"),
            lang.get_text("create_date"),
            lang.get_text("operations")
        ]
        self.modTable.setHorizontalHeaderLabels(headers)
        self._updateMenuTexts()
    
    def _updateMenuTexts(self):
        """更新菜单文本而不重建表格"""
        try:
            for row in range(self.modTable.rowCount()):
                button_widget = self.modTable.cellWidget(row, 7)
                if button_widget:
                    for child in button_widget.findChildren(PrimaryDropDownToolButton):
                        menu = child.menu()
                        if menu:
                            actions = menu.actions()
                            if len(actions) >= 2:
                                actions[0].setText(lang.get_text("revise_again"))
                                actions[1].setText(lang.get_text("delete_record"))
                        child.setToolTip(lang.get_text("operations"))
        except Exception as e:
            self.loadData()
    
    def _getConfigPath(self):
        """获取配置文件路径"""
        from ..common.application import FMMApplication
        return str(FMMApplication.getConfigPath("mod_list_table_config.json"))
    
    def _loadTableConfig(self):
        """加载表格配置"""
        try:
            config_path = self._getConfigPath()
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                column_widths = config.get("column_widths", {})
                for column_index, width in column_widths.items():
                    if column_index.isdigit():
                        self.modTable.setColumnWidth(int(column_index), width)
                table_settings = config.get("table_settings", {})
                if "row_height" in table_settings:
                    self.modTable.verticalHeader().setDefaultSectionSize(150)
                    
        except Exception as e:
            pass
    
    def _ensureRowHeight(self):
        """确保所有行高度都设置为150像素"""
        try:
            self.modTable.verticalHeader().setDefaultSectionSize(150)
            for row in range(self.modTable.rowCount()):
                self.modTable.setRowHeight(row, 150)
                
        except Exception as e:
            pass
    
    def _saveTableConfig(self):
        """保存表格配置"""
        try:
            config_path = self._getConfigPath()
            os.makedirs(os.path.dirname(config_path), exist_ok=True)

            config = {
                "column_widths": {},
                "table_settings": {
                    "row_height": self.modTable.verticalHeader().defaultSectionSize()
                }
            }

            for i in range(self.modTable.columnCount()):
                config["column_widths"][str(i)] = self.modTable.columnWidth(i)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            pass
    
    def _onColumnResized(self, logical_index, old_size, new_size):
        """列宽改变时的回调"""
        self._saveTableConfig()
    
    def isEmpty(self) -> bool:
        """检查表格是否为空"""
        return self.modTable.rowCount() == 0
    
    def setEditMode(self, enabled: bool):
        """设置编辑模式"""
        self.is_edit_mode = enabled
        
        for row in range(self.modTable.rowCount()):
            for col in [1, 2, 3, 5]:
                item = self.modTable.item(row, col)
                if item:
                    if enabled:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    
    def _onItemDoubleClicked(self, item: QTableWidgetItem):
        """双击单元格事件处理"""
        if not self.is_edit_mode:
            return
        
        column = item.column()
        if column not in [1, 2, 3, 5]:
            return

        self.modTable.editItem(item)
    
    def refresh(self):
        """刷新表格数据"""
        try:
            cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
            record_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
            
            if not os.path.exists(record_file):
                self.modTable.setRowCount(0)
                return
            
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            current_row_count = self.modTable.rowCount()
            new_row_count = len(data)
            
            if current_row_count != new_row_count:
                self.loadData()
            else:
                for i, record in enumerate(data):
                    self._updateTableRowData(i, record)
                
                self._updateMenuTexts()
                self._updateTableHeight()
                self.modTable.viewport().update()
                
                # Deferred refresh to ensure that the layout is fully updated, maintaining a 150-pixel row height
                from PySide6.QtCore import QTimer
                QTimer.singleShot(100, lambda: (
                    self.modTable.viewport().update(),
                    self._loadTableConfig(),
                    self._ensureRowHeight()
                ))
                
        except Exception as e:
            self.loadData()
    
    def _updateTableRowData(self, row: int, record: dict):
        """更新表格行数据（不重建按钮）"""
        try:
            mod_info = record.get("mod_info", {})
            build_info = record.get("build_info", {})
            cover_block = record.get("cover_block", {})

            serial_item = self.modTable.item(row, 0)
            if serial_item:
                serial_item.setText(str(row + 1))
                serial_item.setData(Qt.ItemDataRole.UserRole, record)

            name_item = self.modTable.item(row, 1)
            if name_item:
                name_item.setText(mod_info.get("name", ""))
                name_item.setData(Qt.ItemDataRole.UserRole, record)

            author_item = self.modTable.item(row, 2)
            if author_item:
                author_item.setText(mod_info.get("author", ""))
                author_item.setData(Qt.ItemDataRole.UserRole, record)

            category_item = self.modTable.item(row, 3)
            if category_item:
                category_item.setText(mod_info.get("category", ""))
                category_item.setData(Qt.ItemDataRole.UserRole, record)

            cover_item = self.modTable.item(row, 4)
            if cover_item:
                cover_path = cover_block.get("image_path", "")
                if cover_path and os.path.exists(cover_path):
                    cover_item.setText(os.path.basename(cover_path))
                else:
                    cover_item.setText(lang.get_text("no_cover"))
                cover_item.setData(Qt.ItemDataRole.UserRole, record)
            
            version_item = self.modTable.item(row, 5)
            if version_item:
                version_item.setText(mod_info.get("version", ""))
                version_item.setData(Qt.ItemDataRole.UserRole, record)
            
            date_item = self.modTable.item(row, 6)
            if date_item:
                build_time = build_info.get("build_time", "")
                if build_time:
                    try:
                        dt = datetime.fromisoformat(build_time.replace('Z', '+00:00'))
                        formatted_date = dt.strftime("%Y-%m-%d %H:%M")
                        date_item.setText(formatted_date)
                    except:
                        date_item.setText(build_time)
                else:
                    date_item.setText("")
                date_item.setData(Qt.ItemDataRole.UserRole, record)
            
        except Exception as e:
            pass