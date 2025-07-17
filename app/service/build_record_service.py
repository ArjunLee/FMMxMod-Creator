# -*- coding: utf-8 -*-
"""
构建记录服务
用于在构建成功后生成配置文件，记录本次工作的所有信息
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

class BuildRecordService:
    """构建记录服务类"""
    def __init__(self):
        self.cache_dir = None
        
    def generate_build_record(self, build_data: Dict, output_path: str, temp_dir: str) -> str:
        """
        生成构建记录配置文件
        
        Args:
            build_data: 构建数据
            output_path: 输出文件路径
            temp_dir: 临时目录路径
            
        Returns:
            str: 生成的配置文件路径
        """
        from ..common.application import FMMApplication
        self.cache_dir = os.path.join(os.path.dirname(FMMApplication.getConfigPath()), ".cache")
 
        os.makedirs(self.cache_dir, exist_ok=True)                                      # Make sure the record directory exists
        record_data = self._create_record_data(build_data, output_path, temp_dir)       # Generate recorded data
        config_filename = "FMMxMOD-Creator_build-record.json"
        config_path = os.path.join(self.cache_dir, config_filename)

        self._append_record_data(config_path, record_data)                              # Append data to configuration file
            
        return config_path
    
    def _create_record_data(self, build_data: Dict, output_path: str, temp_dir: str) -> Dict:
        """
        创建记录数据
        
        Args:
            build_data: 构建数据
            output_path: 输出文件路径
            temp_dir: 临时目录路径
            
        Returns:
            Dict: 记录数据
        """
        mod_info = build_data["mod_info"]
        cover_data = build_data["cover_data"]
        sorted_blocks = build_data["sorted_blocks"]

        record_data = {
            "build_info": {
                "build_time": datetime.now().isoformat(),
                "output_path": output_path,
                "temp_dir": temp_dir,
                "cache_dir": self.cache_dir
            },
            "mod_info": {
                "name": mod_info.get("name", ""),
                "version": mod_info.get("version", ""),
                "author": mod_info.get("author", ""),
                "category": mod_info.get("category", "")
            },
            "cover_block": self._process_cover_data(cover_data),
            "content_blocks": self._process_content_blocks(sorted_blocks),
            "block_order": self._get_block_order(cover_data, sorted_blocks)
        }
        
        return record_data
    
    def _process_cover_data(self, cover_data: Optional[Dict]) -> Dict:
        """
        处理封面数据
        
        Args:
            cover_data: 封面数据
            
        Returns:
            Dict: 处理后的封面数据
        """
        if not cover_data:
            return {}
            
        return {
            "image_path": cover_data.get("image_path", ""),
            "description": cover_data.get("description", ""),
            "cover_tag": cover_data.get("cover_tag", ""),
            "type": "cover"
        }
    
    def _process_content_blocks(self, sorted_blocks: List[Dict]) -> List[Dict]:
        """
        处理内容区块数据
        
        Args:
            sorted_blocks: 排序后的区块列表
            
        Returns:
            List[Dict]: 处理后的区块数据列表
        """
        processed_blocks = []
        
        for block in sorted_blocks:
            block_type = block.get("type", "")
            
            if block_type == "warning":
                processed_block = self._process_warning_block(block)
            elif block_type == "separator":
                processed_block = self._process_separator_block(block)
            elif block_type == "mod_file":
                processed_block = self._process_mod_file_block(block)
            else:
                processed_block = block.copy()
                
            processed_blocks.append(processed_block)
            
        return processed_blocks
    
    def _process_warning_block(self, block: Dict) -> Dict:
        """
        处理警告区块数据
        
        Args:
            block: 警告区块数据
            
        Returns:
            Dict: 处理后的警告区块数据
        """
        return {
            "type": "warning",
            "block_tag": block.get("block_tag", ""),
            "image_path": block.get("image_path", ""),
            "description": block.get("description", "")
        }
    
    def _process_separator_block(self, block: Dict) -> Dict:
        """
        处理分割线区块数据
        
        Args:
            block: 分割线区块数据
            
        Returns:
            Dict: 处理后的分割线区块数据
        """
        return {
            "type": "separator",
            "separator_name": block.get("separator_name", "")
        }
    
    def _process_mod_file_block(self, block: Dict) -> Dict:
        """
        处理文件区块数据
        
        Args:
            block: 文件区块数据
            
        Returns:
            Dict: 处理后的文件区块数据
        """
        files_info = []
        files = block.get("files", [])
        
        for file_info in files:
            if isinstance(file_info, tuple) and len(file_info) >= 2:
                files_info.append({
                    "file_path": file_info[0],
                    "file_name": file_info[1]
                })
            elif isinstance(file_info, dict):
                files_info.append({
                    "file_path": file_info.get("path", ""),
                    "file_name": file_info.get("name", "")
                })
        
        folder_path = block.get("folder_path", "")
        
        return {
            "type": "mod_file",
            "area_mark": block.get("area_mark", ""),
            "module_name": block.get("module_name", ""),
            "image_path": block.get("image_path", ""),
            "description": block.get("description", ""),
            "files": files_info,
            "folder_path": folder_path
        }
    
    def _get_block_order(self, cover_data: Optional[Dict], sorted_blocks: List[Dict]) -> List[str]:
        """
        获取区块排序信息
        
        Args:
            cover_data: 封面数据
            sorted_blocks: 排序后的区块列表
            
        Returns:
            List[str]: 区块ID的排序列表
        """
        order = []
        
        if cover_data:
            cover_tag = cover_data.get("cover_tag", "")
            if cover_tag:
                order.append(f"cover_{cover_tag}")
            else:
                order.append("cover")
        
        for index, block in enumerate(sorted_blocks):
            block_type = block.get("type", "")
            if block_type == "separator":
                separator_name = block.get("separator_name", "")
                if separator_name:
                    order.append(f"separator_{separator_name}")
                else:
                    order.append(f"separator_{index + 1}")
            elif block_type == "warning":
                block_tag = block.get("block_tag", "")
                if block_tag:
                    order.append(f"warning_{block_tag}")
                else:
                    order.append(f"warning_{index + 1}")
            elif block_type == "mod_file":
                module_name = block.get("module_name", "")
                area_mark = block.get("area_mark", "")
                if area_mark:
                    order.append(f"mod_file_{area_mark}")
                elif module_name:
                    order.append(f"mod_file_{module_name}")
                else:
                    order.append(f"mod_file_{index + 1}")
            else:
                order.append(f"{block_type}_{index + 1}")
        
        return order
    
    def _append_record_data(self, config_path: str, record_data: Dict) -> None:
        """
        追加记录数据到配置文件
        
        Args:
            config_path: 配置文件路径
            record_data: 要追加的记录数据
        """
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
                
                existing_data.append(record_data)
                
            except (json.JSONDecodeError, IOError):
                existing_data = [record_data]
        else:
            existing_data = [record_data]
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)