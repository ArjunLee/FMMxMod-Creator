# coding:utf-8
"""
Build Service
构建服务模块
"""
import os
import shutil
import tempfile
import zipfile
import rarfile
import py7zr
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from PySide6.QtCore import QObject, Signal, QThread
from qfluentwidgets import InfoBar, InfoBarIcon
from ..common.language import lang
from ..common import version_info
from ..common.config import cfg
from ..common.application import FMMApplication
from .build_record_service import BuildRecordService

class BuildWorker(QThread):
    """构建工作线程"""
    # signal definition
    progressChanged = Signal(int)  # Progress change signal
    statusChanged = Signal(str)    # state change signal
    buildCompleted = Signal(str)   # build completion signal
    buildFailed = Signal(str)      # Build failure signal
    
    def __init__(self, build_data: Dict, parent=None):
        super().__init__(parent)
        self.build_data = build_data
        self.temp_dir = None
        self.output_path = None
    
    def run(self):
        """执行构建任务"""
        try:
            # Step 1: Create a temporary directory
            self.statusChanged.emit(lang.get_text("creating_temp_dir"))
            self.progressChanged.emit(10)
            self._create_temp_directory()
            
            # Step 2: Create a cover folder
            self.statusChanged.emit(lang.get_text("creating_cover_folder"))
            self.progressChanged.emit(20)
            self._create_cover_folder()
            
            # Step 3: Create other block folders
            self.statusChanged.emit(lang.get_text("creating_block_folders"))
            self.progressChanged.emit(40)
            self._create_block_folders()
            
            # Step 4: Create an archive file
            self.statusChanged.emit(lang.get_text("creating_archive_file"))
            self.progressChanged.emit(70)
            self._create_archive_file()
            
            # Step 5: Move to the output directory
            self.statusChanged.emit(lang.get_text("moving_to_output"))
            self.progressChanged.emit(90)
            self._move_to_output()
            
            # Step 6: Build completion
            self.statusChanged.emit(lang.get_text("build_completed"))
            self.progressChanged.emit(100)
            self.buildCompleted.emit(self.output_path)
            
        except Exception as e:
            error_msg = str(e)
            self.buildFailed.emit(error_msg)
    
    def _create_temp_directory(self):
        """创建临时目录"""
        mod_name = self.build_data["mod_info"]["name"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        folder_name = f"{mod_name}-{timestamp}"
        
        from ..common.config import cfg
        cache_dir = cfg.cacheDirectory
        os.makedirs(cache_dir, exist_ok=True)

        self.temp_dir = os.path.join(cache_dir, folder_name)
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def _create_cover_folder(self):
        """创建封面文件夹"""
        cover_data = self.build_data["cover_data"]
        if not cover_data:
            raise Exception(lang.get_text("cover_data_missing"))
        
        # Create the 00-cover folder
        cover_folder = os.path.join(self.temp_dir, "00-cover")
        os.makedirs(cover_folder, exist_ok=True)
        
        # Copy the cover image
        if cover_data["image_path"]:
            image_path = cover_data["image_path"]
            if os.path.exists(image_path):
                # Get file extension
                _, ext = os.path.splitext(image_path)
                cover_image_name = f"cover{ext}"
                cover_image_path = os.path.join(cover_folder, cover_image_name)
                shutil.copy2(image_path, cover_image_path)
            else:
                raise Exception(f"{lang.get_text('cover_image_not_found')}: {image_path}")
        
        # Create `modinfo.ini` file
        self._create_modinfo_file(
            folder_path=cover_folder,
            name="00 --------------Cover--------------",
            description=cover_data["description"],
            screenshot=cover_image_name if cover_data["image_path"] else ""
        )
    
    def _create_block_folders(self):
        """创建其他区块文件夹"""
        # Get the user-sorted block data
        sorted_blocks = self.build_data["sorted_blocks"]
        
        for index, block_data in enumerate(sorted_blocks, start=1):
            block_type = block_data["type"]
            
            if block_type == "warning":
                self._create_warning_folder(block_data, index)
            elif block_type == "separator":
                self._create_separator_folder(block_data, index)
            elif block_type == "mod_file":
                self._create_mod_file_folder(block_data, index)
    
    def _create_warning_folder(self, warning_data: Dict, index: int):
        """创建警告文件夹"""
        # Folder name: Serial number -warning
        folder_name = f"{index:02d}-warning"
        folder_path = os.path.join(self.temp_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Copy warning image (if available)
        screenshot_name = ""
        if warning_data.get("image_path") and os.path.exists(warning_data["image_path"]):
            image_path = warning_data["image_path"]
            _, ext = os.path.splitext(image_path)
            screenshot_name = f"warning{ext}"
            warning_image_path = os.path.join(folder_path, screenshot_name)
            shutil.copy2(image_path, warning_image_path)
        
        # Create `modinfo.ini` file
        name = f"{index:02d} --------------Warning--------------"
        self._create_modinfo_file(
            folder_path=folder_path,
            name=name,
            description=warning_data.get("description", ""),
            screenshot=screenshot_name
        )
    
    def _create_separator_folder(self, separator_data: Dict, index: int):
        """创建分割线文件夹"""
        separator_name = separator_data.get("separator_name", "separator").strip()
        
        # If the separator name is empty, use "separator"
        if not separator_name:
            separator_name = "separator"
        
        # Folder name: Serial number -separator- Separator name
        folder_name = f"{index:02d}-separator-{separator_name}"
        folder_path = os.path.join(self.temp_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Create `modinfo.ini` file
        name = f"{index:02d} ----------------Separator {separator_name}----------------"
        self._create_modinfo_file(
            folder_path=folder_path,
            name=name,
            description="This is a separator.",
            screenshot=""
        )
    
    def _create_mod_file_folder(self, mod_file_data: Dict, index: int):
        """创建MOD文件文件夹"""
        # Get module name
        module_name = mod_file_data.get("module_name", "module").strip()
        
        # If the module name is empty, use "module"
        if not module_name:
            module_name = "module"
        
        # Folder name: Serial number -module name
        folder_name = f"{index:02d}-{module_name}"
        folder_path = os.path.join(self.temp_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Copy screenshot (if available)
        screenshot_name = ""
        if mod_file_data.get("image_path") and os.path.exists(mod_file_data["image_path"]):
            image_path = mod_file_data["image_path"]
            _, ext = os.path.splitext(image_path)
            screenshot_name = f"screenshot{ext}"
            screenshot_path = os.path.join(folder_path, screenshot_name)
            shutil.copy2(image_path, screenshot_path)
        
        # Copy files and folders
        files_data = mod_file_data.get("files", [])
        for file_data in files_data:
            # Handling tuple formats (path, name)
            if isinstance(file_data, tuple) and len(file_data) >= 2:
                source_path, file_name = file_data[0], file_data[1]
            elif isinstance(file_data, dict):
                source_path = file_data["path"]
                file_name = file_data["name"]
            else:
                continue
            
            if os.path.exists(source_path):
                if os.path.isfile(source_path):
                    # Copy file
                    dest_path = os.path.join(folder_path, file_name)
                    shutil.copy2(source_path, dest_path)
                elif os.path.isdir(source_path):
                    # Copy folder
                    dest_path = os.path.join(folder_path, file_name)
                    shutil.copytree(source_path, dest_path)
        
        # Create `modinfo.ini` file
        name = f"{index:02d} {module_name}"
        self._create_modinfo_file(
            folder_path=folder_path,
            name=name,
            description=mod_file_data.get("description", ""),
            screenshot=screenshot_name
        )
    
    def _create_modinfo_file(self, folder_path: str, name: str, description: str, screenshot: str):
        """创建modinfo.ini文件"""
        mod_info = self.build_data["mod_info"]
        
        # Format version number digits
        version = self._format_version(mod_info["version"])
        
        # Create ini content
        ini_content = f"""
        name={name}
        version=v{version}
        description={description}
        category={mod_info["category"]}
        screenshot={screenshot}
        author={mod_info["author"]}
        NameAsBundle={mod_info["name"]}
        """
        
        # Write file
        ini_path = os.path.join(folder_path, "modinfo.ini")
        with open(ini_path, 'w', encoding='utf-8') as f:
            f.write(ini_content)
    
    def _format_version(self, version: str) -> str:
        """格式化版本号"""
        if not version:
            return version_info.VERSION_STRING
        
        # Remove prefix characters (such as v, V, etc.)
        formatted = version.strip()
        while formatted and not formatted[0].isdigit():
            formatted = formatted[1:]
        
        # Remove spaces
        formatted = formatted.replace(" ", "")
        
        # Only keep allowed characters: digits, points, hyphens, underscores, and letters
        allowed_chars = "0123456789.-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        formatted = ''.join(c for c in formatted if c in allowed_chars)
        
        return formatted if formatted else version_info.VERSION_STRING
    
    def _create_archive_file(self):
        """根据配置的打包格式创建压缩文件"""
        # Get configuration pack format
        build_type = cfg.buildType.lower()
        
        # Compression file name and temporary folder name same
        folder_name = os.path.basename(self.temp_dir)
        
        # Get .cache directory path
        cache_dir = os.path.dirname(self.temp_dir)
        
        if build_type == "zip":
            archive_name = f"{folder_name}.zip"
            archive_path = os.path.join(cache_dir, archive_name)
            self._create_zip(archive_path)
        elif build_type == "rar":
            archive_name = f"{folder_name}.rar"
            archive_path = os.path.join(cache_dir, archive_name)
            self._create_rar(archive_path)
        elif build_type == "7z":
            archive_name = f"{folder_name}.7z"
            archive_path = os.path.join(cache_dir, archive_name)
            self._create_7z(archive_path)
        else:
            archive_name = f"{folder_name}.zip"
            archive_path = os.path.join(cache_dir, archive_name)
            self._create_zip(archive_path)
        
        self.archive_path = archive_path
    
    def _create_zip(self, archive_path: str):
        """创建ZIP文件"""
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    zipf.write(file_path, arcname)
    
    def _create_rar(self, archive_path: str):
        """创建RAR文件"""
        # Because the rarfile library can only read rar files, not create them.  
        # Here, we're actually creating a zip file and then changing the extension to rar.
        zip_path = archive_path.replace('.rar', '.zip')
        self._create_zip(zip_path)
        # Rename to rar extension (still zip format)
        if os.path.exists(zip_path):
            shutil.move(zip_path, archive_path)
    
    def _create_7z(self, archive_path: str):
        """创建7Z文件"""
        with py7zr.SevenZipFile(archive_path, 'w') as archive:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    archive.write(file_path, arcname)
    
    def _move_to_output(self):
        """移动到输出目录"""
        build_dir = cfg.buildDirectory
        if not build_dir or not build_dir.strip():
            build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "output")
            build_dir = os.path.normpath(build_dir)
        
        os.makedirs(build_dir, exist_ok=True)
        archive_name = os.path.basename(self.archive_path)
        self.output_path = os.path.join(build_dir, archive_name)
        
        if os.path.exists(self.output_path):
            os.remove(self.output_path)
        
        shutil.move(self.archive_path, self.output_path)
    
    def _cleanup_temp_directory(self):
        """清理临时目录（已禁用，保留.cache中的缓存文件）"""
        pass


class BuildService(QObject):
    """构建服务"""
    
    buildStarted = Signal()        # Build start signal
    progressChanged = Signal(int)  # Progress change signal
    statusChanged = Signal(str)    # state change signal
    buildCompleted = Signal(str)   # build completion signal
    buildFailed = Signal(str)      # build failure signal
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
    
    def validate_build_data(self, mod_info: Dict, cover_data: Optional[Dict], 
                          sorted_blocks: List[Dict]) -> Tuple[bool, str]:
        """验证构建数据"""
        error_msg = self._validate_build_data(mod_info, cover_data, sorted_blocks)
        if error_msg:
            return False, error_msg
        
        return True, ""
    
    def start_build(self, mod_info: Dict, cover_data: Optional[Dict], sorted_blocks: List[Dict]):
        """开始构建"""
        is_valid, error_msg = self.validate_build_data(mod_info, cover_data, sorted_blocks)
        if not is_valid:
            self.buildFailed.emit(error_msg)
            return
        
        build_data = {
            "mod_info": mod_info,
            "cover_data": cover_data,
            "sorted_blocks": sorted_blocks
        }
        
        self.worker = BuildWorker(build_data, self)
        self.worker.progressChanged.connect(self.progressChanged.emit)
        self.worker.statusChanged.connect(self.statusChanged.emit)
        self.worker.buildCompleted.connect(self._on_build_completed)
        self.worker.buildFailed.connect(self._on_build_failed)
        self.buildStarted.emit()
        self.worker.start()
    
    def _on_build_completed(self, output_path: str):
        """构建完成处理"""
        # Generate build record profile
        try:
            record_service = BuildRecordService()
            record_service.generate_build_record(
                self.worker.build_data,
                output_path,
                self.worker.temp_dir
            )
        except Exception as e:
            # Record generation failure does not affect build completion
            pass
        
        self.buildCompleted.emit(output_path)
        self._cleanup_worker()
    
    def _on_build_failed(self, error_msg: str):
        """构建失败处理"""
        self.buildFailed.emit(error_msg)
        self._cleanup_worker()
    
    def _cleanup_worker(self):
        """清理工作线程"""
        if self.worker:
            self.worker.quit()
            self.worker.wait()
            self.worker.deleteLater()
            self.worker = None
    
    def _validate_build_data(self, mod_info: Dict, cover_data: Optional[Dict], 
                           sorted_blocks: List[Dict]) -> Optional[str]:
        """验证构建数据，返回错误信息或None"""
        if not mod_info.get("name", "").strip():
            return lang.get_text("mod_name_required")
        
        if not mod_info.get("version", "").strip():
            return lang.get_text("version_required")
        
        if not mod_info.get("author", "").strip():
            return lang.get_text("author_required")
        
        # Note: The MOD category is a non-essential input item and is allowed to be empty
        
        if not cover_data:
            return lang.get_text("cover_block_required")
        
        if cover_data.get("image_path") and not os.path.exists(cover_data["image_path"]):
            return lang.get_text("cover_image_not_found")
        
        for block in sorted_blocks:
            if block.get("type") == "mod_file":
                files = block.get("files", [])
                for file_info in files:
                    if isinstance(file_info, tuple) and len(file_info) >= 2:
                        file_path, file_name = file_info[0], file_info[1]
                        if not os.path.exists(file_path):
                            return f"{lang.get_text('file_not_found')}: {file_name}"
                    elif isinstance(file_info, dict):
                        if not os.path.exists(file_info.get("path", "")):
                            return f"{lang.get_text('file_not_found')}: {file_info.get('name', '未知文件')}"
        
        if not sorted_blocks:
            return lang.get_text("content_block_required")
        
        return None