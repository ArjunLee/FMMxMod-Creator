#!/usr/bin/env python3
# coding:utf-8
"""
Nuitka Build Script
优化的Nuitka打包脚本 - 支持单文件EXE和配置文件管理
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# 添加app目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

try:
    from app.common import version_info
except ImportError:
    print("错误: 无法导入版本信息模块")
    sys.exit(1)


class NuitkaBuildConfig:
    """Nuitka构建配置管理"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.app_dir = self.project_root / "app"
        self.config_dir = self.app_dir / "config"
        self.resources_dir = self.app_dir / "Resources"
        
        # 输出文件配置
        self.output_filename = "FMM x Mod Creator.exe"
        self.main_script = self.project_root / "main.py"
        
        # 版本信息
        self.version_info = self._get_version_info()
    
    def _get_version_info(self) -> Dict[str, str]:
        """获取版本信息"""
        return {
            "file_version": version_info.FULL_VERSION_STRING,
            "product_version": version_info.VERSION_STRING,
            "file_description": version_info.VERSION_INFO["file_description"],
            "product_name": version_info.VERSION_INFO["product_name"],
            "company_name": version_info.VERSION_INFO["company_name"],
            "copyright": version_info.VERSION_INFO["copyright"]
        }
    
    def get_nuitka_args(self) -> List[str]:
        """构建Nuitka命令行参数"""
        args = [
            "python",
            "-m",
            "nuitka",
            # 基本配置
            "--onefile",  # 单文件模式
            "--enable-plugin=pyside6",
            f"--output-dir={self.dist_dir}",
            f"--output-filename={self.output_filename}",
            
            # Windows特定配置
            "--windows-console-mode=disable",
            f"--windows-icon-from-ico={self.resources_dir / 'FMMxModCreator_Icon.ico'}",
            
            # 版本信息
            f"--windows-file-version={self.version_info['file_version']}",
            f"--windows-product-version={self.version_info['product_version']}",
            f"--windows-file-description={self.version_info['file_description']}",
            f"--windows-product-name={self.version_info['product_name']}",
            f"--windows-company-name={self.version_info['company_name']}",
            f"--copyright={self.version_info['copyright']}",
            
            # 数据文件包含
            f"--include-data-dir={self.resources_dir}=Resources",
            f"--include-data-file={self.app_dir / 'common' / 'version_info.py'}=app/common/version_info.py",
            
            # 优化选项
            "--assume-yes-for-downloads",
            "--show-progress",
            "--show-memory",
            "--remove-output",
            
            # 排除不需要的模块
            "--nofollow-import-to=tkinter",
            "--nofollow-import-to=matplotlib",
            "--nofollow-import-to=numpy",
            
            # 主脚本
            str(self.main_script)
        ]
        
        return args


