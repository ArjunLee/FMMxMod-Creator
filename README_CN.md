<div align="center">

# 🎮 FMM x Mod Creator App

[![Language](https://img.shields.io/badge/Language-中文-blue.svg)](README_CN.md)
[![Language](https://img.shields.io/badge/Language-English-red.svg)](README.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt6-brightgreen.svg)](https://doc.qt.io/qtforpython/)
[![Stars](https://img.shields.io/github/stars/ArjunLee/FMMxMod-Creator?style=social)](https://github.com/ArjunLee/FMMxMod-Creator/stargazers)
[![Forks](https://img.shields.io/github/forks/ArjunLee/FMMxMod-Creator?style=social)](https://github.com/ArjunLee/FMMxMod-Creator/network/members)

![FMMxMod-Creator banner](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/banner_pic.png)

**🚀 专为游戏MOD爱好者打造的现代化MOD创建工具**

*使用美观的UI和现代化的便捷操作，无需理解和写任何代码，即可构建出极为复杂配置的`Fluffy Mod Manager`MOD文件包。*

[📥 下载最新版本](https://github.com/ArjunLee/FMMxMod-Creator/releases) • [📚 教学手册](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/eqg0qcvzd05g3dy4) • [🐛 问题反馈](https://github.com/ArjunLee/FMMxMod-Creator/issues) • [💬 讨论交流](https://github.com/ArjunLee/FMMxMod-Creator/discussions)

</div>

---

## 📦 安装方式

### 🎯 使用预编译版本（推荐）

![安装包截图](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_02-08-07.png)

1. 📥 从[Release页面](https://github.com/ArjunLee/FMMxMod-Creator/releases)下载最新的安装包
2. 📂 从`Mod列表 → 导入记录`导入：`root\FMMxMOD-Creator_build-record-20250716_2325.zip`，恢复我提供的示例构建模版
3. ✨ 从`操作按钮 → 再度编撰`恢复编辑器的布局，这是一个极为复杂的示例，有助于你充分了解编辑器的使用

### 🛠️ 从源码部署

#### 📋 安装步骤

1. **🐍 使用Conda创建Python环境**
```bash
conda create -n py313_env python=3.13 -y
conda activate py313_env
```

2. **📥 克隆项目到本地**
```bash
git clone https://github.com/ArjunLee/FMMxMod-Creator.git
cd FMMxMod-Creator
```

3. **📦 安装依赖**
```bash
pip install -r requirements.txt
```

4. **🚀 运行应用**
```bash
python main.py
```

---

## 🌟 功能特性

### 🌍 核心功能
- **🌐 多语言支持**: 支持`中文🇨🇳、英文🇺🇸、日文🇯🇵、韩文🇰🇷`四种语言实时切换
- **🎨 现代化UI**: 基于现代美学的 Fluent Design 风格UI界面
- **🖱️ 拖与拽**: 使用拖拽动作来对区块进行排序，无需编写任何代码
- **📱 响应式设计**: 支持不同屏幕尺寸和分辨率的自适应布局

### 📁 MOD文件管理
- **➕ 文件操作**: 支持添加文件、文件夹、重命名等操作
- **🏷️ 自定义标记**: 支持对区块进行自定义标记，方便在区块收起时定位作用
- **🔍 文件定位**: 快速查找和定位MOD文件
- **📋 批量操作**: 支持批量选择和操作多个文件

### 🗃️ MOD仓库管理
- **💾 备份构建记录**: 手动备份MOD构建历史，确保数据安全
- **📤 导入构建记录**: 分享构建记录，与他人合作创作
- **🔄 永久化构建**: 随时从构建历史中选择版本，恢复编辑器布局进行版本迭代
- **📊 版本对比**: 可视化对比不同版本间的差异

### ⚙️ 全自动构建
- **🤖 智能构建**: 全自动完成FMM所支持的文件夹结构
- **📦 多格式支持**: 支持打包为`.zip`、`.7z`、`.rar`格式
- **⚡ 快速构建**: 优化的构建算法，大幅提升构建速度
- **🔧 自定义配置**: 灵活的构建参数配置

### 🎛️ 设置
- **💾 构建缓存**: 可自定义缓存路径，默认：`%appdata%\FMM x MOD Creator\.cache`
- **📂 构建输出**: 可自定义输出路径，默认：`桌面`
- **🎨 主题切换**: 支持明暗主题切换
- **🔔 通知系统**: 构建完成和错误提醒

---

## 🎯 快速开始

### 1️⃣ 创建你的第一个MOD
1. 安装应用
2. 从[Release页面](https://github.com/ArjunLee/FMMxMod-Creator/releases)下载：
   - `Demo Projects - MOD Source Files.7z`
   - `Demo Projects - MOD build record.zip`
3. 从`MOD府库 → 导入记录 → Demo Projects - MOD build record.zip` 导入构建记录
4. 解压缩`Demo Projects - MOD Source Files.7z`
5. 从`MOD府库`恢复工作区布局，即可开始制作MOD。

### 3️⃣ 详细教学手册

我们为不同语言的用户提供了详细的教学手册：

- 📚 [中文教学手册](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/eqg0qcvzd05g3dy4) 🇨🇳
- 📚 [English Tutorial Manual](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/qh3km88g2ma10pi5) 🇺🇸
- 📚 [日本語チュートリアル](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/ff8wzvahd1ni7397) 🇯🇵
- 📚 [한국어 튜토리얼](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/bx9w5a6ua3mgr29q) 🇰🇷

---

## 📸 应用截图

<div align="center">

### 🏠 主界面
![主界面截图](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_05-09-52.png)

### 📋 MOD府库
![MOD府库截图](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_05-11-36.png)

### ⚙️ 设置页面
![设置页面截图](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_05-12-32.png)

</div>

---

## 🎬 效果展示

### 📹 MOD制作效果视频

<div align="center">

<iframe width="560" height="315" src="https://www.youtube.com/embed/LnWoCBpKzdI?si=pOyXN4bgmFIaeZro" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

*此视频展示了使用本工具制作的MOD在FFM中的实际效果*

</div>

---

## 🏆 案例展示

以下是使用本工具制作并发布在Nexusmods上的真实MOD案例：

<div align="center">

### 🎮 案例一：尼尔2B制服模组
**FMM_FOMOD-YoRHa_No.2_Type_B_Uniform-Modular-CN_EN**

[![Nexusmods链接](https://img.shields.io/badge/Nexusmods-查看MOD-orange?style=for-the-badge&logo=nexusmods)](https://www.nexusmods.com/stellarblade/mods/904)

### 🎮 案例二：尼尔非官方礼服模组
**FMM_FOMOD-YoRHa Unofficial Ceremonial Attire - Modular - CN_EN**

[![Nexusmods链接](https://img.shields.io/badge/Nexusmods-查看MOD-orange?style=for-the-badge&logo=nexusmods)](https://www.nexusmods.com/stellarblade/mods/990)

</div>

*这些MOD展示了工具在创建复杂、模块化MOD方面的能力。*

---

### 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **🐍 Python** | 3.13+ | 主要开发语言 |
| **🖼️ PySide6** | Latest | Qt6的Python绑定，提供现代化GUI |
| **🎨 PySide6-Fluent-Widgets** | Latest | Fluent Design风格的UI组件库 |
| **📦 py7zr** | Latest | 7z压缩文件处理 |
| **📁 rarfile** | Latest | RAR文件处理 |
| **⚡ Nuitka** | Latest | Python代码编译和打包 |

### 🔨 关于构建

我们提供了`Nuitka`打包的自动化解决方案，您可以根据需要选择不同的方案：

```bash
# 🌟 推荐方案: 分散打包 (启动快)
Build_Solution\build_standalone_data.bat
# 或使用Python脚本
python Build_Solution\build_nuitka-standalone_data.py

# 📦 单文件方案 (便于分发)
Build_Solution\build_single_exe.bat
# 或使用Python脚本
python Build_Solution\build_nuitka-single_exe.py

# ⚠️ 传统构建方式（已弃用）
build.bat
```

✅ 打包完成后，可执行文件将生成在 `dist` 目录中。

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！🎉

### 🐛 报告问题
- 在[Issues页面](https://github.com/ArjunLee/FMMxMod-Creator/issues)提交bug报告
- 请详细描述问题和复现步骤

### 💡 功能建议
- 在[Discussions页面](https://github.com/ArjunLee/FMMxMod-Creator/discussions)分享你的想法
- 参与功能讨论和投票



---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🐛 问题反馈

如果您遇到任何问题或有功能建议，请在以下渠道联系我们：

- 🐛 [Issues页面](https://github.com/ArjunLee/FMMxMod-Creator/issues) - 报告bug和功能请求
- 💬 [Discussions页面](https://github.com/ArjunLee/FMMxMod-Creator/discussions) - 社区讨论和交流
- 📧 [联系作者](mailto:shin3sango@qq.com) - Email

---

## 📞 联系方式

<div align="center">

| 平台 | 链接 | 描述 |
|------|------|------|
| 🏠 **项目主页** | [GitHub Repository](https://github.com/ArjunLee/FMMxMod-Creator) | 项目源码和发布 |
| 🐛 **问题反馈** | [Issues](https://github.com/ArjunLee/FMMxMod-Creator/issues) | Bug报告和功能请求 |
| 💬 **社区讨论** | [Discussions](https://github.com/ArjunLee/FMMxMod-Creator/discussions) | 用户交流和讨论 |
| 📖 **使用文档** | [Wiki](https://github.com/ArjunLee/FMMxMod-Creator/wiki) | 详细使用教程 |
| 💬 **微信联系** | WX - shin3sango | 开发者微信 |

</div>

---

## ☕ 请我喝杯咖啡

如果这个项目对您有帮助，不妨请我喝杯咖啡，支持一下开发！☕

<div align="center">

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/H2H51HJEYI)

*您的支持是我持续开发的动力！* 💪

</div>

---

<div align="center">

**⚠️ 注意**: 本项目仍在积极开发中，功能和API可能会发生变化。建议在生产环境使用前进行充分测试。

**🎉 感谢所有贡献者和用户的支持！**

---

*Made with ❤️ by [ArjunLee](https://github.com/ArjunLee)*

</div>

---

## 📁 项目结构

```
FMMxMod-Creator/
├── 📄 .gitignore                          # Git忽略文件配置
├── 📁 Build_Solution/                     # 🔨 构建解决方案目录
│   ├── 📋 BUILD_SYSTEM_README.md          # 构建系统总览
│   ├── 📋 PACKAGING_GUIDE.md              # 打包方案详细对比
│   ├── 📋 STANDALONE_BUILD_GUIDE.md       # Standalone构建指南
│   ├── 📋 DIST_README_STANDALONE.md       # Standalone分发说明
│   ├── 🔧 build_single_exe.bat            # 单文件构建脚本
│   ├── 🔧 build_standalone_data.bat       # Standalone构建脚本
│   ├── 🐍 build_nuitka-single_exe.py      # 单文件Python脚本
│   ├── 🐍 build_nuitka-standalone_data.py # Standalone Python脚本
│   ├── 🐍 test_build_config.py            # 构建配置测试
│   ├── 🐍 update_build_version.py         # 版本更新工具
│   └── ⚙️ pyproject.toml                  # 项目配置文件
├── 📦 FMMxMOD-Creator_build-record-*.zip  # 示例构建记录
├── 📄 LICENSE                             # MIT开源协议
├── 📄 README_CN.md                        # 中文说明文档
├── 📄 README.md                           # 英文说明文档
├── 📁 app/                                # 🏠 应用程序主目录
│   ├── 📁 Resources/                      # 🎨 资源文件目录
│   │   ├── 🎬 Drag_and_Drop_Example_Video.gif # 拖拽示例动画
│   │   ├── 🎬 modlist_editing_tips.gif    # 编辑提示动画
│   │   ├── 🖼️ FMMxModCreator_Icon.ico     # 应用图标
│   │   ├── 🖼️ FMMxModCreator_Icon_512.png # 高清应用图标
│   │   ├── 🎨 Drag_and_drop_black.svg     # 拖拽图标(黑色)
│   │   ├── 🎨 Drag_and_drop_white.svg     # 拖拽图标(白色)
│   │   ├── 🎨 Edit_black.svg              # 编辑图标(黑色)
│   │   ├── 🎨 Edit_white.svg              # 编辑图标(白色)
│   │   └── 📁 qss/                        # 样式表文件
│   ├── 📄 __init__.py                     # 包初始化文件
│   ├── 📁 common/                         # 🔧 通用模块
│   │   ├── 📄 __init__.py                 # 包初始化
│   │   ├── 🏠 application.py              # 应用程序主类
│   │   ├── ⚙️ config.py                   # 配置管理
│   │   ├── 🔧 config_utils.py             # 配置工具函数
│   │   ├── 🌍 language.py                 # 多语言支持
│   │   └── ℹ️ version_info.py             # 版本信息
│   ├── 📁 components/                     # 🧩 UI组件
│   │   ├── 📄 __init__.py                 # 包初始化
│   │   ├── ➕ add_function_card.py        # 添加功能卡片
│   │   ├── 🛡️ cover_block.py              # 封面区块
│   │   ├── 💬 edit_tips_dialog.py         # 编辑提示对话框
│   │   ├── 📁 file_display_widget.py      # 文件显示组件
│   │   ├── 🎈 floating_menu_button.py     # 浮动菜单按钮
│   │   ├── 📦 mod_file_block.py           # MOD文件区块
│   │   ├── 🎴 mod_info_card.py            # MOD信息卡片
│   │   ├── 📊 mod_table_widget.py         # MOD表格组件
│   │   ├── ➖ separator_block.py           # 分隔符区块
│   │   └── ⚠️ warning_block.py            # 警告区块
│   ├── 📁 config/                         # ⚙️ 配置文件
│   │   ├── 🔧 app_config.json             # 应用配置
│   │   └── 📋 mod_list_table_config.json  # MOD列表表格配置
│   ├── 📁 service/                        # 🔧 业务逻辑服务
│   │   ├── 💾 build_record_service.py     # 构建记录服务
│   │   ├── 🔨 build_service.py            # 构建服务
│   │   └── 🔄 restore_service.py          # 恢复服务
│   └── 📁 view/                           # 🖼️ 界面视图
│       ├── 📄 __init__.py                 # 包初始化
│       ├── 🏠 home_interface.py           # 主页界面
│       ├── 🖼️ main_window.py              # 主窗口
│       ├── 📋 mod_list_interface.py       # MOD列表界面
│       └── ⚙️ settings_interface.py       # 设置界面
├── 📁 config/                             # 🌐 全局配置
│   └── ⚙️ config.json                     # 全局配置文件
├── 🚀 main.py                             # 应用程序入口
├── 🖼️ png2ico.py                          # PNG转ICO小脚本
├── 📋 requirements.txt                    # Python依赖列表
└── 📦 测试错误的构建配置文件导入.zip           # 测试文件
```