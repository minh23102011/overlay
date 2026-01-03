# overlay/window.py
import os
import json
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QPoint

from overlay import config
from overlay.models import LABEL_META

_window = None


def ensure_window():
    global _window
    if _window is None:
        _window = OverlayWindow()
    return _window


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self._init_ui()
        self._restore_position()

    # ================= UI =================

    def _init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedWidth(config.CARD_WIDTH)

        self.root = QWidget(self)
        self.root.setObjectName("card")

        r, g, b, a = config.CARD_BG_RGBA
        self.root.setStyleSheet(
            f"""
            QWidget#card {{
                background-color: rgba({r}, {g}, {b}, {a});
                border-radius: {config.CARD_RADIUS}px;
            }}
            """
        )

        main = QHBoxLayout(self.root)
        main.setContentsMargins(
            config.PADDING_LEFT,
            config.PADDING_TOP,
            config.PADDING_RIGHT,
            config.PADDING_BOTTOM,
        )
        main.setSpacing(config.CONTENT_SPACING)

        self.icon = QLabel()
        self.icon.setFixedSize(config.ICON_SIZE, config.ICON_SIZE)
        self.icon.setScaledContents(True)
        self.icon.setStyleSheet("background: transparent;")

        text_layout = QVBoxLayout()
        text_layout.setSpacing(config.TEXT_SPACING)

        self.title = QLabel()
        title_font = QFont()
        title_font.setPointSize(config.TITLE_FONT_SIZE)
        title_font.setBold(config.TITLE_BOLD)
        self.title.setFont(title_font)
        self.title.setStyleSheet("background: transparent; color: %s;" % config.TEXT_COLOR)

        self.subtitle = QLabel()
        sub_font = QFont()
        sub_font.setPointSize(config.SUBTITLE_FONT_SIZE)
        self.subtitle.setFont(sub_font)
        self.subtitle.setStyleSheet("background: transparent; color: %s;" % config.SUBTEXT_COLOR)

        text_layout.addWidget(self.title)
        text_layout.addWidget(self.subtitle)

        main.addWidget(self.icon)
        main.addLayout(text_layout)

        wrapper = QVBoxLayout(self)
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.addWidget(self.root)

    # ================= UPDATE =================

    def update_eval(self, label: str, best_move: str):
        label = label.lower()

        # ⛔ FILTER THEO CONFIG
        if not config.ENABLED_LABELS.get(label, False):
            return

        meta = LABEL_META.get(label)
        if not meta:
            return

        icon_path = os.path.join(config.ASSETS_DIR, meta.icon)
        if os.path.exists(icon_path):
            self.icon.setPixmap(QPixmap(icon_path))

        if config.SHOW_LABEL:
            self.title.setText(meta.title)
            self.title.show()
        else:
            self.title.hide()

        if config.SHOW_BEST_MOVE:
            self.subtitle.setText(f"{config.BEST_MOVE_PREFIX} {best_move}")
            self.subtitle.show()
        else:
            self.subtitle.hide()

        self._apply_size()
        self.show()
        self.raise_()

    def _apply_size(self):
        height = config.BASE_HEIGHT
        if config.SHOW_LABEL:
            height += config.TITLE_HEIGHT
        if config.SHOW_BEST_MOVE:
            height += config.SUBTITLE_HEIGHT
        height += config.PADDING_TOP + config.PADDING_BOTTOM
        self.setFixedHeight(height)

    # ================= DRAG + SAVE =================

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, e):
        if self._drag_pos:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None
        self._save_position()

    def _save_position(self):
        try:
            with open(config.STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({"x": self.x(), "y": self.y()}, f)
        except Exception:
            pass

    def _restore_position(self):
        try:
            if os.path.exists(config.STATE_FILE):
                with open(config.STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.move(QPoint(data["x"], data["y"]))
        except Exception:
            pass
