"""
Visual Configuration Editor for Overlay Settings
Provides a user-friendly GUI to customize all overlay options
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, 
    QPushButton, QGroupBox, QLineEdit, QTabWidget, QMessageBox,
    QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from overlay.config import OverlayConfig, get_config, save_config, reload_config

class ConfigEditor(QMainWindow):
    """
    Visual editor for overlay configuration
    """
    
    def __init__(self):
        super().__init__()
        self.config = get_config()
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Chess Overlay - Configuration Editor")
        self.setGeometry(100, 100, 800, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title = QLabel("⚙️ Overlay Configuration")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self._create_appearance_tab(), "🎨 Appearance")
        tabs.addTab(self._create_position_tab(), "📍 Position")
        tabs.addTab(self._create_display_tab(), "👁️ Display")
        tabs.addTab(self._create_language_tab(), "🌍 Language")
        tabs.addTab(self._create_country_tab(), "🚩 Countries")
        tabs.addTab(self._create_advanced_tab(), "⚡ Advanced")
        
        main_layout.addWidget(tabs)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        btn_save = QPushButton("💾 Save Configuration")
        btn_save.clicked.connect(self.save_settings)
        btn_save.setStyleSheet("QPushButton { background-color: #22c55e; color: white; padding: 10px; font-weight: bold; border-radius: 5px; }")
        button_layout.addWidget(btn_save)
        
        btn_reset = QPushButton("🔄 Reset to Defaults")
        btn_reset.clicked.connect(self.reset_settings)
        btn_reset.setStyleSheet("QPushButton { background-color: #ef4444; color: white; padding: 10px; font-weight: bold; border-radius: 5px; }")
        button_layout.addWidget(btn_reset)
        
        btn_test = QPushButton("🧪 Test Overlay")
        btn_test.clicked.connect(self.test_overlay)
        btn_test.setStyleSheet("QPushButton { background-color: #3b82f6; color: white; padding: 10px; font-weight: bold; border-radius: 5px; }")
        button_layout.addWidget(btn_test)
        
        main_layout.addLayout(button_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def _create_appearance_tab(self) -> QWidget:
        """Create appearance settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Icon Size
        group = QGroupBox("Icon Settings")
        group_layout = QVBoxLayout()
        
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(QLabel("Icon Size (px):"))
        self.icon_size_spin = QSpinBox()
        self.icon_size_spin.setRange(16, 64)
        self.icon_size_spin.setSuffix(" px")
        icon_layout.addWidget(self.icon_size_spin)
        icon_layout.addStretch()
        group_layout.addLayout(icon_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Font Size
        group = QGroupBox("Text Settings")
        group_layout = QVBoxLayout()
        
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Font Size (px):"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 32)
        self.font_size_spin.setSuffix(" px")
        font_layout.addWidget(self.font_size_spin)
        font_layout.addStretch()
        group_layout.addLayout(font_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Overlay Size
        group = QGroupBox("Overlay Dimensions")
        group_layout = QVBoxLayout()
        
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width (px):"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(300, 800)
        self.width_spin.setSuffix(" px")
        width_layout.addWidget(self.width_spin)
        width_layout.addStretch()
        group_layout.addLayout(width_layout)
        
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height (px):"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(200, 600)
        self.height_spin.setSuffix(" px")
        height_layout.addWidget(self.height_spin)
        height_layout.addStretch()
        group_layout.addLayout(height_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Opacity
        group = QGroupBox("Transparency")
        group_layout = QVBoxLayout()
        
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        self.opacity_spin = QDoubleSpinBox()
        self.opacity_spin.setRange(0.0, 1.0)
        self.opacity_spin.setSingleStep(0.05)
        opacity_layout.addWidget(self.opacity_spin)
        opacity_layout.addStretch()
        group_layout.addLayout(opacity_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Theme
        group = QGroupBox("Theme")
        group_layout = QVBoxLayout()
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light", "transparent"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        group_layout.addLayout(theme_layout)
        
        self.blur_check = QCheckBox("Enable Background Blur")
        group_layout.addWidget(self.blur_check)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return widget
    
    def _create_position_tab(self) -> QWidget:
        """Create position settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Position
        group = QGroupBox("Screen Position")
        group_layout = QVBoxLayout()
        
        x_layout = QHBoxLayout()
        x_layout.addWidget(QLabel("X Position:"))
        self.pos_x_spin = QSpinBox()
        self.pos_x_spin.setRange(0, 9999)
        self.pos_x_spin.setSuffix(" px")
        x_layout.addWidget(self.pos_x_spin)
        x_layout.addStretch()
        group_layout.addLayout(x_layout)
        
        y_layout = QHBoxLayout()
        y_layout.addWidget(QLabel("Y Position:"))
        self.pos_y_spin = QSpinBox()
        self.pos_y_spin.setRange(0, 9999)
        self.pos_y_spin.setSuffix(" px")
        y_layout.addWidget(self.pos_y_spin)
        y_layout.addStretch()
        group_layout.addLayout(y_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Options
        group = QGroupBox("Position Options")
        group_layout = QVBoxLayout()
        
        self.lock_position_check = QCheckBox("Lock Position (Disable Dragging)")
        group_layout.addWidget(self.lock_position_check)
        
        self.always_on_top_check = QCheckBox("Always on Top")
        group_layout.addWidget(self.always_on_top_check)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Info
        info = QLabel("💡 Tip: You can drag the overlay window to move it, and the position will be saved automatically.")
        info.setWordWrap(True)
        info.setStyleSheet("QLabel { background-color: #3b82f6; color: white; padding: 10px; border-radius: 5px; }")
        layout.addWidget(info)
        
        layout.addStretch()
        return widget
    
    def _create_display_tab(self) -> QWidget:
        """Create display settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Display Options
        group = QGroupBox("Display Options")
        group_layout = QVBoxLayout()
        
        self.show_best_move_check = QCheckBox("Show Engine's Best Move")
        group_layout.addWidget(self.show_best_move_check)
        
        self.show_opp_best_check = QCheckBox("Show Opponent's Best Response")
        group_layout.addWidget(self.show_opp_best_check)
        
        self.show_eval_check = QCheckBox("Show Evaluation (Centipawns)")
        group_layout.addWidget(self.show_eval_check)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Auto-Hide
        group = QGroupBox("Auto-Hide Settings")
        group_layout = QVBoxLayout()
        
        hide_layout = QHBoxLayout()
        hide_layout.addWidget(QLabel("Auto-Hide Delay:"))
        self.auto_hide_spin = QSpinBox()
        self.auto_hide_spin.setRange(0, 30000)
        self.auto_hide_spin.setSingleStep(1000)
        self.auto_hide_spin.setSuffix(" ms")
        self.auto_hide_spin.setSpecialValueText("Never")
        hide_layout.addWidget(self.auto_hide_spin)
        hide_layout.addStretch()
        group_layout.addLayout(hide_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Animation
        group = QGroupBox("Animation Settings")
        group_layout = QVBoxLayout()
        
        anim_layout = QHBoxLayout()
        anim_layout.addWidget(QLabel("Animation Speed:"))
        self.anim_speed_spin = QDoubleSpinBox()
        self.anim_speed_spin.setRange(0.5, 2.0)
        self.anim_speed_spin.setSingleStep(0.1)
        self.anim_speed_spin.setSuffix("x")
        anim_layout.addWidget(self.anim_speed_spin)
        anim_layout.addStretch()
        group_layout.addLayout(anim_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return widget
    
    def _create_language_tab(self) -> QWidget:
        """Create language settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Language Selection
        group = QGroupBox("Language Settings")
        group_layout = QVBoxLayout()
        
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("UI Language:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "en - English",
            "vi - Tiếng Việt",
            "es - Español",
            "fr - Français",
            "de - Deutsch",
            "ru - Русский",
            "zh - 中文"
        ])
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        group_layout.addLayout(lang_layout)
        
        notation_layout = QHBoxLayout()
        notation_layout.addWidget(QLabel("Move Notation:"))
        self.notation_combo = QComboBox()
        self.notation_combo.addItems(["san - Standard (e4, Nf3)", "uci - Universal (e2e4, g1f3)"])
        notation_layout.addWidget(self.notation_combo)
        notation_layout.addStretch()
        group_layout.addLayout(notation_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Info
        info = QLabel("🌍 Language labels are automatically loaded from the configuration. Custom labels can be edited in the JSON file.")
        info.setWordWrap(True)
        info.setStyleSheet("QLabel { background-color: #22c55e; color: white; padding: 10px; border-radius: 5px; }")
        layout.addWidget(info)
        
        layout.addStretch()
        return widget
    
    def _create_country_tab(self) -> QWidget:
        """Create country filter settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Allowed Countries
        group = QGroupBox("Allowed Countries (Whitelist)")
        group_layout = QVBoxLayout()
        
        info = QLabel("Leave empty to allow all countries. Add ISO country codes (e.g., US, GB, VN) to restrict.")
        info.setWordWrap(True)
        group_layout.addWidget(info)
        
        self.allowed_countries_list = QLineEdit()
        self.allowed_countries_list.setPlaceholderText("e.g., US, GB, VN, FR, DE")
        group_layout.addWidget(self.allowed_countries_list)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Blocked Countries
        group = QGroupBox("Blocked Countries (Blacklist)")
        group_layout = QVBoxLayout()
        
        info = QLabel("Add ISO country codes to block specific countries.")
        info.setWordWrap(True)
        group_layout.addWidget(info)
        
        self.blocked_countries_list = QLineEdit()
        self.blocked_countries_list.setPlaceholderText("e.g., XX, YY, ZZ")
        group_layout.addWidget(self.blocked_countries_list)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Options
        self.show_flags_check = QCheckBox("Show Country Flags for Players")
        layout.addWidget(self.show_flags_check)
        
        # Warning
        warning = QLabel("⚠️ Country filtering is currently not implemented in the player detection system. This will be added in a future update.")
        warning.setWordWrap(True)
        warning.setStyleSheet("QLabel { background-color: #f59e0b; color: white; padding: 10px; border-radius: 5px; }")
        layout.addWidget(warning)
        
        layout.addStretch()
        return widget
    
    def _create_advanced_tab(self) -> QWidget:
        """Create advanced settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Advanced Options
        group = QGroupBox("Advanced Options")
        group_layout = QVBoxLayout()
        
        self.enable_sound_check = QCheckBox("Enable Sound Effects (Not Implemented)")
        self.enable_sound_check.setEnabled(False)
        group_layout.addWidget(self.enable_sound_check)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        # Config File Path
        group = QGroupBox("Configuration File")
        group_layout = QVBoxLayout()
        
        path_label = QLabel(f"📁 Config Path: overlay/overlay_config.json")
        path_label.setWordWrap(True)
        group_layout.addWidget(path_label)
        
        btn_open_folder = QPushButton("📂 Open Config Folder")
        btn_open_folder.clicked.connect(self.open_config_folder)
        group_layout.addWidget(btn_open_folder)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
        layout.addStretch()
        return widget
    
    def load_settings(self):
        """Load settings from config into UI"""
        self.icon_size_spin.setValue(self.config.icon_size)
        self.font_size_spin.setValue(self.config.font_size)
        self.width_spin.setValue(self.config.overlay_width)
        self.height_spin.setValue(self.config.overlay_height)
        self.opacity_spin.setValue(self.config.opacity)
        self.theme_combo.setCurrentText(self.config.theme)
        self.blur_check.setChecked(self.config.blur_background)
        
        self.pos_x_spin.setValue(self.config.position_x)
        self.pos_y_spin.setValue(self.config.position_y)
        self.lock_position_check.setChecked(self.config.lock_position)
        self.always_on_top_check.setChecked(self.config.always_on_top)
        
        self.show_best_move_check.setChecked(self.config.show_best_move)
        self.show_opp_best_check.setChecked(self.config.show_opponent_best)
        self.show_eval_check.setChecked(self.config.show_evaluation)
        self.auto_hide_spin.setValue(self.config.auto_hide_delay)
        self.anim_speed_spin.setValue(self.config.animation_speed)
        
        # Language
        lang_index = {"en": 0, "vi": 1, "es": 2, "fr": 3, "de": 4, "ru": 5, "zh": 6}.get(self.config.language, 0)
        self.language_combo.setCurrentIndex(lang_index)
        
        notation_index = 0 if self.config.move_notation == "san" else 1
        self.notation_combo.setCurrentIndex(notation_index)
        
        # Countries
        self.allowed_countries_list.setText(", ".join(self.config.allowed_countries))
        self.blocked_countries_list.setText(", ".join(self.config.blocked_countries))
        self.show_flags_check.setChecked(self.config.show_country_flags)
        
        self.enable_sound_check.setChecked(self.config.enable_sound)
    
    def save_settings(self):
        """Save UI settings to config"""
        self.config.icon_size = self.icon_size_spin.value()
        self.config.font_size = self.font_size_spin.value()
        self.config.overlay_width = self.width_spin.value()
        self.config.overlay_height = self.height_spin.value()
        self.config.opacity = self.opacity_spin.value()
        self.config.theme = self.theme_combo.currentText()
        self.config.blur_background = self.blur_check.isChecked()
        
        self.config.position_x = self.pos_x_spin.value()
        self.config.position_y = self.pos_y_spin.value()
        self.config.lock_position = self.lock_position_check.isChecked()
        self.config.always_on_top = self.always_on_top_check.isChecked()
        
        self.config.show_best_move = self.show_best_move_check.isChecked()
        self.config.show_opponent_best = self.show_opp_best_check.isChecked()
        self.config.show_evaluation = self.show_eval_check.isChecked()
        self.config.auto_hide_delay = self.auto_hide_spin.value()
        self.config.animation_speed = self.anim_speed_spin.value()
        
        # Language
        lang_map = ["en", "vi", "es", "fr", "de", "ru", "zh"]
        self.config.language = lang_map[self.language_combo.currentIndex()]
        self.config.labels = self.config._get_default_labels()
        
        self.config.move_notation = "san" if self.notation_combo.currentIndex() == 0 else "uci"
        
        # Countries
        allowed = [c.strip() for c in self.allowed_countries_list.text().split(",") if c.strip()]
        blocked = [c.strip() for c in self.blocked_countries_list.text().split(",") if c.strip()]
        self.config.allowed_countries = allowed
        self.config.blocked_countries = blocked
        self.config.show_country_flags = self.show_flags_check.isChecked()
        
        self.config.enable_sound = self.enable_sound_check.isChecked()
        
        # Validate and save
        is_valid, error = self.config.validate()
        if is_valid:
            save_config()
            QMessageBox.information(self, "Success", "✅ Configuration saved successfully!")
            self.statusBar().showMessage("Configuration saved", 3000)
        else:
            QMessageBox.warning(self, "Validation Error", f"❌ {error}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self, 
            "Confirm Reset",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.config.reset_to_defaults()
            save_config()
            self.load_settings()
            QMessageBox.information(self, "Reset Complete", "✅ Settings reset to defaults!")
            self.statusBar().showMessage("Settings reset", 3000)
    
    def test_overlay(self):
        """Test overlay with sample data"""
        try:
            from overlay.window import get_overlay
            from overlay.models import MoveDisplayData
            
            overlay = get_overlay()
            test_data = MoveDisplayData(
                label="brilliant",
                best_move="Nxe5",
                opponent_best_move="Qd4"
            )
            overlay.display_move(test_data)
            
            self.statusBar().showMessage("Test overlay displayed", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Test Failed", f"❌ Could not display overlay: {e}")
    
    def open_config_folder(self):
        """Open config folder in file explorer"""
        import os
        import subprocess
        import platform
        
        config_dir = "overlay"
        
        if platform.system() == "Windows":
            os.startfile(config_dir)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", config_dir])
        else:  # Linux
            subprocess.Popen(["xdg-open", config_dir])


def main():
    """Run configuration editor"""
    app = QApplication(sys.argv)
    editor = ConfigEditor()
    editor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()