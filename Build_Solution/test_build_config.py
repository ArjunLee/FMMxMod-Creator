#!/usr/bin/env python3
# coding:utf-8
"""
测试构建配置脚本
用于验证构建脚本的配置是否正确，而不进行实际构建
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "app"))

def test_version_import():
    """测试版本信息导入"""
    print("🔍 测试版本信息导入...")
    try:
        from common import version_info
        print("✅ 成功导入版本信息 (方式1: from common import version_info)")
        return version_info
    except ImportError:
        try:
            from app.common import version_info
            print("✅ 成功导入版本信息 (方式2: from app.common import version_info)")
            return version_info
        except ImportError:
            print("❌ 无法导入版本信息模块")
            print(f"请确保 {project_root / 'app' / 'common' / 'version_info.py'} 文件存在")
            return None

def test_file_structure():
    """测试文件结构"""
    print("\n🔍 测试文件结构...")
    
    required_files = [
        project_root / "main.py",
        project_root / "app" / "Resources" / "FMMxModCreator_Icon.ico",
        project_root / "app" / "common" / "version_info.py",
        project_root / "requirements.txt"
    ]
    
    all_exist = True
    for file_path in required_files:
        if file_path.exists():
            print(f"✅ {file_path.relative_to(project_root)}")
        else:
            print(f"❌ {file_path.relative_to(project_root)} (缺失)")
            all_exist = False
    
    return all_exist

def test_build_config():
    """测试构建配置"""
    print("\n🔍 测试构建配置...")
    
    # 导入构建配置类
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        # 修正模块名称
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "build_module", 
            Path(__file__).parent / "build_nuitka-standalone_data.py"
        )
        build_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_module)
        NuitkaStandaloneBuildConfig = build_module.NuitkaStandaloneBuildConfig
        
        config = NuitkaStandaloneBuildConfig()
        print("✅ 构建配置类导入成功")
        
        # 测试版本信息
        version_info = config.version_info
        print(f"   产品版本: {version_info['product_version']}")
        print(f"   文件版本: {version_info['file_version']}")
        print(f"   产品名称: {version_info['product_name']}")
        print(f"   公司名称: {version_info['company_name']}")
        
        # 测试Nuitka参数
        nuitka_args = config.get_nuitka_args()
        print(f"   Nuitka参数数量: {len(nuitka_args)}")
        print(f"   输出文件: {config.output_filename}")
        print(f"   主脚本: {config.main_script}")
        
        return True
        
    except Exception as e:
        print(f"❌ 构建配置测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 FMM x Mod Creator - 构建配置测试")
    print("=" * 50)
    
    # 测试版本导入
    version_info = test_version_import()
    if not version_info:
        print("\n❌ 版本信息导入失败，无法继续测试")
        return False
    
    # 测试文件结构
    files_ok = test_file_structure()
    if not files_ok:
        print("\n⚠️  部分必要文件缺失，可能影响构建")
    
    # 测试构建配置
    config_ok = test_build_config()
    
    print("\n" + "=" * 50)
    if version_info and config_ok:
        print("✅ 所有测试通过！构建配置正常")
        print("\n🎯 可以使用以下命令进行构建:")
        print("   Build_Solution\\build_standalone_data.bat")
        print("   python Build_Solution\\build_nuitka-standalone_data.py")
        return True
    else:
        print("❌ 部分测试失败，请检查配置")
        return False

if __name__ == "__main__":
    success = main()
    input("\n按任意键退出...")
    sys.exit(0 if success else 1)