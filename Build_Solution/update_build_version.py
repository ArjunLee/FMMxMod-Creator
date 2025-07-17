#!/usr/bin/env python3
# coding:utf-8
"""
更新构建脚本中的版本信息
自动从version_info.py读取版本信息并更新build.bat
"""

import re
import sys
from pathlib import Path

# 添加父目录到Python路径以导入version_info
sys.path.insert(0, str(Path(__file__).parent.parent))
from version_info import VERSION_INFO, VERSION_STRING, FULL_VERSION_STRING

def update_build_bat():
    """更新build.bat中的版本信息"""
    build_bat_path = Path("../build.bat")
    
    if not build_bat_path.exists():
        print("错误：找不到build.bat文件")
        return False
    
    # 读取build.bat内容
    with open(build_bat_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新版本信息
    # 更新文件版本
    content = re.sub(
        r'--windows-file-version=[\d\.]+',
        f'--windows-file-version={FULL_VERSION_STRING}',
        content
    )
    
    # 更新产品版本
    content = re.sub(
        r'--windows-product-version=[\d\.]+',
        f'--windows-product-version={VERSION_STRING}',
        content
    )
    
    # 更新公司名称
    content = re.sub(
        r'--windows-company-name="[^"]*"',
        f'--windows-company-name="{VERSION_INFO["company_name"]}"',
        content
    )
    
    # 更新文件描述
    content = re.sub(
        r'--windows-file-description="[^"]*"',
        f'--windows-file-description="{VERSION_INFO["file_description"]}"',
        content
    )
    
    # 更新产品名称
    content = re.sub(
        r'--windows-product-name="[^"]*"',
        f'--windows-product-name="{VERSION_INFO["product_name"]}"',
        content
    )
    
    # 写回文件
    with open(build_bat_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已更新build.bat版本信息:")
    print(f"   文件版本: {FULL_VERSION_STRING}")
    print(f"   产品版本: {VERSION_STRING}")
    print(f"   公司名称: {VERSION_INFO['company_name']}")
    print(f"   文件描述: {VERSION_INFO['file_description']}")
    print(f"   产品名称: {VERSION_INFO['product_name']}")
    return True

if __name__ == "__main__":
    update_build_bat()