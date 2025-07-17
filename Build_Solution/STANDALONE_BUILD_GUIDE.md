# FMM x Mod Creator - Standalone构建指南

## 📋 方案3: 分散打包+Data文件夹管理

### 🎯 方案概述

**方案3** 采用Nuitka的Standalone模式，将应用程序打包为分散的文件结构，所有依赖文件统一管理在 `Data/` 文件夹中。

### ✨ 方案优势

- **结构清晰**: 依赖文件统一管理在Data文件夹
- **启动速度快**: 无需解压缩，直接加载
- **调试友好**: 可直接访问和检查依赖文件
- **维护方便**: 配置文件独立管理
- **磁盘友好**: 避免临时文件解压

### 📁 目标结构

```
dist/
├── FMM x Mod Creator.exe     # 主可执行程序
├── Data/                     # 所有依赖文件 (Nuitka生成)
│   ├── PySide6/             # PySide6 GUI库文件
│   ├── scipy/               # 科学计算库文件
│   ├── numpy/               # 数值计算库文件
│   ├── *.dll                # Windows动态链接库
│   ├── Resources/           # 应用程序资源文件
│   └── ...                  # 其他Python依赖库
├── app/                     # 应用程序数据目录
│   ├── config/              # 配置文件目录
│   └── .cache/              # 缓存目录
└── README.md                # 分发说明文档
```

## 🚀 构建方法

### 方法1: 使用批处理脚本 (推荐)

```bash
# 在项目根目录下运行
Build_Solution\build_standalone_data.bat
```

**特点**:
- 自动检查Python环境和依赖
- 自动安装Nuitka (如果未安装)
- 一键完成整个构建流程
- 自动打开输出目录

### 方法2: 直接运行Python脚本

```bash
# 确保在项目根目录
cd /path/to/FMM_Creator_App

# 运行构建脚本
python Build_Solution\build_nuitka-standalone_data.py
```

**适用场景**:
- 需要自定义构建参数
- 集成到其他构建系统
- 调试构建过程

## ⚙️ 构建配置

### Nuitka参数配置

构建脚本使用以下关键Nuitka参数:

```python
# 基本配置
"--standalone"                    # 使用standalone模式
"--enable-plugin=pyside6"         # 启用PySide6插件
"--output-dir=dist"               # 输出目录
"--output-filename=FMM x Mod Creator.exe"  # 输出文件名

# Windows特定
"--windows-console-mode=disable"  # 禁用控制台窗口
"--windows-icon-from-ico=..."     # 设置应用程序图标

# 版本信息 (自动从version_info.py读取)
"--windows-file-version=..."      # 文件版本
"--windows-product-version=..."   # 产品版本
"--windows-file-description=..."  # 文件描述

# 数据文件包含
"--include-data-dir=Resources=Resources"  # 包含资源目录
"--include-data-file=version_info.py=..." # 包含版本文件

# 优化选项
"--assume-yes-for-downloads"      # 自动确认下载
"--show-progress"                 # 显示构建进度
"--remove-output"                 # 清理旧输出
```

### 数据文件管理

构建过程会自动:
1. 将Nuitka生成的依赖文件移动到 `Data/` 目录
2. 创建 `app/config/` 和 `app/.cache/` 目录结构
3. 复制配置文件到分发目录
4. 生成分发说明文档

## 🔧 构建流程详解

### 1. 环境检查
- 检查Python环境
- 检查Nuitka安装状态
- 验证项目文件完整性

### 2. 清理准备
- 删除旧的 `dist/` 目录
- 创建新的输出目录

### 3. 版本更新
- 从 `app/common/version_info.py` 读取版本信息
- 验证版本信息格式

### 4. Nuitka构建
- 执行Nuitka standalone构建
- 生成 `.dist` 临时目录

### 5. 文件组织
- 将依赖文件移动到 `Data/` 目录
- 移动主可执行文件到根目录
- 清理临时文件

### 6. 分发结构设置
- 创建 `app/` 目录结构
- 复制配置文件
- 生成说明文档

## 📊 构建输出

### 成功构建后的输出

```
🎉 构建完成!
   可执行文件: dist/FMM x Mod Creator.exe
   依赖文件: dist/Data
   
📦 Standalone分发结构 (方案3):
   dist/
   ├── FMM x Mod Creator.exe  (主可执行程序)
   ├── Data/                  (所有依赖文件)
   │   ├── PySide6/          (PySide6库文件)
   │   ├── *.dll             (动态链接库)
   │   └── ...               (其他依赖)
   ├── app/
   │   ├── config/           (配置文件)
   │   └── .cache/           (缓存目录)
   └── README.md             (说明文档)
   
   ✨ 特性: 结构清晰、启动快速、调试友好
```

### 文件大小估算

- **总大小**: 约 150-200MB
- **可执行文件**: 约 20-30MB
- **Data目录**: 约 120-170MB
  - PySide6: 约 80-100MB
  - 其他依赖: 约 40-70MB

## 🐛 故障排除

### 常见问题

#### 1. Nuitka构建失败
```
❌ Nuitka构建失败: Command failed
```
**解决方案**:
- 检查Python环境是否正确
- 确保所有依赖已安装: `pip install -r requirements.txt`
- 检查磁盘空间是否充足
- 尝试更新Nuitka: `pip install --upgrade nuitka`

#### 2. 找不到版本信息
```
❌ 错误: 无法导入版本信息模块
```
**解决方案**:
- 确保 `app/common/version_info.py` 文件存在
- 检查文件语法是否正确
- 验证Python路径配置

#### 3. 资源文件缺失
```
❌ 错误: 找不到资源目录
```
**解决方案**:
- 确保 `app/Resources/` 目录存在
- 检查图标文件 `FMMxModCreator_Icon.ico` 是否存在
- 验证资源文件路径

#### 4. 权限问题
```
❌ 权限被拒绝
```
**解决方案**:
- 以管理员身份运行构建脚本
- 检查输出目录的写入权限
- 关闭可能占用文件的程序

### 调试技巧

1. **详细输出**: 构建脚本会显示详细的进度信息
2. **日志检查**: 查看Nuitka的详细输出信息
3. **分步调试**: 可以注释掉部分构建步骤进行调试
4. **手动验证**: 检查中间生成的文件和目录

## 📈 性能优化

### 构建性能
- **并行构建**: Nuitka会自动使用多核CPU
- **缓存利用**: 重复构建会利用Nuitka缓存
- **依赖优化**: 排除不必要的模块可减少构建时间

### 运行性能
- **启动速度**: Standalone模式启动速度快
- **内存使用**: 合理的内存占用
- **磁盘IO**: 减少临时文件操作

## 🔄 版本管理

### 版本更新流程
1. 修改 `app/common/version_info.py` 中的版本信息
2. 运行构建脚本
3. 构建脚本会自动读取新版本信息
4. 生成带有正确版本信息的可执行文件

### 版本信息字段
- `VERSION_STRING`: 产品版本 (如 "1.0.0")
- `FULL_VERSION_STRING`: 文件版本 (如 "1.0.0.0")
- `file_description`: 文件描述
- `product_name`: 产品名称
- `company_name`: 公司名称

## 📚 相关文档

- `DIST_README_STANDALONE.md`: 分发版本说明文档
- `VERSION_UPDATE_GUIDE.md`: 版本更新指南
- `PACKAGING_GUIDE.md`: 打包方案对比
- `BUILD_SYSTEM_README.md`: 构建系统总览

---

**注意**: 方案3适合需要清晰文件结构和快速启动的场景。如果需要单文件分发，请考虑使用方案1的单文件模式。