# FMM x Mod Creator - 构建系统说明

## 📋 构建方案总览

本项目提供多种构建方案，以满足不同的分发需求:

| 方案 | 模式 | 特点 | 适用场景 |
|------|------|------|----------|
| **方案1** | 单文件exe | 单个可执行文件，便于分发 | 简单分发、便携使用 |
| **方案2** | 目录模式 | 传统的目录结构打包 | 开发调试、传统部署 |
| **方案3** ⭐ | 分散打包+Data管理 | 结构清晰、启动快速 | 生产环境、专业分发 |

## 🚀 快速开始

### 推荐方案: 方案3 (分散打包+Data文件夹管理)

```bash
# 方法1: 使用批处理脚本 (推荐)
Build_Solution\build_standalone_data.bat

# 方法2: 直接运行Python脚本
python Build_Solution\build_nuitka-standalone_data.py
```

### 其他方案

```bash
# 方案1: 单文件exe
Build_Solution\build_single_exe.bat
python Build_Solution\build_nuitka-single_exe.py

# 传统构建 (兼容性)
build.bat
```

## 📁 构建文件结构

```
Build_Solution/
├── 📄 BUILD_SYSTEM_README.md          # 本文档 - 构建系统总览
├── 📄 PACKAGING_GUIDE.md              # 打包方案详细对比
├── 📄 VERSION_UPDATE_GUIDE.md         # 版本更新指南
├── 📄 VERSION_MANAGEMENT_ANALYSIS.md  # 版本管理分析
│
├── 🔧 方案1: 单文件exe
│   ├── build_nuitka-single_exe.py     # 单文件构建脚本
│   ├── build_single_exe.bat           # 单文件批处理脚本
│   └── DIST_README.md                 # 单文件分发说明
│
├── 🔧 方案3: 分散打包+Data管理 ⭐
│   ├── build_nuitka-standalone_data.py # Standalone构建脚本
│   ├── build_standalone_data.bat       # Standalone批处理脚本
│   ├── DIST_README_STANDALONE.md       # Standalone分发说明
│   └── STANDALONE_BUILD_GUIDE.md       # Standalone构建指南
│
├── 🛠️ 工具脚本
│   ├── update_build_version.py         # 版本更新工具
│   └── pyproject.toml                  # 项目配置文件
│
└── 📚 文档
    └── (各种构建相关文档)
```

## 🎯 方案详细说明

### 方案1: 单文件exe

**特点**:
- ✅ 单个可执行文件
- ✅ 便于分发和传输
- ✅ 无需安装
- ⚠️ 首次启动较慢 (需解压)
- ⚠️ 文件较大

**输出结构**:
```
dist/
├── FMM x Mod Creator.exe  # 单个可执行文件
└── README.md              # 说明文档
```

**使用场景**:
- 快速分发给最终用户
- 便携式使用
- 简化部署流程

### 方案3: 分散打包+Data文件夹管理 ⭐

**特点**:
- ✅ 结构清晰，依赖文件统一管理
- ✅ 启动速度快，无需解压缩
- ✅ 调试友好，可直接访问依赖文件
- ✅ 维护方便，配置文件独立管理
- ⚠️ 文件较多，需保持目录结构

**输出结构**:
```
dist/
├── FMM x Mod Creator.exe     # 主可执行程序
├── Data/                     # 所有依赖文件
│   ├── PySide6/             # GUI库文件
│   ├── *.dll                # 动态链接库
│   └── ...                  # 其他依赖
├── app/                     # 应用数据目录
│   ├── config/              # 配置文件
│   └── .cache/              # 缓存目录
└── README.md                # 说明文档
```

**使用场景**:
- 生产环境部署
- 需要快速启动的场景
- 需要访问依赖文件的调试场景
- 专业软件分发

## ⚙️ 构建配置

### 版本管理

所有构建方案都会自动从 `app/common/version_info.py` 读取版本信息:

```python
# 版本信息会自动应用到:
--windows-file-version      # 文件版本
--windows-product-version   # 产品版本
--windows-file-description  # 文件描述
--windows-product-name      # 产品名称
--windows-company-name      # 公司名称
```

### 资源文件包含

