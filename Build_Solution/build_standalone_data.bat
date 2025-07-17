@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   FMM x Mod Creator - Standalone构建
echo   方案3: 分散打包+Data文件夹管理
echo ========================================
echo.

REM 切换到项目根目录
cd ..

REM 检查Python环境
echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python环境
    echo    请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

REM 检查Nuitka
echo 🔍 检查Nuitka...
python -m nuitka --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Nuitka
    echo    正在安装Nuitka...
    pip install nuitka
    if errorlevel 1 (
        echo ❌ Nuitka安装失败
        pause
        exit /b 1
    )
)

REM 检查依赖
echo 🔍 检查项目依赖...
if not exist "requirements.txt" (
    echo ❌ 错误: 找不到requirements.txt
    pause
    exit /b 1
)

REM 安装依赖
echo 📦 安装/更新依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo.
echo 🚀 开始Standalone构建...
echo.

REM 执行构建脚本
python Build_Solution\build_nuitka-standalone_data.py

REM 检查构建结果
if errorlevel 1 (
    echo.
    echo ❌ 构建失败!
    pause
    exit /b 1
) else (
    echo.
    echo ✅ 构建成功!
    echo.
    echo 📁 输出目录: dist\
    echo 🎯 可执行文件: dist\FMM x Mod Creator.exe
    echo 📦 依赖文件: dist\Data\
    echo 📋 配置文件: dist\app\config\
    echo.
)

pause