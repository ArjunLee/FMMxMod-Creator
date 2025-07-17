# coding:utf-8
"""
Settings Interface
设置界面模块
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from qfluentwidgets import (
    ScrollArea, SettingCardGroup, ComboBoxSettingCard, SwitchSettingCard, HyperlinkCard,
    PrimaryPushSettingCard, PushSettingCard, OptionsSettingCard, FluentIcon as FIF, setTheme, Theme, setThemeColor,
    InfoBar, InfoBarPosition, OptionsConfigItem, BoolValidator, OptionsValidator
)
from PySide6.QtWidgets import QFileDialog
from ..common.config import cfg
from ..common.language import lang

class SettingsInterface(ScrollArea):
    """设置界面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._initUI()
        self._connectSignals()
    
    def _initUI(self):
        """初始化界面"""
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self._createPersonalizationGroup()
        self._createBuildGroup()
        self._createAboutGroup()
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.addWidget(self.personalizationGroup)
        self.vBoxLayout.addWidget(self.buildGroup)
        self.vBoxLayout.addWidget(self.aboutGroup)
        self.vBoxLayout.addStretch(1)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName("settingsInterface")
        
        self.setStyleSheet("""
            SettingsInterface {
                background-color: transparent;
                border: none;
            }
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QWidget {
                background-color: transparent;
                border: none;
            }
        """)
    
    def _createPersonalizationGroup(self):
        """创建个性化设置组"""
        self.personalizationGroup = SettingCardGroup(
            lang.get_text("personalization"), 
            self.scrollWidget
        )
        
        # Create Theme Configuration Item
        self.themeConfigItem = OptionsConfigItem(
            "Personalization", "ThemeMode", "Dark", 
            OptionsValidator(["Dark", "Light", "Auto"])
        )
        
        # Create Language Configuration Item
        self.languageConfigItem = OptionsConfigItem(
            "Personalization", "Language", "system", 
            OptionsValidator(["system", "zh_CN", "en", "ja_JP", "ko_KR"])
        )
        
        # Create Theme Color Configuration Item
        self.themeColorConfigItem = OptionsConfigItem(
            "Personalization", "ThemeColor", "bichun_green",
            OptionsValidator(["haitang_red", "jingtai_blue", "wheat_yellow", "bichun_green", "qinglian_purple", "lotus_white", "camellia_red", "gem_blue", "cangshan_yellow", "mint_green", "lilac_purple", "xuandai_black"])
        )
        
        # Create Theme Setting Card
        self.themeCard = ComboBoxSettingCard(
            self.themeConfigItem,
            FIF.BRUSH,
            lang.get_text("theme_mode"),
            lang.get_text("theme_mode_desc"),
            texts=[
                lang.get_text("dark"),
                lang.get_text("light"),
                lang.get_text("auto")
            ],
            parent=self.personalizationGroup
        )
        
        # Create Language Setting Card
        self.languageCard = ComboBoxSettingCard(
            self.languageConfigItem,
            FIF.LANGUAGE,
            lang.get_text("language_setting"),
            lang.get_text("language_desc"),
            texts=[lang.get_text("follow_system"), lang.get_text("chinese"), lang.get_text("english"), lang.get_text("japanese"), lang.get_text("korean")],
            parent=self.personalizationGroup
        )
        
        # Create Theme Color Setting Card
        self.themeColorCard = ComboBoxSettingCard(
            self.themeColorConfigItem,
            FIF.PALETTE,
            lang.get_text("theme_color"),
            lang.get_text("theme_color_desc"),
            texts=[
                "碧春绿",
                "海棠红",
                "景泰蓝",
                "麦桔黄",
                "青莲紫",
                "莲瓣白"
            ],
            parent=self.personalizationGroup
        )
        
        # Create Mica Effect Configuration Item
        self.micaConfigItem = OptionsConfigItem(
            "Personalization", "MicaEffect", True, 
            BoolValidator()
        )
        
        # Create Mica Effect Setting Card
        self.micaCard = SwitchSettingCard(
            FIF.TRANSPARENT,
            lang.get_text("mica_effect"),
            lang.get_text("mica_effect_desc"),
            self.micaConfigItem,
            parent=self.personalizationGroup
        )
        
        # Set the current selection
        current_theme = cfg.get("theme_mode", "Auto")
        self.themeConfigItem.value = current_theme
        theme_map = {"Auto": 0, "Light": 1, "Dark": 2}
        self.themeCard.comboBox.setCurrentIndex(theme_map.get(current_theme, 0))
        
        current_language = cfg.get("language", "system")
        self.languageConfigItem.value = current_language
        lang_map = {"system": 0, "zh_CN": 1, "en": 2, "ja_JP": 3, "ko_KR": 4}
        self.languageCard.comboBox.setCurrentIndex(lang_map.get(current_language, 0))
        
        # Create Mica Effect Default State
        current_mica = cfg.get("mica_enabled", True)
        self.micaConfigItem.value = current_mica
        self.micaCard.setChecked(current_mica)
        
        # Create Mica Effect Default State
        current_theme = cfg.get("theme_mode", "Auto")
        current_theme_color = cfg.get("theme_color", "bichun_green" if current_theme == "Dark" else "camellia_red")
        self.themeColorConfigItem.value = current_theme_color
        
        # Update Theme Color Options
        self._updateThemeColorOptions(current_theme)
        
        # Set the current selection
        self._setCurrentThemeColorIndex(current_theme_color, current_theme)
        
        # Add cards to the group
        self.personalizationGroup.addSettingCard(self.micaCard)
        self.personalizationGroup.addSettingCard(self.themeCard)
        self.personalizationGroup.addSettingCard(self.languageCard)
        self.personalizationGroup.addSettingCard(self.themeColorCard)
    
    def _createBuildGroup(self):
        """创建构筑设置组"""
        self.buildGroup = SettingCardGroup(
            lang.get_text("build_settings"), 
            self.scrollWidget
        )
        
        # Create Build Directory Setting Card
        current_build_dir = cfg.get("build_directory", "")
        if not current_build_dir:
            display_path = cfg.buildDirectory
        else:
            display_path = current_build_dir
        
        self.buildDirectoryCard = PushSettingCard(
            lang.get_text("choose_folder"),
            FIF.FOLDER,
            lang.get_text("build_directory"),
            display_path,
            self.buildGroup
        )
        
        # Create build type configuration item
        current_build_type = cfg.get("build_type", "zip")
        self.buildTypeConfigItem = OptionsConfigItem(
            "Build", "BuildType", current_build_type, 
            OptionsValidator(["zip", "rar", "7z"])
        )
        
        # Create build cache setting card
        current_cache_dir = cfg.get("cache_directory", "")
        if not current_cache_dir:
            current_cache_dir = cfg.cacheDirectory
        
        self.buildCacheCard = PushSettingCard(
            lang.get_text("choose_folder"),
            FIF.BROOM,
            lang.get_text("build_cache"),
            current_cache_dir,
            self.buildGroup
        )
        
        # Build Type Setup Card
        self.buildTypeCard = OptionsSettingCard(
            self.buildTypeConfigItem,
            FIF.ZIP_FOLDER,
            lang.get_text("build_type"),
            lang.get_text("build_type_desc"),
            texts=[".Zip", ".Rar", ".7z"],
            parent=self.buildGroup
        )
        
        # Add cards to the group
        self.buildGroup.addSettingCard(self.buildDirectoryCard)
        self.buildGroup.addSettingCard(self.buildCacheCard)
        self.buildGroup.addSettingCard(self.buildTypeCard)
    
    def _updateThemeColorOptions(self, theme_mode):
        """根据主题模式更新主题色选项"""
        try:
            self.themeColorCard.comboBox.currentTextChanged.disconnect(self._onThemeColorChanged)
        except (TypeError, RuntimeError):
            # If the signal is not connected or disconnected, ignore the error
            pass
        
        # Clear existing options
        self.themeColorCard.comboBox.clear()
        
        if theme_mode == "Dark":
            self.themeColorCard.comboBox.addItems([
                lang.get_text("dark_bichun_green"),
                lang.get_text("dark_haitang_red"),
                lang.get_text("dark_jingtai_blue"),
                lang.get_text("dark_wheat_yellow"),
                lang.get_text("dark_qinglian_purple"),
                lang.get_text("dark_lotus_white")
            ])
        else:
            self.themeColorCard.comboBox.addItems([
                lang.get_text("light_camellia_red"),
                lang.get_text("light_gem_blue"),
                lang.get_text("light_cangshan_yellow"),
                lang.get_text("light_mint_green"),
                lang.get_text("light_lilac_purple"),
                lang.get_text("light_xuandai_black")
            ])
        
        self.themeColorCard.comboBox.currentTextChanged.connect(self._onThemeColorChanged)
    
    def _setCurrentThemeColorIndex(self, theme_color, theme_mode):
        """设置当前主题色选中项"""
        if theme_mode == "Dark":
            dark_color_map = {
                "bichun_green": 0,
                "haitang_red": 1,
                "jingtai_blue": 2,
                "wheat_yellow": 3,
                "qinglian_purple": 4,
                "lotus_white": 5
            }
            index = dark_color_map.get(theme_color, 0)
        else:
            light_color_map = {
                "camellia_red": 0,
                "gem_blue": 1,
                "cangshan_yellow": 2,
                "mint_green": 3,
                "lilac_purple": 4,
                "xuandai_black": 5
            }
            index = light_color_map.get(theme_color, 0)
        
        self.themeColorCard.comboBox.setCurrentIndex(index)
    
    def _createAboutGroup(self):
        """创建关于设置组"""
        self.aboutGroup = SettingCardGroup(
            lang.get_text("about"), 
            self.scrollWidget
        )
        
        self.helpCard = HyperlinkCard(
            "https://github.com/ArjunLee/FMMxMod-Creator",
            lang.get_text("help"),
            FIF.HELP,
            lang.get_text("help"),
            lang.get_text("help_desc"),
            self.aboutGroup
        )
        
        self.aboutCard = PrimaryPushSettingCard(
            lang.get_text("check_update"),
            FIF.INFO,
            lang.get_text("about_app"),
            lang.get_text("developer"),
            self.aboutGroup
        )
        
        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.aboutCard)
    
    def _connectSignals(self):
        """连接信号"""
        self.themeCard.comboBox.currentTextChanged.connect(self._onThemeChanged)                 # theme change
        self.languageCard.comboBox.currentTextChanged.connect(self._onLanguageChanged)           # language change
        self.themeColorCard.comboBox.currentTextChanged.connect(self._onThemeColorChanged)       # theme color change
        self.micaCard.checkedChanged.connect(self._onMicaChanged)                                # mica effect change
        self.aboutCard.clicked.connect(self._showAboutDialog)                                    # about button click
        self.buildDirectoryCard.clicked.connect(self._onBuildDirectoryClicked)                   # build directory choose
        self.buildCacheCard.clicked.connect(self._onBuildCacheClicked)                           # build cache choose
        self.buildTypeCard.optionChanged.connect(self._onBuildTypeChanged)                       # build type change
        
        lang.languageChanged.connect(lambda: self._updateTexts(disconnect_signals=True))
    
    def _onThemeChanged(self, theme_text):
        """主题改变时的处理"""
        theme_map = {
            lang.get_text("dark"): "Dark",
            lang.get_text("light"): "Light",
            lang.get_text("auto"): "Auto"
        }
        theme_value = theme_map.get(theme_text, "Dark")
        cfg.set("theme_mode", theme_value)
        setTheme(Theme.DARK if theme_value == "Dark" else 
                Theme.LIGHT if theme_value == "Light" else Theme.AUTO)

        self._updateThemeColorOptions(theme_value)
        
        if theme_value == "Dark":
            default_color = "bichun_green"
            color_hex = "#10893E"
        else:
            default_color = "camellia_red"
            color_hex = "#EE3F4E"
        
        cfg.set("theme_color", default_color)
        self._setCurrentThemeColorIndex(default_color, theme_value)
        setThemeColor(color_hex)
    
    def _onLanguageChanged(self, language_text):
        """语言变化处理"""
        if language_text == lang.get_text("follow_system"):
            language = "system"
        elif language_text == lang.get_text("chinese"):
            language = "zh_CN"
        elif language_text == lang.get_text("english"):
            language = "en"
        elif language_text == lang.get_text("japanese"):
            language = "ja_JP"
        elif language_text == lang.get_text("korean"):
            language = "ko_KR"
        else:
            language = "system"
        
        current_language = cfg.get("language", "system")
        if current_language == language:
            return
        
        if language == "zh_CN":
            title = "幸甚至哉"
            content = "言枢已焕"
        else:
            title = "Success"
            content = "The language has been successfully switched"
        
        cfg.set("language", language)
        lang.set_language(language)
                
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def _onThemeColorChanged(self, color_text):
        """主题色变化处理"""
        current_theme = cfg.get("theme_mode", "Auto")
        
        if current_theme == "Dark":
            dark_color_map = {
                lang.get_text("dark_bichun_green"): ("bichun_green", "#10893E"),
                lang.get_text("dark_haitang_red"): ("haitang_red", "#FF5F91"),
                lang.get_text("dark_jingtai_blue"): ("jingtai_blue", "#61B2DD"),
                lang.get_text("dark_wheat_yellow"): ("wheat_yellow", "#F9DF70"),
                lang.get_text("dark_qinglian_purple"): ("qinglian_purple", "#9583CD"),
                lang.get_text("dark_lotus_white"): ("lotus_white", "#EFF4F7")
            }
            theme_color, color_hex = dark_color_map.get(color_text, ("bichun_green", "#10893E"))
        else:
            light_color_map = {
                lang.get_text("light_camellia_red"): ("camellia_red", "#EE3F4E"),
                lang.get_text("light_gem_blue"): ("gem_blue", "#3946AF"),
                lang.get_text("light_cangshan_yellow"): ("cangshan_yellow", "#A4612D"),
                lang.get_text("light_mint_green"): ("mint_green", "#217F4D"),
                lang.get_text("light_lilac_purple"): ("lilac_purple", "#635282"),
                lang.get_text("light_xuandai_black"): ("xuandai_black", "#36353B")
            }
            theme_color, color_hex = light_color_map.get(color_text, ("camellia_red", "#EE3F4E"))
        
        cfg.set("theme_color", theme_color)
        setThemeColor(color_hex)
    
    def _onMicaChanged(self, enabled):
        """云母效果变化处理"""
        cfg.set("mica_enabled", enabled)

        if self.parent and hasattr(self.parent, 'setMicaEffectEnabled'):
            self.parent.setMicaEffectEnabled(enabled)
    
    def _showAboutDialog(self):
        """显示关于对话框"""
        InfoBar.error(
            title=lang.get_text("update_error_title"),
            content=lang.get_text("update_error_content"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3000,
            parent=self
        )
    
    def _onBuildDirectoryClicked(self):
        """构筑目录选择处理"""
        current_dir = cfg.get("build_directory", "")
        folder = QFileDialog.getExistingDirectory(
            self,
            lang.get_text("choose_folder"),
            current_dir
        )
        
        if folder:
            cfg.set("build_directory", folder)
            self.buildDirectoryCard.setContent(folder)
    
    def _onBuildCacheClicked(self):
        """构筑缓存目录选择处理"""
        current_dir = cfg.get("cache_directory", "")
        if not current_dir:
            current_dir = cfg.cacheDirectory
        
        folder = QFileDialog.getExistingDirectory(
            self,
            lang.get_text("choose_folder"),
            current_dir
        )
        
        if folder:
            cfg.set("cache_directory", folder)
            self.buildCacheCard.setContent(folder)
    
    def _onBuildTypeChanged(self, config_value):
        """构筑类型变化处理"""
        cfg.set("build_type", config_value)
    
    def _updateTexts(self, disconnect_signals=False):
        """更新界面文本"""
        self.personalizationGroup.titleLabel.setText(lang.get_text("personalization"))
        self.buildGroup.titleLabel.setText(lang.get_text("build_settings"))
        self.aboutGroup.titleLabel.setText(lang.get_text("about"))

        try:
            self.themeCard.comboBox.currentTextChanged.disconnect(self._onThemeChanged)
        except TypeError:
            pass
        self.themeCard.setTitle(lang.get_text("theme_mode"))
        self.themeCard.setContent(lang.get_text("theme_mode_desc"))
        self.themeCard.comboBox.clear()
        
        theme_options = [
            lang.get_text("auto"),
            lang.get_text("light"), 
            lang.get_text("dark")
        ]
        self.themeCard.comboBox.addItems(theme_options)
        
        current_theme = cfg.get("theme_mode", "Auto")
        if current_theme == "Auto":
            current_index = 0
        elif current_theme == "Light":
            current_index = 1
        elif current_theme == "Dark":
            current_index = 2
        else:
            current_index = 0
            
        self.themeCard.comboBox.setCurrentIndex(current_index)
        self.themeCard.comboBox.currentTextChanged.connect(self._onThemeChanged)

        try:
            self.languageCard.comboBox.currentTextChanged.disconnect(self._onLanguageChanged)
        except TypeError:
            pass
        self.languageCard.setTitle(lang.get_text("language_setting"))
        self.languageCard.setContent(lang.get_text("language_desc"))
        self.languageCard.comboBox.clear()
        self.languageCard.comboBox.addItems([
            lang.get_text("follow_system"),
            lang.get_text("chinese"),
            lang.get_text("english"),
            lang.get_text("japanese"),
            lang.get_text("korean")
        ])
        lang_map = {"system": 0, "zh_CN": 1, "en": 2, "ja_JP": 3, "ko_KR": 4}
        current_language = cfg.get("language", "system")
        self.languageCard.comboBox.setCurrentIndex(lang_map.get(current_language, 0))
        self.languageCard.comboBox.currentTextChanged.connect(self._onLanguageChanged)

        try:
            self.themeColorCard.comboBox.currentTextChanged.disconnect(self._onThemeColorChanged)
        except (TypeError, RuntimeError):
            pass
            
        self.themeColorCard.setTitle(lang.get_text("theme_color"))
        self.themeColorCard.setContent(lang.get_text("theme_color_desc"))
        current_theme = cfg.get("theme_mode", "Auto")
        current_theme_color = cfg.get("theme_color", "bichun_green" if current_theme == "Dark" else "camellia_red")
        self._updateThemeColorOptions(current_theme)
        self._setCurrentThemeColorIndex(current_theme_color, current_theme)
        self.helpCard.setTitle(lang.get_text("help"))
        self.helpCard.setContent(lang.get_text("help_desc"))
        self.helpCard.linkButton.setText(lang.get_text("help"))

        try:
            self.micaCard.checkedChanged.disconnect(self._onMicaChanged)
        except TypeError:
            pass

        self.micaCard.setTitle(lang.get_text("mica_effect"))
        self.micaCard.setContent(lang.get_text("mica_effect_desc"))
        current_mica = cfg.get("mica_enabled", True)
        self.micaCard.setChecked(current_mica)
        self.micaCard.checkedChanged.connect(self._onMicaChanged)
        
        try:
            self.buildDirectoryCard.clicked.disconnect(self._onBuildDirectoryClicked)
        except TypeError:
            pass

        self.buildDirectoryCard.setTitle(lang.get_text("build_directory"))
        current_build_dir = cfg.get("build_directory", "")

        if not current_build_dir:
            display_path = cfg.buildDirectory
        else:
            display_path = current_build_dir

        self.buildDirectoryCard.setContent(display_path)
        self.buildDirectoryCard.button.setText(lang.get_text("choose_folder"))
        self.buildDirectoryCard.clicked.connect(self._onBuildDirectoryClicked)
        
        try:
            self.buildCacheCard.clicked.disconnect(self._onBuildCacheClicked)
        except TypeError:
            pass

        self.buildCacheCard.setTitle(lang.get_text("build_cache"))
        current_cache_dir = cfg.get("cache_directory", "")

        if not current_cache_dir:
            current_cache_dir = cfg.cacheDirectory

        self.buildCacheCard.setContent(current_cache_dir)
        self.buildCacheCard.button.setText(lang.get_text("choose_folder"))
        self.buildCacheCard.clicked.connect(self._onBuildCacheClicked)
        
        try:
            self.buildTypeCard.optionChanged.disconnect(self._onBuildTypeChanged)
        except TypeError:
            pass

        self.buildTypeCard.card.setTitle(lang.get_text("build_type"))
        self.buildTypeCard.card.setContent(lang.get_text("build_type_desc"))
        self.buildTypeCard.optionChanged.connect(self._onBuildTypeChanged)
        self.aboutCard.setTitle(lang.get_text("about_app"))
        self.aboutCard.setContent(lang.get_text("developer"))
        self.aboutCard.button.setText(lang.get_text("check_update"))
    
    def updateText(self):
        """更新文本"""
        self._updateTexts()