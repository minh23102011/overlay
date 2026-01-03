"""
Enhanced PyQt6 Overlay Window with Drag-and-Drop Positioning
Supports custom icons, animations, and persistent position saving
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette, QIcon
from overlay.config import get_config, save_config
from overlay.models import MoveDisplayData

class DraggableOverlay(QWidget):
    """
    Frameless, draggable overlay window for displaying chess move analysis
    """
    
    position_changed = pyqtSignal(int, int)  # Emits when position changes
    
    def __init__(self):
        super().__init__()
        self.config = get_config()
        self.dragging = False
        self.drag_position = QPoint()
        self.current_data = None
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self._auto_hide)
        
        self._init_ui()
        self._load_position()
        
    def _init_ui(self):
        """Initialize the UI components"""
        # Window flags for frameless, always-on-top overlay
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        if not self.config.always_on_top:
            flags = Qt.WindowType.FramelessWindowHint
        
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set window size
        self.setFixedSize(self.config.overlay_width, self.config.overlay_height)
        
        # Main container
        self.container = QFrame(self)
        self.container.setObjectName("container")
        self.container.setGeometry(0, 0, self.config.overlay_width, self.config.overlay_height)
        
        # Layout
        main_layout = QVBoxLayout(self.container)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # === HEADER (Icon + Label) ===
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)
        
        # Icon label
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(self.config.icon_size, self.config.icon_size)
        self.icon_label.setScaledContents(True)
        header_layout.addWidget(self.icon_label)
        
        # Move quality label
        self.quality_label = QLabel()
        self.quality_label.setFont(QFont("Arial", self.config.font_size + 8, QFont.Weight.Bold))
        self.quality_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(self.quality_label, 1)
        
        main_layout.addLayout(header_layout)
        
        # === BEST MOVE SECTION ===
        self.best_move_container = QFrame()
        self.best_move_container.setObjectName("moveContainer")
        best_move_layout = QVBoxLayout(self.best_move_container)
        best_move_layout.setContentsMargins(15, 10, 15, 10)
        best_move_layout.setSpacing(5)
        
        self.best_move_title = QLabel()
        self.best_move_title.setFont(QFont("Arial", self.config.font_size - 2, QFont.Weight.Bold))
        best_move_layout.addWidget(self.best_move_title)
        
        self.best_move_label = QLabel()
        self.best_move_label.setFont(QFont("Consolas", self.config.font_size + 6, QFont.Weight.Bold))
        best_move_layout.addWidget(self.best_move_label)
        
        main_layout.addWidget(self.best_move_container)
        
        # === OPPONENT'S BEST SECTION ===
        self.opp_move_container = QFrame()
        self.opp_move_container.setObjectName("moveContainer")
        opp_move_layout = QVBoxLayout(self.opp_move_container)
        opp_move_layout.setContentsMargins(15, 10, 15, 10)
        opp_move_layout.setSpacing(5)
        
        self.opp_move_title = QLabel()
        self.opp_move_title.setFont(QFont("Arial", self.config.font_size - 2, QFont.Weight.Bold))
        opp_move_layout.addWidget(self.opp_move_title)
        
        self.opp_move_label = QLabel()
        self.opp_move_label.setFont(QFont("Consolas", self.config.font_size + 4, QFont.Weight.Bold))
        opp_move_layout.addWidget(self.opp_move_label)
        
        main_layout.addWidget(self.opp_move_container)
        
        # Add stretch to push content to top
        main_layout.addStretch()
        
        # Apply theme
        self._apply_theme()
        
        # Initially hidden
        self.hide()
    
    def _apply_theme(self):
        """Apply theme colors and styling"""
        if self.config.theme == "dark":
            bg_color = f"rgba(20, 20, 20, {int(self.config.opacity * 255)})"
            text_color = "#FFFFFF"
            container_bg = "rgba(40, 40, 40, 200)"
        elif self.config.theme == "light":
            bg_color = f"rgba(240, 240, 240, {int(self.config.opacity * 255)})"
            text_color = "#000000"
            container_bg = "rgba(255, 255, 255, 200)"
        else:  # transparent
            bg_color = f"rgba(0, 0, 0, {int(self.config.opacity * 128)})"
            text_color = "#FFFFFF"
            container_bg = "rgba(30, 30, 30, 150)"
        
        blur_effect = "background: rgba(20, 20, 20, 0.8); backdrop-filter: blur(10px);" if self.config.blur_background else ""
        
        self.container.setStyleSheet(f"""
            QFrame#container {{
                background: {bg_color};
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.1);
                {blur_effect}
            }}
            QFrame#moveContainer {{
                background: {container_bg};
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }}
            QLabel {{
                color: {text_color};
                background: transparent;
            }}
        """)
    
    def _get_icon_path(self, label: str) -> str:
        """Get icon path for move quality label"""
        icon_map = {
            "brilliant": "brilliant.png",
            "best": "best.png",
            "excellent": "excellent.png",
            "good": "good.png",
            "inaccuracy": "inaccuracy.png",
            "mistake": "mistake.png",
            "blunder": "blunder.png",
            "forced": "forced.png"
        }
        
        icon_filename = icon_map.get(label, "good.png")
        assets_path = Path(__file__).parent / "assets" / icon_filename
        
        if assets_path.exists():
            return str(assets_path)
        else:
            # Fallback to placeholder if icon not found
            return ""
    
    def _get_color_gradient(self, label: str) -> str:
        """Get color gradient for move quality"""
        gradients = {
            "brilliant": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #06b6d4, stop:0.5 #3b82f6, stop:1 #9333ea)",
            "best": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #22c55e, stop:1 #10b981)",
            "excellent": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #14b8a6, stop:1 #06b6d4)",
            "good": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #84cc16, stop:1 #22c55e)",
            "inaccuracy": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #facc15, stop:1 #f97316)",
            "mistake": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f97316, stop:1 #dc2626)",
            "blunder": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #dc2626, stop:1 #9f1239)",
            "forced": "qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #9ca3af, stop:1 #6b7280)"
        }
        return gradients.get(label, gradients["good"])
    
    def display_move(self, data: MoveDisplayData):
        """Display move analysis data with animation"""
        self.current_data = data
        
        # Stop any existing hide timer
        self.hide_timer.stop()
        
        # Update icon
        icon_path = self._get_icon_path(data.label)
        if icon_path and os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            self.icon_label.setPixmap(pixmap)
        else:
            # Use colored square as fallback
            self.icon_label.setText("")
        
        # Update quality label with gradient
        label_text = self.config.labels.get(data.label, data.label.upper())
        gradient = self._get_color_gradient(data.label)
        self.quality_label.setText(label_text)
        self.quality_label.setStyleSheet(f"""
            QLabel {{
                background: {gradient};
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;
            }}
        """)
        
        # Update best move
        if data.best_move and self.config.show_best_move:
            self.best_move_title.setText(self.config.labels.get("engine_suggests", "ENGINE SUGGESTS"))
            self.best_move_label.setText(data.best_move)
            self.best_move_container.show()
        else:
            self.best_move_container.hide()
        
        # Update opponent's best move
        if data.opponent_best_move and self.config.show_opponent_best:
            self.opp_move_title.setText(self.config.labels.get("opponent_best", "OPPONENT'S BEST"))
            self.opp_move_label.setText(data.opponent_best_move)
            self.opp_move_container.show()
        else:
            self.opp_move_container.hide()
        
        # Show with animation
        self._animate_show()
        
        # Set auto-hide timer if configured
        if self.config.auto_hide_delay > 0:
            self.hide_timer.start(self.config.auto_hide_delay)
    
    def _animate_show(self):
        """Animate overlay appearance"""
        self.show()
        
        # Fade in animation
        self.setWindowOpacity(0)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(int(300 / self.config.animation_speed))
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.config.opacity)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
        
        # Slide up animation
        start_pos = self.pos()
        self.move(start_pos.x(), start_pos.y() + 30)
        
        self.pos_animation = QPropertyAnimation(self, b"pos")
        self.pos_animation.setDuration(int(400 / self.config.animation_speed))
        self.pos_animation.setStartValue(self.pos())
        self.pos_animation.setEndValue(start_pos)
        self.pos_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.pos_animation.start()
    
    def _animate_hide(self):
        """Animate overlay disappearance"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(int(400 / self.config.animation_speed))
        self.animation.setStartValue(self.config.opacity)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self.hide)
        self.animation.start()
    
    def _auto_hide(self):
        """Auto-hide the overlay after delay"""
        self._animate_hide()
    
    # === DRAG AND DROP FUNCTIONALITY ===
    
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        if event.button() == Qt.MouseButton.LeftButton and not self.config.lock_position:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            
            # Change cursor to indicate dragging
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging"""
        if self.dragging and not self.config.lock_position:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            self.move(new_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release to stop dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            
            # Save new position
            self._save_position()
            
            # Emit signal
            pos = self.pos()
            self.position_changed.emit(pos.x(), pos.y())
            
            event.accept()
    
    def _save_position(self):
        """Save current window position to config"""
        pos = self.pos()
        self.config.position_x = pos.x()
        self.config.position_y = pos.y()
        save_config()
        print(f"💾 Overlay position saved: ({pos.x()}, {pos.y()})")
    
    def _load_position(self):
        """Load window position from config"""
        self.move(self.config.position_x, self.config.position_y)
        print(f"📍 Overlay position loaded: ({self.config.position_x}, {self.config.position_y})")
    
    def reset_position(self):
        """Reset position to default (center of screen)"""
        # Get screen geometry
        screen = self.screen().geometry()
        
        # Calculate center position
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        
        self.move(x, y)
        self._save_position()
        print(f"🔄 Overlay position reset to center: ({x}, {y})")


# === GLOBAL OVERLAY INSTANCE ===
_overlay_instance = None

def get_overlay() -> DraggableOverlay:
    """Get or create the global overlay instance"""
    global _overlay_instance
    if _overlay_instance is None:
        _overlay_instance = DraggableOverlay()
    return _overlay_instance


# === TEST CODE ===
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    overlay = get_overlay()
    
    # Test display
    test_data = MoveDisplayData(
        label="brilliant",
        best_move="Nxe5",
        opponent_best_move="Qd4"
    )
    
    overlay.display_move(test_data)
    
    sys.exit(app.exec())