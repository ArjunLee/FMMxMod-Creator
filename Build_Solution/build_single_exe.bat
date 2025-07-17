@echo off
chcp 65001 >nul
echo.
echo 🚀 FMM x Mod Creator - 优化构建脚本
echo ==========================================
echo.
echo 使用优化的Nuitka打包解决方案
echo - 单文件EXE打包
echo - 同目录配置文件支持
echo - 动态版本号管理
echo - 英文版本信息（避免乱码）
echo.

REM 检查Python环境
echo 🔍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 找不到Python环境
    echo    请确保Python已正确安装并添加到PATH
    goto :error
)

REM 检查Nuitka
echo 🔍 检查Nuitka...
python -c "import nuitka" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 找不到Nuitka
    echo    正在尝试安装Nuitka...
    pip install nuitka
    if %errorlevel% neq 0 (
        echo ❌ Nuitka安装失败
        goto :error
    )
)

REM 检查必要的依赖
echo 🔍 检查项目依赖...
cd ..
python -c "import PySide6" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 找不到PySide6
    echo    请运行: pip install -r requirements.txt
    goto :error
)

echo ✅ 环境检查完成
echo.

REM 运行优化构建脚本
echo 🔨 启动优化构建流程...
echo.
python Build_Solution\build_nuitka-single_exe.py

if %errorlevel% equ 0 (
    echo.
    echo 🎉 构建成功完成!
    echo.
    echo 📦 输出文件:
    echo    ..\dist\FMM x Mod Creator.exe
    echo.
    echo 📁 分发结构:
    echo    dist\
    echo    ├── FMM x Mod Creator.exe  (单文件可执行程序)
    echo    ├── app\
    echo    │   ├── config\            (配置文件)
    echo    │   └── .cache\            (缓存目录)
    echo    └── README.md             (说明文档)
    echo.
    echo ✨ 特性:
    echo    • 单文件EXE，无需安装
    echo    • 配置文件位于exe同目录
    echo    • 资源文件已嵌入
    echo    • 英文版本信息，避免乱码
    echo    • 动态版本号管理
    goto :success
) else (
    echo.
    echo ❌ 构建失败!
    echo    请检查上方的错误信息
    goto :error
)

:success
echo.
echo ✅ 所有操作完成!
goto :end

:error
echo.
echo ❌ 操作失败!
echo    请检查错误信息并重试
goto :end

:end
echo.
echo 按任意键退出...
pause >nul