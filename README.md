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

<div align="center">

## [📖 README_ZH](README_CN.md) | README_EN

</div>

**🚀 Modern MOD Creation Tool for Game MOD Enthusiasts**

*Create complex `Fluffy Mod Manager` MOD packages with beautiful UI and modern convenient operations, without understanding or writing any code.*

[📥 Download Latest](https://github.com/ArjunLee/FMMxMod-Creator/releases) • [📚 Tutorial Manual](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/qh3km88g2ma10pi5) • [🐛 Report Issues](https://github.com/ArjunLee/FMMxMod-Creator/issues) • [💬 Discussions](https://github.com/ArjunLee/FMMxMod-Creator/discussions)

</div>

---

## Installation

### Using Pre-built Version (Recommended)

![Installation Screenshot](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_02-08-07.png)

1. Download the latest installer from [Release page](https://github.com/ArjunLee/FMMxMod-Creator/releases)
2. Import from `Mod List → Import Record`: `root\FMMxMOD-Creator_build-record-20250716_2325.zip` to restore the example build template I provided
3. Restore the editor layout from `Action Button → Re-edit`. This is an extremely complex example that helps you fully understand how to use the editor

### Deploy from Source

#### Installation Steps

1. **Create Python Environment**
```bash
conda create -n py313_env python=3.13 -y
conda activate py313_env
```

2. **Clone Project**
```bash
git clone https://github.com/ArjunLee/FMMxMod-Creator.git
cd FMMxMod-Creator
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run Application**
```bash
python main.py
```

---

## Features

### Core Features
- **Multi-language Support**: Real-time switching between `Chinese🇨🇳, English🇺🇸, Japanese🇯🇵, Korean🇰🇷`
- **Modern UI**: Fluent Design style interface based on modern aesthetics
- **Drag & Drop**: Use drag actions to sort blocks without writing any code
- **Responsive Design**: Adaptive layout supporting different screen sizes and resolutions

### MOD File Management
- **File Operations**: Support adding files, folders, renaming, and other operations
- **Custom Tags**: Support custom tagging of blocks for easy location when blocks are collapsed
- **Smart Search**: Quickly find and locate MOD files
- **Batch Operations**: Support batch selection and operations on multiple files

### MOD Repository Management
- **Backup Build Records**: Manually backup MOD build history to ensure data safety
- **Import Build Records**: Share build records and collaborate with others
- **Persistent Builds**: Restore editor layout from build history anytime for version iteration
- **Version Comparison**: Visual comparison of differences between versions

### Fully Automated Building
- **Smart Building**: Automatically complete folder structures supported by FMM
- **Multi-format Support**: Support packaging as `.zip`, `.7z`, `.rar` formats
- **Fast Building**: Optimized build algorithms for significantly improved build speed
- **Custom Configuration**: Flexible build parameter configuration

### Advanced Settings
- **Build Cache**: Customizable cache path, default: `%appdata%\FMM x MOD Creator\.cache`
- **Build Output**: Customizable output path, default: `Desktop`
- **Theme Switching**: Support light/dark theme switching
- **Notification System**: Build completion and error notifications

---

## Quick Start

### Create Your First MOD
1. Install the application  
2. Download from the [Release page](https://github.com/ArjunLee/FMMxMod-Creator/releases):  
   - `Demo Projects - MOD Source Files.7z`  
   - `Demo Projects - MOD build record.zip`  
3. Import build records from `MOD Repository → Import Records → Demo Projects - MOD build record.zip`  
4. Extract `Demo Projects - MOD Source Files.7z`  
5. Restore the workspace layout from `MOD Repository` to begin creating MODs.

### Detailed Tutorial Manuals

We provide detailed tutorial manuals for users of different languages:

- 📚 [中文教学手册](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/eqg0qcvzd05g3dy4) 🇨🇳
- 📚 [English Tutorial Manual](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/qh3km88g2ma10pi5) 🇺🇸
- 📚 [日本語チュートリアル](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/ff8wzvahd1ni7397) 🇯🇵
- 📚 [한국어 튜토리얼](https://www.yuque.com/lilaoshi-c4hmh/esrvuh/bx9w5a6ua3mgr29q) 🇰🇷

---

## 📸 Screenshots

<div align="center">

![Main Interface Screenshot](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_05-09-52.png)

![MOD Repository Screenshot](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_05-11-36.png)

![Settings Page Screenshot](https://github.com/ArjunLee/FMMxMod-Creator/blob/main/Other/image/PixPin_2025-07-18_05-12-32.png)

</div>

---

## App Feature Showcase

Video: https://www.bilibili.com/video/BV1ZFgGzTEGY/

---

## Showcase

Here are real MOD cases created with this tool and published on Nexusmods:

<div align="center">

### 🎮 Case 1: NieR 2B Uniform Mod
**FMM_FOMOD-YoRHa_No.2_Type_B_Uniform-Modular-CN_EN**

[![Nexusmods Link](https://img.shields.io/badge/Nexusmods-View%20MOD-orange?style=for-the-badge&logo=nexusmods)](https://www.nexusmods.com/stellarblade/mods/904)

### 🎮 Case 2: NieR Unofficial Ceremonial Attire Mod
**FMM_FOMOD-YoRHa Unofficial Ceremonial Attire - Modular - CN_EN**

[![Nexusmods Link](https://img.shields.io/badge/Nexusmods-View%20MOD-orange?style=for-the-badge&logo=nexusmods)](https://www.nexusmods.com/stellarblade/mods/990)

</div>

*These MODs demonstrate the tool's capability in creating complex, modular MODs.*

---

### Tech Stack

| Technology | Version | Purpose |
|------------|---------|----------|
| **Python** | 3.13+ | Main development language |
| **PySide6** | Latest | Python bindings for Qt6, providing modern GUI |
| **PySide6-Fluent-Widgets** | Latest | Fluent Design style UI component library |
| **py7zr** | Latest | 7z compression file handling |
| **rarfile** | Latest | RAR file handling |
| **Nuitka** | Latest | Python code compilation and packaging |

### About Building

We provide automated `Nuitka` packaging solutions. You can choose different options based on your needs:

```bash
# Recommended: Standalone packaging (faster startup)
Build_Solution\build_standalone_data.bat
# Or use Python script
python Build_Solution\build_nuitka-standalone_data.py

# Single file option (easier distribution)
Build_Solution\build_single_exe.bat
# Or use Python script
python Build_Solution\build_nuitka-single_exe.py

# Legacy build method (deprecated)
build.bat
```

✅ After packaging is complete, the executable file will be generated in the `dist` directory.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Issue Reporting

If you encounter any problems or have feature suggestions, please contact us through the following channels:

- 🐛 [Issues Page](https://github.com/ArjunLee/FMMxMod-Creator/issues) - Report bugs and feature requests
- 💬 [Discussions Page](https://github.com/ArjunLee/FMMxMod-Creator/discussions) - Community discussions and exchanges
- 📧 [Contact Me](mailto:shin3sango@qq.com) - Email

---

## ☕ Buy Me a Coffee

If this project helps you, consider buying me a coffee to support development! ☕

<div align="center">

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/H2H51HJEYI)

*Your support is my motivation for continuous development!* 💪

</div>

---

<div align="center">

*Made with ❤️ by [ArjunLee](https://github.com/ArjunLee)*

</div>

---

## 📁 Project Structure

```
FMMxMod-Creator/
├── 📄 .gitignore                          # Git ignore file configuration
├── 📁 Build_Solution/                     # 🔨 Build solution directory
│   ├── 📋 BUILD_SYSTEM_README.md          # Build system overview
│   ├── 📋 PACKAGING_GUIDE.md              # Detailed packaging solution comparison
│   ├── 📋 STANDALONE_BUILD_GUIDE.md       # Standalone build guide
│   ├── 📋 DIST_README_STANDALONE.md       # Standalone distribution instructions
│   ├── 🔧 build_single_exe.bat           # Single file build script
│   ├── 🔧 build_standalone_data.bat       # Standalone build script
│   ├── 🐍 build_nuitka-single_exe.py     # Single file Python script
│   ├── 🐍 build_nuitka-standalone_data.py # Standalone Python script
│   ├── 🐍 test_build_config.py           # Build configuration test
│   ├── 🐍 update_build_version.py         # Version update tool
│   └── ⚙️ pyproject.toml                  # Project configuration file
├── 📦 FMMxMOD-Creator_build-record-*.zip  # Example build records
├── 📄 LICENSE                             # MIT open source license
├── 📄 README_CN.md                        # Chinese documentation
├── 📄 README.md                           # English documentation
├── 📁 app/                                # 🏠 Main application directory
│   ├── 📁 Resources/                      # 🎨 Resource files directory
│   │   ├── 🎬 Drag_and_Drop_Example_Video.gif # Drag and drop example animation
│   │   ├── 🎬 modlist_editing_tips.gif    # Editing tips animation
│   │   ├── 🖼️ FMMxModCreator_Icon.ico     # Application icon
│   │   ├── 🖼️ FMMxModCreator_Icon_512.png # High-resolution application icon
│   │   ├── 🎨 Drag_and_drop_black.svg     # Drag and drop icon (black)
│   │   ├── 🎨 Drag_and_drop_white.svg     # Drag and drop icon (white)
│   │   ├── 🎨 Edit_black.svg              # Edit icon (black)
│   │   ├── 🎨 Edit_white.svg              # Edit icon (white)
│   │   └── 📁 qss/                        # Stylesheet files
│   ├── 📄 __init__.py                     # Package initialization file
│   ├── 📁 common/                         # 🔧 Common modules
│   │   ├── 📄 __init__.py                 # Package initialization
│   │   ├── 🏠 application.py              # Main application class
│   │   ├── ⚙️ config.py                   # Configuration management
│   │   ├── 🔧 config_utils.py             # Configuration utility functions
│   │   ├── 🌍 language.py                 # Multi-language support
│   │   └── ℹ️ version_info.py             # Version information
│   ├── 📁 components/                     # 🧩 UI components
│   │   ├── 📄 __init__.py                 # Package initialization
│   │   ├── ➕ add_function_card.py        # Add function card
│   │   ├── 🛡️ cover_block.py              # Cover block
│   │   ├── 💬 edit_tips_dialog.py         # Edit tips dialog
│   │   ├── 📁 file_display_widget.py      # File display widget
│   │   ├── 🎈 floating_menu_button.py     # Floating menu button
│   │   ├── 📦 mod_file_block.py           # MOD file block
│   │   ├── 🎴 mod_info_card.py            # MOD info card
│   │   ├── 📊 mod_table_widget.py         # MOD table widget
│   │   ├── ➖ separator_block.py           # Separator block
│   │   └── ⚠️ warning_block.py            # Warning block
│   ├── 📁 config/                         # ⚙️ Configuration files
│   │   ├── 🔧 app_config.json             # Application configuration
│   │   └── 📋 mod_list_table_config.json  # MOD list table configuration
│   ├── 📁 service/                        # 🔧 Business logic services
│   │   ├── 💾 build_record_service.py     # Build record service
│   │   ├── 🔨 build_service.py            # Build service
│   │   └── 🔄 restore_service.py          # Restore service
│   └── 📁 view/                           # 🖼️ Interface views
│       ├── 📄 __init__.py                 # Package initialization
│       ├── 🏠 home_interface.py           # Home interface
│       ├── 🖼️ main_window.py              # Main window
│       ├── 📋 mod_list_interface.py       # MOD list interface
│       └── ⚙️ settings_interface.py       # Settings interface
├── 📁 config/                             # 🌐 Global configuration
│   └── ⚙️ config.json                     # Global configuration file
├── 🚀 main.py                             # Application entry point
├── 🖼️ png2ico.py                          # PNG to ICO converter tool
├── 📋 requirements.txt                    # Python dependencies list
└── 📦 测试错误的构建配置文件导入.zip        # Test file
```