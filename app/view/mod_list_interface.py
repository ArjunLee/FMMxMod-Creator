# coding:utf-8
"""
MOD List Interface
MOD列表界面模块
"""
import os
import json
import zipfile
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QActionGroup
from qfluentwidgets import (
    ScrollArea, BodyLabel, CommandBar, Action, TransparentDropDownPushButton,
    CheckableMenu, MenuIndicatorType, FluentIcon as FIF, InfoBar, InfoBarPosition
)
from ..common.language import lang
from ..common.config import cfg
from ..common.application import FMMApplication
from ..components.mod_table_widget import ModTableWidget
from ..components.edit_tips_dialog import EditTipsDialog

class ModListInterface(ScrollArea):
    """MOD列表界面"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.is_edit_mode = False                       # Edit mode status
        self.home_interface = None                      # Used to store the main interface reference
        self.edit_tips_shown = cfg.editTipsShown        # Has the edit prompt been displayed
        self._initUI()
        self._connectSignals()
        lang.languageChanged.connect(self._updateTexts)
    
    def _initUI(self):
        """初始化界面"""
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self._createCommandBar()
        self._createHintLabel()
        self.modTableWidget = ModTableWidget(self)
        self.modTableWidget.recordDeleted.connect(self._onRecordDeleted)
        self.modTableWidget.recordEdited.connect(self._onRecordEdited)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.vBoxLayout.addWidget(self.commandBar)
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.hintLabel)
        self.vBoxLayout.addWidget(self.modTableWidget)
        self.vBoxLayout.addStretch(1)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("modListInterface")

        self._checkBuildRecordFile()
        
        self.setStyleSheet("""
            ModListInterface {
                background-color: transparent;
                border: none;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QWidget {
                background-color: transparent;
            }
        """)
    
    def _createCommandBar(self):
        """创建操作通栏"""
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.importRecordAction = Action(FIF.ADD, lang.get_text("import_record"))
        self.backupRecordAction = Action(FIF.CLOUD, lang.get_text("backup_record"))
        self.editAction = Action(FIF.EDIT, lang.get_text("edit_mode"), checkable=True)
        self.refreshAction = Action(FIF.SYNC, lang.get_text("refresh"))
        self.sortAction = Action(FIF.SCROLL, lang.get_text("sort_mod"))
        self.commandBar.addAction(self.importRecordAction)
        self.commandBar.addAction(self.backupRecordAction)
        self.commandBar.addSeparator()
        self.editButton = self.commandBar.addAction(self.editAction)
        self.commandBar.addAction(self.refreshAction)
        self.commandBar.addSeparator()

        self.sortButton = TransparentDropDownPushButton(lang.get_text("sort_mod"), self, FIF.SCROLL)
        self.sortButton.setMenu(self._createSortMenu())
        font = self.sortButton.font()
        font.setPointSize(10)
        self.sortButton.setFont(font)
        self.commandBar.addWidget(self.sortButton)
        
        self._setCommandBarFontSize()
        self.commandBar.updateGeometry()
    
    def _createSortMenu(self):
        """创建排序菜单"""
        menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)
        
        self.sortByNameAction = Action(FIF.FONT, lang.get_text("sort_by_name"), checkable=True)
        self.sortByAuthorAction = Action(FIF.PEOPLE, lang.get_text("sort_by_author"), checkable=True)
        self.sortByCategoryAction = Action(FIF.TAG, lang.get_text("sort_by_category"), checkable=True)
        self.sortByDateAction = Action(FIF.CALENDAR, lang.get_text("sort_by_date"), checkable=True)
        self.sortConditionGroup = QActionGroup(self)
        self.sortConditionGroup.addAction(self.sortByNameAction)
        self.sortConditionGroup.addAction(self.sortByAuthorAction)
        self.sortConditionGroup.addAction(self.sortByCategoryAction)
        self.sortConditionGroup.addAction(self.sortByDateAction)
        self.ascendingAction = Action(FIF.UP, lang.get_text("sort_ascending"), checkable=True)
        self.descendingAction = Action(FIF.DOWN, lang.get_text("sort_descending"), checkable=True)
        self.sortDirectionGroup = QActionGroup(self)
        self.sortDirectionGroup.addAction(self.ascendingAction)
        self.sortDirectionGroup.addAction(self.descendingAction)
        self.sortByNameAction.setChecked(True)
        self.ascendingAction.setChecked(True)
        menu.addActions([
            self.sortByNameAction, self.sortByAuthorAction,
            self.sortByCategoryAction, self.sortByDateAction
        ])
        menu.addSeparator()
        menu.addActions([self.ascendingAction, self.descendingAction])
        self._setMenuFontSize(menu)
        
        return menu
    
    def _createHintLabel(self):
        """创建提示文字"""
        self.hintLabel = BodyLabel(lang.get_text("no_mod_hint"))
        self.hintLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        font = self.hintLabel.font()
        font.setPointSize(18)
        self.hintLabel.setFont(font)
    
    def _checkBuildRecordFile(self):
        """检查构建记录文件是否存在且有内容"""
        cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
        record_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
        
        has_records = False
        
        if os.path.exists(record_file):
            try:
                with open(record_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    has_records = isinstance(data, list) and len(data) > 0
            except (json.JSONDecodeError, IOError):
                has_records = False
        
        if has_records:
            self.hintLabel.hide()
            self.modTableWidget.show()
            self.modTableWidget.refresh()
        else:
            self.hintLabel.show()
            self.modTableWidget.hide()
    
    def _onRecordDeleted(self):
        """记录删除后的处理"""
        self._checkBuildRecordFile()
    
    def _onRecordEdited(self, record: dict):
        """记录编辑后的处理"""
        # TODO: 实现还原工作区功能
        mod_name = record.get("mod_info", {}).get("name", "")
        print(f"编辑记录: {mod_name}")
    

    def _connectSignals(self):
        """连接信号"""
        self.editAction.triggered.connect(self._onEditModeToggled)
        self.importRecordAction.triggered.connect(self._onImportRecordClicked)
        self.backupRecordAction.triggered.connect(self._onBackupRecordClicked)
        self.refreshAction.triggered.connect(self._onRefreshClicked)
        self.sortConditionGroup.triggered.connect(self._onSortConditionChanged)
        self.sortDirectionGroup.triggered.connect(self._onSortDirectionChanged)
    
    def _onEditModeToggled(self):
        """编辑模式切换"""
        self.is_edit_mode = self.editAction.isChecked()
        
        # If editing mode is turned on for the first time and no prompt is displayed, the edit prompt is displayed
        if self.is_edit_mode and not self.edit_tips_shown:
            self._showEditTips()
        
        # Set the editing mode of the table
        if hasattr(self, 'modTableWidget'):
            self.modTableWidget.setEditMode(self.is_edit_mode)
        
        print(f"编辑模式: {self.is_edit_mode}")
    
    def _showEditTips(self):
        """显示编辑提示对话框"""
        flyout = EditTipsDialog.show(
            target=self.editButton,
            parent=self
        )
        
        self.edit_tips_shown = True
        
        return flyout
    
    def _onBackupRecordClicked(self):
        """备份记录按钮点击"""
        try:
            # Get build log file path
            cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
            record_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
            
            # Check if the file exists
            if not os.path.exists(record_file):
                InfoBar.error(
                    title=lang.get_text("backup_record_failed_title"),
                    content=lang.get_text("import_failed"),
                    orient=Qt.Orientation.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
                return
            
            # Generate backup file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            backup_filename = f"FMMxMOD-Creator_build-record-{timestamp}.zip"
            
            # Get project root directory
            project_root = os.path.dirname(FMMApplication.getConfigPath())
            backup_path = os.path.join(project_root, backup_filename)
            
            # Create zip file
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(record_file, "FMMxMOD-Creator_build-record.json")
            
            InfoBar.success(
                title=lang.get_text("backup_record_success_title"),
                content=lang.get_text("backup_record_success_content").format(path=backup_path),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title=lang.get_text("backup_record_failed_title"),
                content=lang.get_text("backup_record_failed_content").format(error=str(e)),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
    
    def _onImportRecordClicked(self):
        """导入记录按钮点击"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                lang.get_text("import_record"),
                "",
                "ZIP files (*.zip)"
            )
            
            if not file_path:
                return
            
            # Get target file path
            cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
            target_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
            
            # Ensure cache directory exists
            os.makedirs(cache_dir, exist_ok=True)
            
            # Unzip zip file
            with zipfile.ZipFile(file_path, 'r') as zipf:
                # Check if zip file contains target file
                if "FMMxMOD-Creator_build-record.json" not in zipf.namelist():
                    InfoBar.error(
                        title=lang.get_text("import_failed_title"),
                        content=lang.get_text("import_failed"),
                        orient=Qt.Orientation.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                    return
                
                zipf.extract("FMMxMOD-Creator_build-record.json", cache_dir)
            
            self._checkBuildRecordFile()
            if self.modTableWidget.isVisible():
                self.modTableWidget.refresh()
            
            InfoBar.success(
                title=lang.get_text("import_success_title"),
                content=lang.get_text("import_success_content"),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
            
        except Exception as e:
            InfoBar.error(
                title=lang.get_text("import_failed_title"),
                content=lang.get_text("import_error").format(error=str(e)),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
    
    def _onRefreshClicked(self):
        """刷新按钮点击"""
        try:
            self._checkBuildRecordFile()
            
            if self.modTableWidget.isVisible():
                self.modTableWidget.refresh()
            
            InfoBar.success(
                title=lang.get_text("refresh"),
                content=lang.get_text("refresh_success"),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        except Exception as e:
            InfoBar.error(
                title=lang.get_text("error"),
                content=lang.get_text("refresh_failed").format(error=str(e)),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
    
    def _onSortConditionChanged(self, action):
        """排序条件改变"""
        self._applySorting()
    
    def _onSortDirectionChanged(self, action):
        """排序方向改变"""
        self._applySorting()
    
    def _applySorting(self):
        """应用排序"""
        try:
            sort_condition = None
            sort_direction = None
            
            if self.sortByNameAction.isChecked():
                sort_condition = "name"
            elif self.sortByAuthorAction.isChecked():
                sort_condition = "author"
            elif self.sortByCategoryAction.isChecked():
                sort_condition = "category"
            elif self.sortByDateAction.isChecked():
                sort_condition = "date"
            
            if self.ascendingAction.isChecked():
                sort_direction = "asc"
            elif self.descendingAction.isChecked():
                sort_direction = "desc"
            
            if sort_condition and sort_direction:
                self._sortTableData(sort_condition, sort_direction)
                
        except Exception as e:
            print(f"排序失败: {e}")
    
    def _sortTableData(self, condition: str, direction: str):
        """排序表格数据"""
        try:
            cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
            record_file = os.path.join(cache_dir, "FMMxMOD-Creator_build-record.json")
            
            if not os.path.exists(record_file):
                return
            
            with open(record_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                return
            
            def get_sort_key(record):
                if condition == "name":
                    return record.get("mod_info", {}).get("name", "").lower()
                elif condition == "author":
                    return record.get("mod_info", {}).get("author", "").lower()
                elif condition == "category":
                    return record.get("mod_info", {}).get("category", "").lower()
                elif condition == "date":
                    build_time = record.get("build_info", {}).get("build_time", "")
                    if build_time:
                        try:
                            from datetime import datetime
                            return datetime.fromisoformat(build_time.replace('Z', '+00:00'))
                        except:
                            return datetime.min
                    return datetime.min
                return ""
            
            reverse = (direction == "desc")
            sorted_data = sorted(data, key=get_sort_key, reverse=reverse)
            
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_data, f, ensure_ascii=False, indent=2)
            
            if self.modTableWidget.isVisible():
                self.modTableWidget.refresh()
            
        except Exception as e:
            print(f"排序数据失败: {e}")
    
    def _updateTexts(self):
        """更新界面文本"""
        self.importRecordAction.setText(lang.get_text("import_record"))
        self.backupRecordAction.setText(lang.get_text("backup_record"))
        self.editAction.setText(lang.get_text("edit_mode"))
        self.refreshAction.setText(lang.get_text("refresh"))
        self.sortButton.setText(lang.get_text("sort_mod"))
        self.sortByNameAction.setText(lang.get_text("sort_by_name"))
        self.sortByAuthorAction.setText(lang.get_text("sort_by_author"))
        self.sortByCategoryAction.setText(lang.get_text("sort_by_category"))
        self.sortByDateAction.setText(lang.get_text("sort_by_date"))
        self.ascendingAction.setText(lang.get_text("sort_ascending"))
        self.descendingAction.setText(lang.get_text("sort_descending"))
        self.hintLabel.setText(lang.get_text("no_mod_hint"))
        self._updateCommandBarLayout()
    
    def _setCommandBarFontSize(self):
        """设置CommandBar所有按钮的字体大小"""
        try:
            for action in [self.importRecordAction, self.backupRecordAction, 
                          self.editAction, self.refreshAction]:
                widget = self.commandBar.widgetForAction(action)
                if widget:
                    font = widget.font()
                    font.setPointSize(10)
                    widget.setFont(font)
        except Exception as e:
            pass
    
    def _setMenuFontSize(self, menu):
        """设置菜单字体大小"""
        try:
            font = menu.font()
            font.setPointSize(10)
            menu.setFont(font)

            for action in menu.actions():
                if hasattr(action, 'setFont'):
                    action_font = action.font()
                    action_font.setPointSize(10)
                    action.setFont(action_font)
        except Exception as e:
            pass
    
    def _updateCommandBarLayout(self):
        """更新CommandBar布局以适应文本宽度变化"""
        for button in self.commandBar.commandButtons:
            button.adjustSize()
            button.updateGeometry()
        
        self.sortButton.adjustSize()
        self.sortButton.updateGeometry()
        self.commandBar.adjustSize()
        self.commandBar.updateGeometry()

        if hasattr(self.commandBar, 'resizeToSuitableWidth'):
            self.commandBar.resizeToSuitableWidth()
        
        self.commandBar.update()
        if self.commandBar.parent():
            self.commandBar.parent().updateGeometry()