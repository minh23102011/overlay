# overlay/config.py
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# ================= CARD =================
CARD_WIDTH = 360
CARD_RADIUS = 18

PADDING_LEFT = 18
PADDING_TOP = 14
PADDING_RIGHT = 18
PADDING_BOTTOM = 14

CONTENT_SPACING = 14
TEXT_SPACING = 6

# ================= COLORS =================
CARD_BG_RGBA = (123, 156, 79, 80)   # RGBA
TEXT_COLOR = "#FFFFFF"
SUBTEXT_COLOR = "#DDDDDD"

# ================= ICON =================
ICON_SIZE = 82

# ================= TEXT =================
TITLE_FONT_SIZE = 26
TITLE_BOLD = True
SUBTITLE_FONT_SIZE = 14

# ================= FEATURE TOGGLES =================
# Ẩn / hiện title (GOOD / BLUNDER / …)
SHOW_LABEL = True

# Ẩn / hiện dòng Best move
SHOW_BEST_MOVE = True
BEST_MOVE_PREFIX = "Best move:"

# ================= LABEL FILTER (QUAN TRỌNG) =================
# False → overlay KHÔNG HIỆN nước đó (bỏ qua hoàn toàn)
ENABLED_LABELS = {
    "best": True,
    "brilliant": True,
    "excellent": True,
    "great": True,
    "good": True,

    "theory": True,
    "inaccuracy": True,
    "miss": True,

    "mistake": True,
    "blunder": True,

    "forced": True,
}

# ================= AUTO SIZE =================
BASE_HEIGHT = 40
TITLE_HEIGHT = 32
SUBTITLE_HEIGHT = 20

# ================= POSITION =================
STATE_FILE = os.path.join(BASE_DIR, "overlay_state.json")

#CARD_BG_RGBA = (123, 156, 79, 80)