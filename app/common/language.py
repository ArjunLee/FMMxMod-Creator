# coding:utf-8
"""
Language Manager
语言管理模块
"""

from PySide6.QtCore import QObject, Signal, QLocale
from . import version_info
from typing import Dict, Any
import locale


class LanguageManager(QObject):
    """语言管理器"""
    languageChanged = Signal()  # language change signal
    
    def __init__(self):
        super().__init__()
        self.current_language = "zh_CN"
        self.translations = {
            # 简体中文
            "zh_CN": {
                # 主窗口
                "main_window_title": "FMM x MOD 创作者",
                "home": "首屏",
                "mod_list": "MOD 府库",
                "settings": "规设",
                
                # 主页 - 区块1
                "mod_info": "MOD 信息",
                "mod_name": "MOD 名称",
                "mod_name_desc": "烦请键入欲制 MOD 之名",
                "mod_name_placeholder": "留意：FMM 仅纳英文之名",
                "version": "版本号",
                "version_desc": "烦请录入此 MOD 之版本编号",
                "version_placeholder": "楷式：1.0.0，\"v\"无需录入",
                "author": "作者信息",
                "author_desc": "烦请书作者之名",
                "author_placeholder": "留意：FMM 仅纳英文之名",
                "mod_category": "MOD 类别",
                "mod_category_desc": "烦请择定此 MOD 所隶类目",
                "mod_category_placeholder": "留意：FMM 仅纳英文之名",
                
                # 主页 - 区块2
                "add_function": "添设功能",
                "add_function_desc": "点击右侧按钮，可添诸般不同组件",
                "add_cover": "添设封面",
                "add_warning": "添设警告",
                "add_separator": "添设分割线",
                "add_mod_files": "添设MOD文件",
                
                # MOD列表界面
                "import_record": "导入记录",
                "backup_record": "备份记录",
                "backup_record_success_title": "幸甚至哉",
                "backup_record_success_content": "文档存于 {path}",
                "backup_record_failed_title": "悲夫哀哉",
                "backup_record_failed_content": "何故: {error}",
                "import_success_title": "幸甚至哉",
                "import_success_content": "顺遂复还",
                "import_failed_title": "悲夫哀哉",
                "import_failed": "找不到 FMM x Mod Creator 的创建记录",
                "import_error": "复还未济: {error}",
                "import_mod": "导入",
                "edit_mode": "编辑",
                "revise_again": "再度编撰",
                "restore_success_title": "幸甚至哉",
                "restore_success_content": "文档复还告成",
                "restore_failed_title": "悲夫哀哉",
                "restore_failed_content": "复还未济: {error}",
                "home_interface_not_set": "主页界面未设置",
                "delete_record": "自府库削除",
                "operations": "操作",
                "sort_mod": "排序",
                "sort_by_name": "MOD名称",
                "sort_by_author": "作者",
                "sort_by_category": "分类",
                "sort_by_date": "创建日期",
                "sort_ascending": "升序",
                "sort_descending": "降序",
                "no_mod_hint": "此境未启，寂寥如也；且赴首屏，肇建新篇。",
                "serial_number": "序号",
                "cover_image": "封面图",
                "operations": "操作",
                "refresh": "刷新",
                "no_cover": "无封面",
                "category": "分类",
                "create_date": "创建日期",
                "delete_mod_record_title": "削除 MOD 肇建纪载",
                "delete_mod_record_content": "君决意削除 {mod_name} 乎？此举覆水不回。",
                "refresh_success": "府库文档更新告成。",
                "refresh_failed": "刷新失败: {error}",
                "error": "错误",
                
                # 编辑提示
                "edit_tips_title": "直接编纂文字",
                "edit_tips_content": "轻点编辑按钮后，君可双击单元格，直接对数据进行编纂。",
                "edit_tips_got_it": "了然",
                "edit_tips_dont_show": "毋须再提",
                
                # 拖拽排序技巧
                "sorting_tips": "列序妙法",
                "drag_and_drop_sorting_tips_title": "拖拽排序技巧",
                "drag_and_drop_sorting_tips_content": "诸君可按住拖曳之钮，以行区块排序之事，调弦理丝，拨转有序。",
                
                # 封面区块
                "cover_area": "封面区块",
                "cover_area_desc": "烦请上传封面图",
                "cover_upload": "封面上传",
                "cover_upload_desc": "烦请上传封面图",
                "cover_description_placeholder": "烦请书封面之注语",
                "click_to_upload": "烦请上传一幅图像，以达封面之意",
                "select_image": "选择图片",
                "delete_cover_block": "删除封面区块",
                "cover_exists_title": "既有封面存焉",
                "cover_exists_content": "FMM 仅可设单张封面之像。烦请先除现有封皮，方可另行操持。",
                
                # 警告区块
                "warning_area": "警告区块",
                "warning_area_desc": "告诫诸君，欲装汝之MOD，有何事宜须谨慎",
                "warning_upload_hint": "宜上传一幅图像，以明所需留意之诸般事宜",
                "warning_description_placeholder": "烦请录入警示之辞。留意：FMM 仅纳英文之名",
                "move_warning_block": "移动警告区块",
                "copy_warning_block": "复制警告区块",
                "delete_warning_block": "删除警告区块",
                "clear_image": "清除图片",
                "drag_to_move_block": "拖拽移动区块",
                "collapse_expand": "折叠/展开",
                "area_mark": "标记(可选)",
                "block_mark_placeholder": "区块标记",
                
                # 分割线区块
                "separator_area": "分割线区块",
                "separator_area_desc": "用于在MOD中添加分割线，便于内容分组",
                "separator_name_placeholder": "隔线之名",
                "copy_separator_block": "复制分割线区块",
                "delete_separator_block": "删除分割线区块",
                
                # MOD文件区块
                "mod_file_area": "文件区块",
                "mod_file_area_desc": "典藏 MOD 文件之府库",
                "module_name": "模块名称",
                "module_name_desc": "烦请键入模块之名",
                "module_name_placeholder": "烦请书录模块之名",
                "mod_file_upload_hint": "烦请上传一幅图像，以明此模块之用",
                "mod_file_description_placeholder": "烦请书此 MOD 模块之释解",
                "add_files": "加诸文档",
                "add_folders": "加诸文档夹",
                "move_mod_file_block": "移动文件区块",
                "copy_mod_file_block": "复制文件区块",
                "delete_mod_file_block": "删除文件区块",
                "select_files": "选择文件",
                "select_folders": "选择文件夹",
                "remove_file": "移除文件",
                
                # 文件展示区块
                "rename": "易其名",
                "delete": "剔出簿册",
                "open_file_location": "启文件之所",
                "rename_dialog_title": "易其名",
                "rename_dialog_content": "烦请键入新名：",
                "rename_placeholder": "请输入新的文件/文件夹名称",
                "name_cannot_be_empty": "名称不得为空",
                "name_unchanged": "名称未曾更易",
                "file_display_area": "文件/文件夹簿册",
                "confirm": "允",
                "cancel": "罢",
                "no_files_selected": "尚无文件择选，可经由左上角按钮，录入文件或文件夹",
                
                # 设置页面
                "personalization": "个性化",
                "build_settings": "构筑设置",
                "build_directory": "构筑府库",
                "build_directory_desc": "于右方择取输出之府库",
                "build_cache": "构筑缓存",
                "build_cache_desc": "",  # 将显示实际路径
                "choose_folder": "择取府库",
                "build_type": "构筑类型",
                "build_type_desc": "选择被打包的格式",
                "theme_setting": "主题设置",
                "theme_mode": "玄明流转",
                "theme_mode_desc": "调整应用程序的外观",
                "language_setting": "言枢四译",
                "language_desc": "选择应用程序的显示语言",
                "mica_effect": "云母侵染",
                "mica_effect_desc": "启用窗口和材质的半透明效果",
                "theme_color": "丹青焕斓",
                "theme_color_desc": "选择应用程序的主题颜色",
                "theme_color_turquoise": "🎨绿松石",
                "theme_color_camellia": "🎨茶花红",
                "theme_color_cloisonne": "🎨景泰蓝",
                "theme_color_wheat": "🎨麦桔黄",
                "theme_color_vitriol": "🎨青矾绿",
                "theme_color_primrose": "🎨樱草紫",
                "theme_color_lotus": "🎨莲瓣白",
                "theme_color_dark": "🎨玄色",
                
                # 深色模式主题色
                "dark_bichun_green": "碧春绿",
                "dark_haitang_red": "海棠红",
                "dark_jingtai_blue": "景泰蓝",
                "dark_wheat_yellow": "麦桔黄",
                "dark_qinglian_purple": "青莲紫",
                "dark_lotus_white": "莲瓣白",
                
                # 浅色模式主题色
                "light_camellia_red": "茶花红",
                "light_gem_blue": "宝石蓝",
                "light_cangshan_yellow": "苍山黄",
                "light_mint_green": "薄荷绿",
                "light_lilac_purple": "丁香紫",
                "light_xuandai_black": "玄黛黑",
                "check_update": "检查更新",
                "auto": "跟随系统",
                "light": "浅色",
                "dark": "深色",
                "chinese": "中文",
                "english": "English",
                "japanese": "日本語",
                "korean": "한국어",
                "follow_system": "Follow System",
                "language_changed_to_chinese": "Success",
                "language_changed_to_english": "Success",
                "restart_required_chinese": "Language switched successfully",
                "restart_required_english": "The language has been successfully switched",
                "japanese": "日本語",
                "korean": "한국어",
                "follow_system": "跟随系统",
                "language_changed_to_chinese": "幸甚至哉",
                "language_changed_to_english": "Success",
                "restart_required_chinese": "言枢已焕",
                "restart_required_english": "The language has been successfully switched",
                "update_error_title": "惜哉",
                "update_error_content": "此功能在当前版本未启用",
                
                # 关于页面
                "about": "关于",
                "help": "帮助",
                "help_desc": "获取使用帮助和支持",
                "about_app": "关于 FMM x Mod 创作者",
                "about_app_desc": "查看应用程序信息",
                "app_version": f"版本 {version_info.VERSION_STRING}",
                "app_description": "一个用于创建 FMM MOD 的工具",
                "developer": f"肇建 · {version_info.APP_AUTHOR} | Version {version_info.VERSION_STRING}",
                "copyright": "© 2025 FMM x Mod Creator. All rights reserved.",
                
                # 浮层菜单按钮
                "build_zip": "构筑MOD",
                "start_build": "开始构筑",
                "clear_all_area": "区块净除",
                
                # 构建相关
                "build_success_title": "幸甚至哉",
                "build_success_content": "MOD 已然告成构筑，输出于",
                "build_failed_title": "悲夫哀哉",
                "build_failed_content": "MOD 构筑之际，舛误乍现",
                "build_success": "幸甚至哉",
                "build_failed": "悲夫哀哉",
                "mod_name_required": "MOD名称 不可阙如",
                "version_required": "版本号 不可阙如",
                "author_required": "作者信息 不可阙如",
                "category_required": "MOD类别 不可阙如",
                "cover_block_required": "至少当增一封面区块",
                "cover_image_not_found": "封面图像之文件未存",
                "content_block_required": "至少当增一文件区块",
                "file_not_found": "文件未存于府库",
                "creating_temp_dir": "方构临时之府库",
                "creating_cover_folder": "正建封面之府库",
                "creating_block_folders": "正建区块之府库",
                "creating_archive_file": "正造压缩之文件",
                "moving_to_output": "正徙于输出之府库",
                "build_completed": "构筑完成，幸甚至哉",
                "cover_data_missing": "封面之数据阙如"
            },
            # 英文
            "en": {
                # Main Window
                "main_window_title": "FMM x Mod Creator",
                "home": "Home",
                "mod_list": "MOD List",
                "settings": "Settings",
                
                # Home - Block 1
                "mod_info": "Mod Info",
                "mod_name": "MOD Name",
                "mod_name_desc": "Please enter the name of the mod",
                "mod_name_placeholder": "Please enter the mod name, note: FMM only supports English",
                "version": "Version",
                "version_desc": "Please enter the version number of the mod",
                "version_placeholder": "For example, 1.0.0, no need to input \"v\"",
                "author": "Author",
                "author_desc": "Please enter the author's name",
                "author_placeholder": "Note: that FMM only supports English.",
                "mod_category": "Mod Category",
                "mod_category_desc": "Please select the category to which the mod belongs",
                "mod_category_placeholder": "Note: that FMM only supports English.",
                
                # Home - Block 2
                "add_function": "Add Function",
                "add_function_desc": "Click buttons to add different types of MOD components",
                "add_cover": "Add Cover",
                "add_warning": "Add Warning",
                "add_separator": "Add Separator",
                "add_mod_files": "Add Mod Files",
                
                # MOD List Interface
                "import_record": "Import Record",
                "backup_record": "Backup Record",
                "backup_record_success_title": "Backup successful",
                "backup_record_success_content": "File located at {path}",
                "backup_record_failed_title": "Backup failed",
                "backup_record_failed_content": "Reason: {error}",
                "import_success_title": "Import successful",
                "import_success_content": "FMM x Mod Creator build record imported successfully",
                "import_failed_title": "Import failed",
                "import_failed": "FMM x Mod Creator build record not found",
                "import_error": "Reason: {error}",
                "import_mod": "Import",
                "edit_mode": "Edit",
                "revise_again": "Revise again",
                "restore_success_title": "Restore successful",
                "restore_success_content": "Workspace layout restored successfully",
                "restore_failed_title": "Restore failed",
                "restore_failed_content": "Reason: {error}",
                "home_interface_not_set": "Home interface not set",
                "delete_record": "Delete record",
                "operations": "Operations",
                "sort_mod": "Sort",
                "sort_by_name": "MOD Name",
                "sort_by_author": "Author",
                "sort_by_category": "Category",
                "sort_by_date": "Creation Date",
                "sort_ascending": "Ascending",
                "sort_descending": "Descending",
                "no_mod_hint": "No MOD build records found. Go create your first MOD! Great!",
                "serial_number": "No.",
                "cover_image": "Cover Image",
                "operations": "Operations",
                "refresh": "Refresh",
                "no_cover": "No Cover",
                "category": "Category",
                "create_date": "Creation Date",
                "delete_mod_record_title": "Delete MOD Creation Record",
                "delete_mod_record_content": "Are you sure you want to delete {mod_name}? This action cannot be undone.",
                "refresh_success": "Data refreshed",
                "refresh_failed": "Refresh failed: {error}",
                "error": "Error",
                
                # Edit Tips
                "edit_tips_title": "Direct Text Editing",
                "edit_tips_content": "After clicking the edit button, you can double-click on cells to directly edit the data.",
                "edit_tips_got_it": "Got it",
                "edit_tips_dont_show": "Don't show again",
                
                # Drag and Drop Sorting Tips
                "sorting_tips": "Sorting Tips",
                "drag_and_drop_sorting_tips_title": "Drag-and-Drop Sorting Tips",
                "drag_and_drop_sorting_tips_content": "You can reorder blocks by holding down the drag button.",
                
                # Cover Block
                "cover_area": "Cover Area",
                "cover_area_desc": "Please upload the cover image",
                "cover_upload": "Cover Upload",
                "cover_upload_desc": "Please upload the cover image",
                "cover_description_placeholder": "Please enter the description on the cover",
                "click_to_upload": "Click to upload",
                "select_image": "Select Image",
                "delete_cover_block": "Delete Cover Block",
                "cover_exists_title": "Cover already exists",
                "cover_exists_content": "FMM only supports setting one cover. Please delete the existing cover first.",
                
                # Warning Block
                "warning_area": "Warning Area",
                "warning_area_desc": "Used to remind users what to pay attention to when installing your mod",
                "warning_upload_hint": "Upload a picture to explain the precautions to the user",
                "warning_description_placeholder": "Please enter the warning description, note: FMM only supports English",
                "move_warning_block": "Move Warning Block",
                "copy_warning_block": "Copy Warning Block",
                "delete_warning_block": "Delete Warning Block",
                "clear_image": "Clear Image",
                "drag_to_move_block": "Drag to Move Block",
                "collapse_expand": "Collapse/Expand",
                "area_mark": "Mark(optional)",
                "block_mark_placeholder": "Block mark",
                
                # Separator Block
                "separator_area": "Separator Area",
                "separator_area_desc": "Used to add separators in MOD for content grouping",
                "separator_name_placeholder": "Separator name",
                "copy_separator_block": "Copy Separator Block",
                "delete_separator_block": "Delete Separator Block",
                
                # MOD File Block
                "mod_file_area": "Files Area",
                "mod_file_area_desc": "Repository for storing MOD files",
                "module_name": "Module name",
                "module_name_desc": "Please enter the name of the mod module",
                "module_name_placeholder": "Please enter the name of the module",
                "mod_file_upload_hint": "Upload a picture to explain this module",
                "mod_file_description_placeholder": "Please enter a description for this mod module",
                "add_files": "Add Files",
                "add_folders": "Add Folders",
                "move_mod_file_block": "Move Mod File Block",
                "copy_mod_file_block": "Copy Mod File Block",
                "delete_mod_file_block": "Delete Mod File Block",
                "select_files": "Select Files",
                "select_folders": "Select Folders",
                "remove_file": "Remove File",
                
                # File Display Block
                "rename": "Rename",
                "delete": "Delete",
                "open_file_location": "Open File Location",
                "rename_dialog_title": "Rename",
                "rename_dialog_content": "Please enter new name:",
                "rename_placeholder": "Please enter new file/folder name",
                "name_cannot_be_empty": "Name cannot be empty",
                "name_unchanged": "Name unchanged",
                "file_display_area": "File/Folder Display Area",
                "confirm": "OK",
                "cancel": "Cancel",
                "no_files_selected": "No file selected, please add a file or folder using the button in the upper left corner",
                
                # Settings page
                "personalization": "Personalization",
                "build_settings": "Build Settings",
                "build_directory": "Build Directory",
                "build_directory_desc": "Select the output folder on the right",
                "build_cache": "Build cache",
                "build_cache_desc": "",  # 将显示实际路径
                "choose_folder": "Select folder",
                "build_type": "Build Type",
                "build_type_desc": "Select the packaging format",
                "theme_setting": "Theme Settings",
                "theme_mode": "Theme Mode",
                "theme_mode_desc": "Change the application theme",
                "language_setting": "Language Settings",
                "language_desc": "Change the application language",
                "mica_effect": "Mica Effect",
                "mica_effect_desc": "Enable translucent effects for windows and materials",

                "theme_color": "Theme Color",
                "theme_color_desc": "Adjust the theme color of the application",
                "theme_color_turquoise": "Turquoise",
                "theme_color_camellia": "Camellia",
                "theme_color_cloisonne": "Cloisonne",
                "theme_color_wheat": "Wheat",
                "theme_color_vitriol": "Vitriol",
                "theme_color_primrose": "Primrose",
                "theme_color_lotus": "Lotus",
                "theme_color_dark": "Dark",
                
                # Dark mode theme colors
                "dark_bichun_green": "Spring Green",
                "dark_haitang_red": "Begonia Red",
                "dark_jingtai_blue": "Cloisonne Blue",
                "dark_wheat_yellow": "Wheat Yellow",
                "dark_qinglian_purple": "Lotus Purple",
                "dark_lotus_white": "Lotus White",
                
                # Light mode theme colors
                "light_camellia_red": "Camellia Red",
                "light_gem_blue": "Gem Blue",
                "light_cangshan_yellow": "Mountain Yellow",
                "light_mint_green": "Mint Green",
                "light_lilac_purple": "Lilac Purple",
                "light_xuandai_black": "Ink Black",
                "check_update": "Check Update",
                "auto": "Auto",
                "light": "Light",
                "dark": "Dark",
                "chinese": "中文",
                "english": "English",
                "japanese": "日本語",
                "korean": "한국어",
                "follow_system": "Follow System",
                
                # About Page
                "about": "About",
                "help": "Help",
                "help_desc": "Discover new features and learn tips about FMM xCreator",
                "about_app": "About FMM x Mod Creator",
                "about_app_desc": "Version information and developer information",
                "app_version": f"Version {version_info.VERSION_STRING}",
                "app_description": "A tool for creating FMM MODs",
                "developer": f"Developer · {version_info.APP_AUTHOR} | Version {version_info.VERSION_STRING}",
                "copyright": "© 2025 FMM x Mod Creator. All rights reserved.",
                "update_error_title": "Error",
                "update_error_content": "This feature is not enabled in the current version",
                
                # 浮层菜单按钮
                "build_zip": "Build ZIP",
                "start_build": "Start build",
                "clear_all_area": "Clear all Area",
                
                # Build related
                "build_success_title": "Build Success",
                "build_success_content": "MOD has been successfully built, output path",
                "build_failed_title": "Build Failed",
                "build_failed_content": "An error occurred during MOD building",
                "build_success": "Build Successful",
                "build_failed": "Build Failed",
                "mod_name_required": "MOD name cannot be empty",
                "version_required": "Version number cannot be empty",
                "author_required": "Author information cannot be empty",
                "category_required": "MOD category cannot be empty",
                "cover_block_required": "Please add at least one cover block",
                "cover_image_not_found": "Cover image file not found",
                "content_block_required": "Please add at least one content block",
                "file_not_found": "File not found",
                "creating_temp_dir": "Creating temporary directory",
                "creating_cover_folder": "Creating cover folder",
                "creating_block_folders": "Creating block folders",
                "creating_archive_file": "Creating archive file",
                "moving_to_output": "Moving to output directory",
                "build_completed": "Build completed",
                "cover_data_missing": "Cover data missing"
            },
            # 日语
            "ja_JP": {
                # メインウィンドウ
                "main_window_title": "FMM x MOD クリエイター",
                "home": "ホーム",
                "mod_list": "MOD リスト",
                "settings": "設定",

                # ホーム - ブロック1
                "mod_info": "MOD 情報",
                "mod_name": "MOD 名称",
                "mod_name_desc": "MODの名称を入力してください",
                "mod_name_placeholder": "注意：FMM は英語のみ対応",
                "version": "バージョン番号",
                "version_desc": "MODのバージョン番号を入力",
                "version_placeholder": "例：1.0.0 (\"v\"の入力不要)",
                "author": "作者情報",
                "author_desc": "MOD作者名を入力",
                "author_placeholder": "注意：FMM は英語のみ対応",
                "mod_category": "MOD カテゴリ",
                "mod_category_desc": "MODの分類を入力",
                "mod_category_placeholder": "注意：FMM は英語のみ対応",

                # ホーム - ブロック2
                "add_function": "機能追加",
                "add_function_desc": "右側ボタンで各種機能コンポーネントを追加",
                "add_cover": "カバー追加",
                "add_warning": "警告追加",
                "add_separator": "区切り線追加",
                "add_mod_files": "MODファイル追加",

                # MODリストインターフェース
                "import_record": "インポート記録",
                "backup_record": "バックアップ記録",
                "backup_record_success_title": "バックアップ成功",
                "backup_record_success_content": "ファイルの場所: {path}",
                "backup_record_failed_title": "バックアップ失敗",
                "backup_record_failed_content": "原因: {error}",
                "import_success_title": "インポート成功",
                "import_success_content": "FMM x Mod Creator作成記録をインポートしました",
                "import_failed_title": "インポート失敗",
                "import_failed": "FMM x Mod Creatorの作成記録が見つかりません",
                "import_error": "原因: {error}",
                "import_mod": "インポート",
                "edit_mode": "編集",
                "revise_again": "再度修正",
                "restore_success_title": "復元成功",
                "restore_success_content": "作業レイアウトの復元に成功しました",
                "restore_failed_title": "復元失敗",
                "restore_failed_content": "原因: {error}",
                "home_interface_not_set": "ホームインターフェイス未設定",
                "delete_record": "記録を削除する",
                "operations": "操作",
                "sort_mod": "ソート",
                "sort_by_name": "MOD名称",
                "sort_by_author": "作者",
                "sort_by_category": "カテゴリ",
                "sort_by_date": "作成日",
                "sort_ascending": "昇順",
                "sort_descending": "降順",
                "no_mod_hint": "MODビルド記録がありません。最初のMODを作成しましょう！Great！",
                "serial_number": "No.",
                "cover_image": "カバー画像",
                "operations": "操作",
                "refresh": "更新",
                "no_cover": "カバーなし",
                "category": "カテゴリ",
                "create_date": "作成日",
                "delete_mod_record_title": "MOD作成記録の削除",
                "delete_mod_record_content": "{mod_name} を削除しますか？この操作は取り消せません。",
                "refresh_success": "データが更新されました",
                "refresh_failed": "更新に失敗しました: {error}",
                "error": "エラー",
                
                # 編集ヒント
                "edit_tips_title": "直接テキスト編集",
                "edit_tips_content": "編集ボタンをクリックした後、セルをダブルクリックしてデータを直接編集できます。",
                "edit_tips_got_it": "了解しました",
                "edit_tips_dont_show": "今後表示しない",

                # ドラッグ＆ドロップソート
                "sorting_tips": "ソート技法",
                "drag_and_drop_sorting_tips_title": "ドラッグソート技法",
                "drag_and_drop_sorting_tips_content": "コンポーネントを左クリックで保持し、新しい位置へ移動",

                # カバーブロック
                "cover_area": "カバー領域",
                "cover_area_desc": "カバー画像をアップロード",
                "cover_upload": "カバーアップロード",
                "cover_upload_desc": "カバー画像をアップロード",
                "cover_description_placeholder": "カバーの説明文を入力",
                "click_to_upload": "画像をアップロード (MOD説明用)",
                "select_image": "画像選択",
                "delete_cover_block": "カバーブロック削除",
                "cover_exists_title": "カバーブロックが存在",
                "cover_exists_content": "FMM は1枚のカバーのみ表示可能。既存のカバーブロックを削除してください。",

                # 警告ブロック
                "warning_area": "警告領域",
                "warning_area_desc": "MODインストール時の注意事項をユーザーに通知",
                "warning_upload_hint": "注意事項説明用画像をアップロード",
                "warning_description_placeholder": "警告説明を入力 (注意：FMM は英語のみ対応)",
                "move_warning_block": "警告ブロック移動",
                "copy_warning_block": "警告ブロック複製",
                "delete_warning_block": "警告ブロック削除",
                "clear_image": "画像消去",
                "drag_to_move_block": "ドラッグで移動",
                "collapse_expand": "折り畳み/展開",
                "area_mark": "マーク(optional)",
                "block_mark_placeholder": "ブロックマーク",

                # 区切り線ブロック
                "separator_area": "区切り線領域",
                "separator_area_desc": "MOD内のコンテンツ分類用区切り線",
                "separator_name_placeholder": "区切り線名称",
                "copy_separator_block": "区切り線複製",
                "delete_separator_block": "区切り線削除",

                # MODファイルブロック
                "mod_file_area": "ファイル領域",
                "mod_file_area_desc": "MODファイル保管庫",
                "module_name": "モジュール名",
                "module_name_desc": "モジュール名称を入力",
                "module_name_placeholder": "モジュール名を入力",
                "mod_file_upload_hint": "モジュール機能説明用画像をアップロード",
                "mod_file_description_placeholder": "MODモジュールの説明を入力",
                "add_files": "Add File",
                "add_folders": "Add Folder",
                "move_mod_file_block": "ファイルブロック移動",
                "copy_mod_file_block": "ファイルブロック複製",
                "delete_mod_file_block": "ファイルブロック削除",
                "select_files": "ファイル選択",
                "select_folders": "フォルダ選択",
                "remove_file": "ファイル削除",

                # ファイル表示領域
                "rename": "名称変更",
                "delete": "リストから削除",
                "open_file_location": "保存場所を開く",
                "rename_dialog_title": "名称変更",
                "rename_dialog_content": "新しい名称を入力：",
                "rename_placeholder": "ファイル/フォルダの新名称",
                "name_cannot_be_empty": "名称が空です",
                "name_unchanged": "名称変更なし",
                "file_display_area": "ファイル/フォルダ表示領域",
                "confirm": "確定",
                "cancel": "キャンセル",
                "no_files_selected": "ファイル未選択。左上ボタンで新規追加可能",

                # 設定ページ
                "personalization": "カスタマイズ",
                "build_settings": "ビルド設定",
                "build_directory": "ビルドディレクトリ",
                "build_directory_desc": "右側で出力フォルダを選択してください",
                "build_cache": "キャッシュの構築",
                "build_cache_desc": "",  # 将显示实际路径
                "choose_folder": "フォルダを選択",
                "build_type": "ビルドタイプ",
                "build_type_desc": "パッケージ形式を選択",
                "theme_setting": "テーマ設定",
                "theme_mode": "テーマモード",
                "theme_mode_desc": "アプリケーション外観を調整",
                "language_setting": "言語設定",
                "language_desc": "表示言語を選択",
                "mica_effect": "マイカ効果",
                "mica_effect_desc": "ウィンドウと素材の半透明効果を有効にする",

                "theme_color": "テーマカラー",
                "theme_color_desc": "アプリケーションの配色を選択",
                "theme_color_turquoise": "🎨ターコイズ",
                "theme_color_camellia": "🎨カメリアレッド",
                "theme_color_cloisonne": "🎨七宝焼ブルー",
                "theme_color_wheat": "🎨小麦色",
                "theme_color_vitriol": "🎨緑礬緑",
                "theme_color_primrose": "🎨桜草紫",
                "theme_color_lotus": "🎨蓮の白",
                "theme_color_dark": "🎨玄色",

                # ダークモードテーマカラー
                "dark_bichun_green": "碧春緑",
                "dark_haitang_red": "海棠紅",
                "dark_jingtai_blue": "景泰藍",
                "dark_wheat_yellow": "小麦黄",
                "dark_qinglian_purple": "青蓮紫",
                "dark_lotus_white": "蓮弁白",

                # ライトモードテーマカラー
                "light_camellia_red": "椿赤",
                "light_gem_blue": "宝石青",
                "light_cangshan_yellow": "蒼山黄",
                "light_mint_green": "薄荷緑",
                "light_lilac_purple": "ライラック紫",
                "light_xuandai_black": "玄黛黒",
                "check_update": "更新確認",
                "auto": "システム準拠",
                "light": "ライト",
                "dark": "ダーク",
                "chinese": "中国語",
                "english": "英語",
                "japanese": "日本語",
                "korean": "韓国語",
                "follow_system": "システムに従う",
                "language_changed_to_chinese": "中国語に切替成功",
                "language_changed_to_english": "英語切替成功",
                "restart_required_chinese": "言語切替完了",
                "restart_required_english": "言語切替が正常に完了しました",
                "update_error_title": "失敗",
                "update_error_content": "当バージョンでは本機能を利用できません",

                # アバウトページ
                "about": "情報",
                "help": "ヘルプ",
                "help_desc": "サポート情報を取得",
                "about_app": "FMM x MOD クリエイターについて",
                "about_app_desc": "アプリケーション情報",
                "app_version": f"バージョン {version_info.VERSION_STRING}",
                "app_description": "FMM MOD作成ツール",
                "developer": f"開発者 · {version_info.APP_AUTHOR} | Version {version_info.VERSION_STRING}",
                "copyright": "© 2025 FMM x Mod Creator. All rights reserved.",

                # フローティングメニュー
                "build_zip": "ZIPビルド",
                "start_build": "ビルド開始",
                "clear_all_area": "全領域削除",

                # ビルド関連
                "build_success": "ビルド成功",
                "build_failed": "ビルド失敗",
                "mod_name_required": "MOD名は空にできません",
                "version_required": "バージョン番号は空にできません",
                "author_required": "作成者情報は空にできません",
                "category_required": "MODカテゴリは空にできません",
                "cover_block_required": "カバーブロックを少なくとも1つ追加してください",
                "cover_image_not_found": "カバー画像ファイルが見つかりません",
                "content_block_required": "コンテンツブロックを少なくとも1つ追加してください",
                "file_not_found": "ファイルが見つかりません",
                "creating_temp_dir": "一時ディレクトリを作成中",
                "creating_cover_folder": "カバーフォルダを作成中",
                "creating_block_folders": "ブロックフォルダを作成中",
                "creating_archive_file": "アーカイブファイルを作成中",
                "moving_to_output": "出力ディレクトリに移動中",
                "build_completed": "ビルド完了",
                "cover_data_missing": "カバーデータが不足しています"
            },
            # 韩语
            "ko_KR": {
                # 메인 윈도우
                "main_window_title": "FMM x MOD 크리에이터",
                "home": "홈",
                "mod_list": "MOD 목록",
                "settings": "설정",

                # 홈 - 블록1
                "mod_info": "MOD 정보",
                "mod_name": "MOD 이름",
                "mod_name_desc": "MOD의 이름을 입력하세요",
                "mod_name_placeholder": "주의: FMM은 영어만 지원",
                "version": "버전 번호",
                "version_desc": "MOD의 버전 번호를 입력",
                "version_placeholder": "예: 1.0.0 (\"v\" 입력 불필요)",
                "author": "작성자 정보",
                "author_desc": "MOD 작성자 이름을 입력",
                "author_placeholder": "주의: FMM은 영어만 지원",
                "mod_category": "MOD 카테고리",
                "mod_category_desc": "MOD의 분류를 입력",
                "mod_category_placeholder": "주의: FMM은 영어만 지원",

                # 홈 - 블록2
                "add_function": "기능 추가",
                "add_function_desc": "오른쪽 버튼으로 각종 기능 컴포넌트를 추가",
                "add_cover": "커버 추가",
                "add_warning": "경고 추가",
                "add_separator": "구분선 추가",
                "add_mod_files": "MOD 파일 추가",

                # MOD 목록 인터페이스
                "import_record": "가져오기 기록",
                "backup_record": "백업 기록",
                "backup_record_success_title": "백업 성공",
                "backup_record_success_content": "파일 위치: {path}",
                "backup_record_failed_title": "백업 실패",
                "backup_record_failed_content": "원인: {error}",
                "import_success_title": "가져오기 성공",
                "import_success_content": "FMM x Mod Creator 생성 기록을 가져왔습니다",
                "import_failed_title": "가져오기 실패",
                "import_failed": "FMM x Mod Creator 생성 기록을 찾을 수 없음",
                "import_error": "원인: {error}",
                "import_mod": "가져오기",
                "edit_mode": "편집",
                "revise_again": "다시 수정합니다",
                "restore_success_title": "복원 성공",
                "restore_success_content": "작업 레이아웃 복원 완료",
                "restore_failed_title": "복원 실패",
                "restore_failed_content": "원인: {error}",
                "home_interface_not_set": "홈 인터페이스 미설정",
                "delete_record": "기록 삭제",
                "operations": "작업",
                "sort_mod": "정렬",
                "sort_by_name": "MOD 이름",
                "sort_by_author": "작성자",
                "sort_by_category": "카테고리",
                "sort_by_date": "생성일",
                "sort_ascending": "오름차순",
                "sort_descending": "내림차순",
                "no_mod_hint": "MOD 빌드 기록이 없습니다. 첫 번째 MOD를 만들어보세요! Great!",
                "serial_number": "No.",
                "cover_image": "커버 이미지",
                "operations": "작업",
                "refresh": "새로고침",
                "no_cover": "커버 없음",
                "category": "카테고리",
                "create_date": "생성일",
                "delete_mod_record_title": "MOD 생성 기록 삭제",
                "delete_mod_record_content": "{mod_name} 을(를) 정말 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.",
                "refresh_success": "데이터가 새로고침되었습니다",
                "refresh_failed": "새로고침 실패: {error}",
                "error": "오류",
                
                # 편집 팁
                "edit_tips_title": "직접 텍스트 편집",
                "edit_tips_content": "편집 버튼을 클릭한 후 셀을 더블클릭하여 데이터를 직접 편집할 수 있습니다.",
                "edit_tips_got_it": "알겠습니다",
                "edit_tips_dont_show": "다시 표시하지 않음",

                # 드래그 앤 드롭 정렬
                "sorting_tips": "정렬 기법",
                "drag_and_drop_sorting_tips_title": "드래그 정렬 기법",
                "drag_and_drop_sorting_tips_content": "컴포넌트를 왼쪽 클릭으로 유지하고 새 위치로 이동",

                # 커버 블록
                "cover_area": "커버 영역",
                "cover_area_desc": "커버 이미지를 업로드",
                "cover_upload": "커버 업로드",
                "cover_upload_desc": "커버 이미지를 업로드",
                "cover_description_placeholder": "커버 설명을 입력",
                "click_to_upload": "이미지 업로드 (MOD 설명용)",
                "select_image": "이미지 선택",
                "delete_cover_block": "커버 블록 삭제",
                "cover_exists_title": "커버 블록이 존재",
                "cover_exists_content": "FMM은 하나의 커버만 표시 가능합니다. 기존 커버 블록을 삭제하세요.",

                # 경고 블록
                "warning_area": "경고 영역",
                "warning_area_desc": "MOD 설치 시 주의사항을 사용자에게 알림",
                "warning_upload_hint": "주의사항 설명용 이미지를 업로드",
                "warning_description_placeholder": "경고 설명을 입력 (주의: FMM은 영어만 지원)",
                "move_warning_block": "경고 블록 이동",
                "copy_warning_block": "경고 블록 복제",
                "delete_warning_block": "경고 블록 삭제",
                "clear_image": "이미지 지우기",
                "drag_to_move_block": "드래그로 이동",
                "collapse_expand": "접기/펼치기",
                "area_mark": "마크(선택 사항)",
                "block_mark_placeholder": "블록 마크",

                # 구분선 블록
                "separator_area": "구분선 영역",
                "separator_area_desc": "MOD 내 콘텐츠 분류용 구분선",
                "separator_name_placeholder": "구분선 이름",
                "copy_separator_block": "구분선 복제",
                "delete_separator_block": "구분선 삭제",

                # MOD 파일 블록
                "mod_file_area": "파일 영역",
                "mod_file_area_desc": "MOD 파일 저장소",
                "module_name": "모듈 이름",
                "module_name_desc": "모듈 이름을 입력",
                "module_name_placeholder": "모듈 이름을 입력",
                "mod_file_upload_hint": "모듈 기능 설명용 이미지를 업로드",
                "mod_file_description_placeholder": "MOD 모듈 설명을 입력",
                "add_files": "파일 추가",
                "add_folders": "폴더 추가",
                "move_mod_file_block": "파일 블록 이동",
                "copy_mod_file_block": "파일 블록 복제",
                "delete_mod_file_block": "파일 블록 삭제",
                "select_files": "파일 선택",
                "select_folders": "폴더 선택",
                "remove_file": "파일 삭제",

                # 파일 표시 영역
                "rename": "이름 변경",
                "delete": "목록에서 삭제",
                "open_file_location": "저장 위치 열기",
                "rename_dialog_title": "이름 변경",
                "rename_dialog_content": "새 이름을 입력:",
                "rename_placeholder": "파일/폴더의 새 이름",
                "name_cannot_be_empty": "이름이 비어있습니다",
                "name_unchanged": "이름 변경 없음",
                "file_display_area": "파일/폴더 표시 영역",
                "confirm": "확인",
                "cancel": "취소",
                "no_files_selected": "파일이 선택되지 않음. 왼쪽 상단 버튼으로 새로 추가 가능",

                # 설정 페이지
                "personalization": "개인화",
                "build_settings": "빌드 설정",
                "build_directory": "빌드 디렉토리",
                "build_directory_desc": "오른쪽에서 출력할 폴더를 선택하세요",
                "build_cache": "캐시 구축",
                "build_cache_desc": "",  # 将显示实际路径
                "choose_folder": "폴더 선택",
                "build_type": "빌드 타입",
                "build_type_desc": "패키지 형식을 선택",
                "theme_setting": "테마 설정",
                "theme_mode": "테마 모드",
                "theme_mode_desc": "애플리케이션 외관을 조정",
                "language_setting": "언어 설정",
                "language_desc": "표시 언어를 선택",
                "mica_effect": "마이카 효과",
                "mica_effect_desc": "창과 재질의 반투명 효과를 활성화",

                "theme_color": "테마 색상",
                "theme_color_desc": "애플리케이션의 색상을 선택",
                "theme_color_turquoise": "🎨터키석",
                "theme_color_camellia": "🎨동백빨강",
                "theme_color_cloisonne": "🎨칠보파랑",
                "theme_color_wheat": "🎨밀색",
                "theme_color_vitriol": "🎨녹반초록",
                "theme_color_primrose": "🎨앵초보라",
                "theme_color_lotus": "🎨연꽃흰색",
                "theme_color_dark": "🎨현색",

                # 다크 모드 테마 색상
                "dark_bichun_green": "벽춘녹",
                "dark_haitang_red": "해당홍",
                "dark_jingtai_blue": "경태람",
                "dark_wheat_yellow": "밀황",
                "dark_qinglian_purple": "청련자",
                "dark_lotus_white": "연판백",

                # 라이트 모드 테마 색상
                "light_camellia_red": "동백빨강",
                "light_gem_blue": "보석파랑",
                "light_cangshan_yellow": "창산황",
                "light_mint_green": "박하녹",
                "light_lilac_purple": "라일락보라",
                "light_xuandai_black": "현대검정",
                "check_update": "업데이트 확인",
                "auto": "시스템 따름",
                "light": "라이트",
                "dark": "다크",
                "chinese": "중국어",
                "english": "영어",
                "japanese": "일본어",
                "korean": "한국어",
                "follow_system": "시스템 따름",
                "language_changed_to_chinese": "중국어로 전환 성공",
                "language_changed_to_english": "영어 전환 성공",
                "restart_required_chinese": "언어 전환 완료",
                "restart_required_english": "언어 전환이 정상적으로 완료되었습니다",
                "update_error_title": "실패",
                "update_error_content": "현재 버전에서는 이 기능을 사용할 수 없습니다",

                # 정보 페이지
                "about": "정보",
                "help": "도움말",
                "help_desc": "지원 정보를 얻기",
                "about_app": "FMM x MOD 크리에이터 정보",
                "about_app_desc": "애플리케이션 정보",
                "app_version": f"버전 {version_info.VERSION_STRING}",
                "app_description": "FMM MOD 제작 도구",
                "developer": f"개발자 · {version_info.APP_AUTHOR} | Version {version_info.VERSION_STRING}",
                "copyright": "© 2025 FMM x Mod Creator. All rights reserved.",

                # 플로팅 메뉴
                "build_zip": "ZIP 빌드",
                "start_build": "빌드 시작",
                "clear_all_area": "모든 영역 지우기",

                # 构建相关
                "build_success": "빌드 성공",
                "build_failed": "빌드 실패",
                "mod_name_required": "MOD 이름이 비어있습니다",
                "version_required": "버전 번호가 비어있습니다",
                "author_required": "작성자 정보가 비어있습니다",
                "category_required": "MOD 카테고리가 비어있습니다",
                "cover_block_required": "커버 블록을 최소 하나 추가해주세요",
                "cover_image_not_found": "커버 이미지 파일을 찾을 수 없습니다",
                "content_block_required": "콘텐츠 블록을 최소 하나 추가해주세요",
                "file_not_found": "파일을 찾을 수 없습니다",
                "creating_temp_dir": "임시 디렉토리 생성 중",
                "creating_cover_folder": "커버 폴더 생성 중",
                "creating_block_folders": "블록 폴더 생성 중",
                "creating_archive_file": "아카이브 파일 생성 중",
                "moving_to_output": "출력 디렉토리로 이동 중",
                "build_completed": "빌드 완료",
                "cover_data_missing": "커버 데이터가 누락되었습니다"
            }
        }
    
    def _get_system_language(self) -> str:
        """获取系统语言"""
        try:
            # Get the system language with QLocale
            system_locale = QLocale.system()
            locale_name = system_locale.name()
            
            # Mapping system languages to supported languages
            if locale_name.startswith('zh_CN') or locale_name.startswith('zh_Hans'):
                return 'zh_CN'
            elif locale_name.startswith('en'):
                return 'en'
            elif locale_name.startswith('ja'):
                return 'ja_JP'
            elif locale_name.startswith('ko'):
                return 'ko_KR'
            else:
                # If QLocale cannot identify, try using Python's locale module
                try:
                    system_lang = locale.getdefaultlocale()[0]
                    if system_lang:
                        if system_lang.startswith('zh_CN') or system_lang.startswith('Chinese'):
                            return 'zh_CN'
                        elif system_lang.startswith('en'):
                            return 'en'
                        elif system_lang.startswith('ja'):
                            return 'ja_JP'
                        elif system_lang.startswith('ko'):
                            return 'ko_KR'
                except:
                    pass
                return 'zh_CN'
        except Exception:
            return 'zh_CN'
    
    def set_language(self, language: str):
        """设置语言"""
        if language == "system":
            actual_language = self._get_system_language()
        else:
            actual_language = language
            
        if actual_language in self.translations and actual_language != self.current_language:
            self.current_language = actual_language
            self.languageChanged.emit()
    
    def get_text(self, key: str, default: str = None) -> str:
        """获取文本"""
        if default is None:
            default = key
        return self.translations.get(self.current_language, {}).get(key, default)
    
    def get_current_language(self) -> str:
        """获取当前语言"""
        return self.current_language

# Global Language Manager instance
lang = LanguageManager()