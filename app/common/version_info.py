# coding:utf-8
"""
Version Information
版本信息文件 - 用于Nuitka打包时设置exe属性
"""

# 版本号组件（规则）
MAJOR_VERSION = 1  # 主版本号：重大功能更新或不兼容变更
MINOR_VERSION = 3  # 次版本号：新功能添加，向后兼容
PATCH_VERSION = 3  # 修订版本号：bug修复和小改进

# 版本字符串
VERSION_STRING = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}"
# 填补Windows版本号，添加第四位为0
FULL_VERSION_STRING = f"{MAJOR_VERSION}.{MINOR_VERSION}.{PATCH_VERSION}.0"

# 应用程序版本信息
VERSION_INFO = {
    "file_version": FULL_VERSION_STRING,                                     # Windows版本号 | 4位数字
    "product_version": VERSION_STRING,                                       # 产品版本 | 3位数字
    "file_description": "FMM x Mod Creator - Game MOD Creation Tool",
    "product_name": "FMM x Mod Creator",
    "company_name": "Arjun520",
    "copyright": "Copyright © 2025 Arjun520. All rights reserved.",
    "internal_name": "FMMxModCreator",
    "original_filename": "FMM x Mod Creator.exe",
    "language": "0x0409",
    "codepage": "1200",
    "legal_copyright": "Copyright © 2025 Arjun520. All rights reserved.",
    "legal_trademarks": "FMM x Mod Creator™",
    "private_build": "",
    "special_build": "",
    "comments": "Modern desktop application designed for game MOD creators"
}

# 应用程序信息
APP_NAME = "FMM x Mod Creator"
APP_DESCRIPTION = "Modern desktop application designed for game MOD creators"
APP_AUTHOR = "Arjun520"
APP_LICENSE = "MIT License"
APP_URL = "https://github.com/ArjunLee/FMMxMod-Creator"