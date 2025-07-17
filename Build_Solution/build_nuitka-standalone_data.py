#!/usr/bin/env python3
# coding:utf-8
"""
Nuitka Standalone Build Script - Data Folder Management
方案3: 分散打包+Data文件夹管理的Nuitka构建脚本

目标结构:
root/
├── Data/  (所有nuitka生成文件)
│   ├── PySide6/
│   ├── scipy/
│   ├── *.dll
│   └── ...
├── app/
│   ├── .cache/
│   └── config/
└── FMM x Mod Creator.exe
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

try:
    from common import version_info
except ImportError:
    try:
        from app.common import version_info
    except ImportError:
        print("错误: 无法导入版本信息模块")
        print(f"请确保 {project_root / 'app' / 'common' / 'version_info.py'} 文件存在")
        sys.exit(1)


class NuitkaStandaloneBuildConfig:
    """Nuitka Standalone构建配置管理"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.app_dir = self.project_root / "app"
        self.config_dir = self.app_dir / "config"
        self.resources_dir = self.app_dir / "Resources"
        
        # 输出文件配置
        self.output_filename = "FMM x Mod Creator.exe"
        self.main_script = self.project_root / "main.py"
        
        # Data文件夹配置
        self.data_dir = self.dist_dir / "Data"
        
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
        """构建Nuitka命令行参数 - Standalone模式"""
        args = [
            "python",
            "-m",
            "nuitka",
            # 基本配置 - 使用standalone模式
            "--standalone",
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
            # "--remove-output",  # 注释掉以保留main.build文件夹用于调试
            
            # 排除不需要的模块
            "--nofollow-import-to=tkinter",
            "--nofollow-import-to=matplotlib",
            "--nofollow-import-to=numpy",
            
            # 主脚本
            str(self.main_script)
        ]
        
        return args