class NuitkaBuilder:
    """Nuitka构建器"""
    
    def __init__(self):
        self.config = NuitkaBuildConfig()
        self.project_root = self.config.project_root
        self.dist_dir = self.config.dist_dir
    
    def clean_previous_build(self):
        """清理之前的构建"""
        print("🧹 清理之前的构建...")
        
        if self.dist_dir.exists():
            # 删除旧的exe文件
            old_exe = self.dist_dir / self.config.output_filename
            if old_exe.exists():
                old_exe.unlink()
                print(f"   删除旧文件: {old_exe.name}")
            
            # 删除旧的dist目录（如果存在）
            old_dist = self.dist_dir / "FMM_Creator_App.dist"
            if old_dist.exists():
                shutil.rmtree(old_dist)
                print(f"   删除旧目录: {old_dist.name}")
        else:
            self.dist_dir.mkdir(exist_ok=True)
        
        print("✅ 清理完成")
    
    def update_version(self):
        """更新版本信息"""
        print("📝 检查版本信息...")
        
        # 直接从version_info模块获取版本信息，无需外部脚本
        version_info = self.config.version_info
        print(f"   当前版本: {version_info['product_version']} (文件: {version_info['file_version']})")
        print(f"   产品名称: {version_info['product_name']}")
        print(f"   公司名称: {version_info['company_name']}")
        print("✅ 版本信息检查完成")
    
    def build_with_nuitka(self) -> bool:
        """使用Nuitka构建"""
        print("🔨 开始Nuitka构建...")
        print(f"   版本: {self.config.version_info['product_version']} (文件: {self.config.version_info['file_version']})")
        print(f"   输出: {self.config.output_filename}")
        print()
        
        # 构建Nuitka命令
        nuitka_args = self.config.get_nuitka_args()
        
        try:
            # 执行Nuitka构建
            result = subprocess.run(
                nuitka_args,
                cwd=self.project_root,
                check=True
            )
            
            print("✅ Nuitka构建成功!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Nuitka构建失败: {e}")
            print(f"   错误代码: {e.returncode}")
            return False
        except FileNotFoundError:
            print("❌ 错误: 找不到nuitka命令")
            print("   请确保已安装nuitka: pip install nuitka")
            return False
    
    def setup_distribution_structure(self):
        """设置分发目录结构"""
        print("📁 设置分发目录结构...")
        
        # 创建app目录结构
        app_dist_dir = self.dist_dir / "app"
        config_dist_dir = app_dist_dir / "config"
        cache_dist_dir = app_dist_dir / ".cache"
        
        # 创建目录
        config_dist_dir.mkdir(parents=True, exist_ok=True)
        cache_dist_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制配置文件
        if self.config.config_dir.exists():
            for config_file in self.config.config_dir.glob("*"):
                if config_file.is_file():
                    shutil.copy2(config_file, config_dist_dir)
                    print(f"   复制配置: {config_file.name}")
        
        # 复制说明文档
        readme_src = Path(__file__).parent / "DIST_README.md"
        readme_dst = self.dist_dir / "README.md"
        if readme_src.exists():
            shutil.copy2(readme_src, readme_dst)
            print(f"   复制文档: README.md")
        
        print("✅ 分发结构设置完成")
        print()
        print("📦 单文件分发结构:")
        print("   dist/")
        print(f"   ├── {self.config.output_filename}  (单文件可执行程序)")
        print("   ├── app/")
        print("   │   ├── config/            (配置文件)")
        print("   │   └── .cache/            (缓存目录)")
        print("   └── README.md             (说明文档)")
        print()
        print("   资源文件已嵌入到可执行文件中")
    
    def open_dist_folder(self):
        """打开分发文件夹"""
        if sys.platform == "win32":
            try:
                subprocess.run(["explorer", str(self.dist_dir)], check=True)
                print(f"📂 已打开分发文件夹: {self.dist_dir}")
            except subprocess.CalledProcessError:
                print(f"⚠️  无法打开文件夹: {self.dist_dir}")
    
    def build(self) -> bool:
        """执行完整构建流程"""
        print("🚀 开始FMM x Mod Creator构建流程")
        print("=" * 50)
        print()
        
        try:
            # 1. 清理之前的构建
            self.clean_previous_build()
            print()
            
            # 2. 更新版本信息
            self.update_version()
            print()
            
            # 3. 使用Nuitka构建
            if not self.build_with_nuitka():
                return False
            print()
            
            # 4. 设置分发目录结构
            self.setup_distribution_structure()
            print()
            
            # 5. 打开分发文件夹
            self.open_dist_folder()
            
            print("🎉 构建完成!")
            print(f"   可执行文件: {self.dist_dir / self.config.output_filename}")
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  构建被用户中断")
            return False
        except Exception as e:
            print(f"❌ 构建过程中发生错误: {e}")
            return False


def main():
    """主函数"""
    builder = NuitkaBuilder()
    
    # 检查必要文件
    if not builder.config.main_script.exists():
        print(f"❌ 错误: 找不到主脚本 {builder.config.main_script}")
        sys.exit(1)
    
    if not builder.config.resources_dir.exists():
        print(f"❌ 错误: 找不到资源目录 {builder.config.resources_dir}")
        sys.exit(1)
    
    # 执行构建
    success = builder.build()
    
    if success:
        print("\n✅ 所有操作完成!")
        input("\n按任意键退出...")
        sys.exit(0)
    else:
        print("\n❌ 构建失败!")
        input("\n按任意键退出...")
        sys.exit(1)


if __name__ == "__main__":
    main()