所有方案都会自动包含:
- `app/Resources/` 目录下的所有资源文件
- `app/common/version_info.py` 版本信息文件
- 应用程序图标文件

### Nuitka插件

自动启用的插件:
- `pyside6`: PySide6 GUI框架支持
- 其他必要的依赖插件

## 🔧 环境要求

### 开发环境
- **Python**: 3.8+ (推荐 3.9+)
- **Nuitka**: 最新版本
- **操作系统**: Windows 10/11

### 依赖安装
```bash
# 安装项目依赖
pip install -r requirements.txt

# 安装Nuitka (如果未安装)
pip install nuitka
```

### 系统要求
- **内存**: 建议 8GB+ (构建时)
- **磁盘空间**: 至少 2GB 可用空间
- **CPU**: 多核CPU可加速构建

## 🚀 构建流程

### 标准构建流程

1. **环境检查**
   - 验证Python环境
   - 检查Nuitka安装
   - 确认依赖完整性

2. **版本更新**
   - 读取 `version_info.py`
   - 验证版本格式
   - 应用版本信息

3. **清理准备**
   - 清理旧的构建输出
   - 创建输出目录

4. **Nuitka构建**
   - 执行Nuitka编译
   - 应用配置参数
   - 包含资源文件

5. **后处理**
   - 组织输出结构
   - 复制配置文件
   - 生成说明文档

### 自动化特性

- **依赖检查**: 自动检查和安装缺失的依赖
- **版本同步**: 自动从源码读取版本信息
- **资源包含**: 自动包含必要的资源文件
- **结构优化**: 自动优化输出目录结构

## 📊 性能对比

| 指标 | 方案1 (单文件) | 方案3 (Standalone) |
|------|----------------|--------------------|
| **文件大小** | ~180MB | ~200MB (总计) |
| **启动速度** | 慢 (需解压) | 快 (直接加载) |
| **分发便利性** | 极高 | 中等 |
| **调试友好性** | 低 | 高 |
| **维护便利性** | 低 | 高 |
| **磁盘占用** | 单文件 | 多文件 |

## 🐛 故障排除

### 常见问题

#### 1. 构建失败
```bash
# 检查环境
python --version
python -m nuitka --version

# 重新安装依赖
pip install --upgrade -r requirements.txt
pip install --upgrade nuitka
```

#### 2. 版本信息错误
- 检查 `app/common/version_info.py` 语法
- 确认版本格式符合要求
- 验证文件编码为UTF-8

#### 3. 资源文件缺失
- 确认 `app/Resources/` 目录存在
- 检查图标文件路径
- 验证资源文件权限

#### 4. 权限问题
- 以管理员身份运行
- 检查输出目录权限
- 关闭占用文件的程序

### 调试技巧

1. **详细日志**: 构建脚本提供详细的进度信息
2. **分步调试**: 可以注释部分构建步骤
3. **手动验证**: 检查中间生成的文件
4. **环境隔离**: 使用虚拟环境避免依赖冲突

## 📚 相关文档

- **[PACKAGING_GUIDE.md](PACKAGING_GUIDE.md)**: 详细的打包方案对比
- **[STANDALONE_BUILD_GUIDE.md](STANDALONE_BUILD_GUIDE.md)**: 方案3构建指南
- **[VERSION_UPDATE_GUIDE.md](VERSION_UPDATE_GUIDE.md)**: 版本更新指南
- **[VERSION_MANAGEMENT_ANALYSIS.md](VERSION_MANAGEMENT_ANALYSIS.md)**: 版本管理分析

## 🔄 更新日志

### 最新更新
- ✅ 新增方案3: 分散打包+Data文件夹管理
- ✅ 优化构建脚本结构和错误处理
- ✅ 完善文档体系和使用指南
- ✅ 统一版本管理和自动化流程

### 计划改进
- 🔄 添加更多构建选项和自定义配置
- 🔄 支持Linux和macOS构建
- 🔄 集成CI/CD自动化构建
- 🔄 添加构建性能分析工具

---

**推荐**: 对于大多数用户，建议使用 **方案3 (分散打包+Data文件夹管理)**，它提供了最佳的性能和维护性平衡。