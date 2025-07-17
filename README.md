# FMM Creator App

一个专为游戏MOD制作者设计的现代化桌面应用程序，提供直观的界面来创建和管理游戏模组。

## 🌟 功能特性

- **多语言支持**: 支持中文、英文、日文、韩文四种语言界面
- **现代化UI**: 基于PySide6和Fluent Design设计语言的美观界面
- **MOD管理**: 便捷的MOD文件创建、编辑和管理功能
- **拖拽操作**: 支持文件拖拽，提升用户体验
- **配置管理**: 灵活的配置文件管理系统
- **跨平台**: 支持Windows、macOS和Linux系统

## 🛠️ 技术栈

- **Python 3.13+**: 主要开发语言
- **PySide6**: Qt6的Python绑定，提供现代化GUI
- **PySide6-Fluent-Widgets**: Fluent Design风格的UI组件库
- **py7zr**: 7z压缩文件处理
- **rarfile**: RAR文件处理

## 📦 安装说明

### 环境要求

- Python 3.13 或更高版本
- Windows 10/11 (推荐)

### 安装步骤

1. 克隆项目到本地：
```bash
git clone <repository-url>
cd FMM_Creator_App
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python main.py
```

### 打包为可执行文件

项目提供了Nuitka打包脚本，可以将应用打包为单文件可执行程序：

```bash
# 推荐方案: 分散打包+Data文件夹管理 (方案3) ⭐
Build_Solution\build_standalone_data.bat
python Build_Solution\build_nuitka-standalone_data.py

# 单文件exe方案 (方案1)
Build_Solution\build_single_exe.bat
python Build_Solution\build_nuitka-single_exe.py

# 传统构建方式（兼容性）
build.bat
```

打包完成后，可执行文件将生成在 `dist` 目录中。

## 🚀 使用方法

1. **启动应用**: 运行 `main.py` 或使用打包后的可执行文件
2. **语言设置**: 在设置界面选择您偏好的语言
3. **创建MOD**: 使用主界面的功能创建新的MOD项目
4. **文件管理**: 通过拖拽或文件选择器添加MOD文件
5. **配置编辑**: 编辑MOD的配置信息和元数据

## 📁 项目结构

```
FMM_Creator_App/
├── app/                    # 应用程序主目录
│   ├── common/            # 通用模块（配置、语言等）
│   ├── components/        # UI组件
│   ├── service/           # 业务逻辑服务
│   ├── view/              # 界面视图
│   ├── Resources/         # 资源文件（图标、样式等）
│   └── config/            # 配置文件
├── config/                # 全局配置
├── dist/                  # 打包输出目录
├── Build_Solution/       # 构建解决方案目录
│   ├── 📄 BUILD_SYSTEM_README.md          # 构建系统总览
│   ├── 📄 PACKAGING_GUIDE.md              # 打包方案详细对比
│   ├── 🔧 方案1: 单文件exe
│   │   ├── build_single_exe.bat           # 单文件构建脚本
│   │   ├── build_nuitka-single_exe.py     # 单文件Python脚本
│   │   └── DIST_README.md                 # 单文件分发说明
│   ├── 🔧 方案3: 分散打包+Data管理 ⭐
│   │   ├── build_standalone_data.bat       # Standalone构建脚本
│   │   ├── build_nuitka-standalone_data.py # Standalone Python脚本
│   │   ├── DIST_README_STANDALONE.md       # Standalone分发说明
│   │   └── STANDALONE_BUILD_GUIDE.md       # Standalone构建指南
│   └── 🛠️ 工具和文档
│       ├── update_build_version.py         # 版本更新工具
│       ├── pyproject.toml                  # 项目配置
│       └── *.md                           # 其他构建文档
├── build.bat             # 传统构建脚本（兼容性）
├── main.py               # 应用程序入口
├── requirements.txt      # Python依赖
├── LICENSE               # MIT开源协议
└── README.md             # 项目说明文档
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 🐛 问题反馈

如果您遇到任何问题或有功能建议，请在 [Issues](../../issues) 页面提交。

## 📞 联系方式

- 项目主页: [GitHub Repository](../../)
- 问题反馈: [Issues](../../issues)

---

**注意**: 本项目仍在积极开发中，功能和API可能会发生变化。建议在生产环境使用前进行充分测试。