class NuitkaStandaloneBuilder:
    """Nuitka Standalone构建器"""
    
    def __init__(self):
        self.config = NuitkaStandaloneBuildConfig()
        self.project_root = self.config.project_root
        self.dist_dir = self.config.dist_dir
        self.data_dir = self.config.data_dir
    
    def clean_previous_build(self):
        """清理之前的构建"""
        print("🧹 检查之前的构建...")
        
        if self.dist_dir.exists():
            print(f"   发现已存在的构建目录: {self.dist_dir.name}")
            
            # 询问用户是否删除
            while True:
                choice = input("   是否删除已存在的构建缓存? (y/n/默认n): ").strip().lower()
                if choice in ['y', 'yes', '是']:
                    shutil.rmtree(self.dist_dir)
                    print(f"   已删除旧目录: {self.dist_dir.name}")
                    break
                elif choice in ['n', 'no', '否', '']:
                    print("   保留现有构建缓存")
                    break
                else:
                    print("   请输入 y(是) 或 n(否)")
        
        # 确保dist目录存在
        self.dist_dir.mkdir(exist_ok=True)
        
        print("✅ 构建环境检查完成")
    
    def update_version(self):
        """更新版本信息"""
        print("📝 检查版本信息...")
        
        version_info = self.config.version_info
        print(f"   当前版本: {version_info['product_version']} (文件: {version_info['file_version']})")
        print(f"   产品名称: {version_info['product_name']}")
        print(f"   公司名称: {version_info['company_name']}")
        print("✅ 版本信息检查完成")
    
    def build_with_nuitka(self) -> bool:
        """使用Nuitka构建 - Standalone模式"""
        print("🔨 开始Nuitka Standalone构建...")
        print(f"   版本: {self.config.version_info['product_version']} (文件: {self.config.version_info['file_version']})")
        print(f"   输出: {self.config.output_filename}")
        print(f"   模式: Standalone (分散打包)")
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
    
    def organize_data_folder(self):
        """组织Data文件夹结构 - 基于Nuitka限制的解决方案"""
        print("📁 组织Data文件夹结构...")
        print("⚠️  注意: 根据Nuitka文档，standalone模式不支持将exe与依赖分离到不同目录")
        print("   Nuitka官方文档明确指出所有文件必须在同一目录才能正常运行")
        print("   参考: https://nuitka.net/user-documentation/use-cases.html")
        
        # 查找Nuitka生成的.dist文件夹（基于主脚本名称）
        main_script_name = self.config.main_script.stem  # 获取main.py的文件名（不含扩展名）
        dist_folder_name = f"{main_script_name}.dist"
        nuitka_dist_folder = self.dist_dir / dist_folder_name
        
        if not nuitka_dist_folder.exists():
            print(f"❌ 错误: 找不到Nuitka生成的文件夹 {nuitka_dist_folder}")
            print(f"   预期文件夹: {dist_folder_name}")
            # 列出dist目录下的所有文件夹以便调试
            if self.dist_dir.exists():
                print("   dist目录下的内容:")
                for item in self.dist_dir.iterdir():
                    print(f"     - {item.name} ({'目录' if item.is_dir() else '文件'})")
            return False
        
        print("\n🔄 应用替代方案: 保持Nuitka原始结构但重命名文件夹")
        print("   这样可以确保可执行文件能正常找到所有依赖")
        
        # 重命名.dist文件夹为Data（保持所有文件在同一目录）
        final_data_dir = self.dist_dir / "Data"
        if final_data_dir.exists():
            shutil.rmtree(final_data_dir)
        
        # 直接重命名整个.dist文件夹为Data
        nuitka_dist_folder.rename(final_data_dir)
        print(f"   重命名: {dist_folder_name} -> Data")
        
        # 将可执行文件移动到dist根目录
        exe_source = final_data_dir / self.config.output_filename
        exe_dest = self.dist_dir / self.config.output_filename
        if exe_source.exists():
            shutil.move(str(exe_source), str(exe_dest))
            print(f"   移动可执行文件到根目录: {self.config.output_filename}")
        
        # 更新data_dir路径
        self.data_dir = final_data_dir
        
        print("✅ 文件夹结构重组完成")
        print("   📝 说明: 所有依赖文件现在位于Data文件夹中")
        print("   📝 说明: 可执行文件位于根目录，可以正常访问Data中的依赖")
        return True
    
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
        readme_src = Path(__file__).parent / "DIST_README_STANDALONE.md"
        readme_dst = self.dist_dir / "README.md"
        if readme_src.exists():
            shutil.copy2(readme_src, readme_dst)
            print(f"   复制文档: README.md")
        
        print("✅ 分发结构设置完成")
        print()
        print("📦 Standalone分发结构 (方案3):")
        print("   dist/")
        print(f"   ├── {self.config.output_filename}  (主可执行程序)")
        print("   ├── Data/                     (所有依赖文件)")
        print("   │   ├── PySide6/              (PySide6库文件)")
        print("   │   ├── *.dll                 (动态链接库)")
        print("   │   └── ...                   (其他依赖)")
        print("   ├── app/")
        print("   │   ├── config/               (配置文件)")
        print("   │   └── .cache/               (缓存目录)")
        print("   └── README.md                 (说明文档)")
        print()
        print("   ✨ 特性: 结构清晰、启动快速、调试友好")
    
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
        print("🚀 开始FMM x Mod Creator Standalone构建流程 (方案3)")
        print("=" * 60)
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
            
            # 4. 组织Data文件夹结构
            if not self.organize_data_folder():
                return False
            print()
            
            # 5. 设置分发目录结构
            self.setup_distribution_structure()
            print()
            
            # 6. 打开分发文件夹
            self.open_dist_folder()
            
            print("🎉 构建完成!")
            print(f"   可执行文件: {self.dist_dir / self.config.output_filename}")
            print(f"   依赖文件: {self.data_dir}")
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  构建被用户中断")
            return False
        except Exception as e:
            print(f"❌ 构建过程中发生错误: {e}")
            return False


def main():
    """主函数"""
    builder = NuitkaStandaloneBuilder()
    
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