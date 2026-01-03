# 🚀 Implementation Guide - New Overlay System

## Overview

This guide will help you implement the new overlay architecture into your existing chess analysis project. The new system provides:

- ✅ **Draggable overlay** with persistent position saving
- ✅ **Multi-language support** (EN, VI, ES, FR, DE, RU, ZH)
- ✅ **Country filtering** for allowed/blocked regions
- ✅ **Customizable appearance** (icons, fonts, colors, themes)
- ✅ **Visual configuration editor** (no need to edit JSON manually)
- ✅ **Thread-safe architecture** for background analysis

---

## 📁 File Structure

Your overlay folder should look like this:

```
overlay/
├── assets/                    # NEW: Icon files
│   ├── brilliant.png
│   ├── best.png
│   ├── excellent.png
│   ├── good.png
│   ├── inaccuracy.png
│   ├── mistake.png
│   ├── blunder.png
│   └── forced.png
├── __init__.py
├── config.py                  # NEW: Configuration system
├── config_gui.py              # NEW: Visual editor
├── dispatcher.py              # UPDATED: Enhanced dispatcher
├── models.py                  # UNCHANGED
├── overlay_config.json        # NEW: Auto-generated config file
└── window.py                  # NEW: Draggable overlay window
```

---

## 🔧 Step 1: Update Your Files

### **1.1 Update `main.py`**

Replace the initialization section in your `main()` function:

```python
def main():
    """
    Initialize all systems with new overlay architecture
    """
    qt_app = QApplication(sys.argv)
    
    # ⭐ NEW: Initialize dispatcher on main thread
    from overlay.dispatcher import init_dispatcher
    init_dispatcher()
    
    # ⭐ NEW: Load and display configuration
    from overlay.config import get_config
    config = get_config()
    print(f"📋 Config: Language={config.language}, Theme={config.theme}, Size={config.overlay_width}x{config.overlay_height}")
    
    # UNCHANGED: Subscribe to store updates
    STORE.subscribe(on_new_fen)
    
    # UNCHANGED: Start receiver server
    print(f"📡 [RECEIVER] Starting server on http://127.0.0.1:8765/fen")
    threading.Thread(target=server.start, daemon=True).start()
    
    # UNCHANGED: Pre-warm engine
    def prewarm_engine():
        print("⚡ [ENGINE] Pre-warming Stockfish...")
        try:
            evaluate_position({
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "time_ms": 100
            })
            print("✅ [ENGINE] Ready!")
        except:
            print("⚠️  [ENGINE] Pre-warm failed (will start on first move)")
    
    threading.Thread(target=prewarm_engine, daemon=True).start()
    
    print("🚀 [MAIN] READY — Waiting for moves from Chess.com...")
    sys.exit(qt_app.exec())
```

### **1.2 Keep Existing Dispatch Code**

The dispatch code in `analyse_job()` **does NOT need to change**:

```python
# This code remains the same
from overlay.dispatcher import dispatch_data
from overlay.models import MoveDisplayData

move_data = MoveDisplayData(
    label=label,
    best_move=best_move_san,
    opponent_best_move=opponent_best_san
)

QTimer.singleShot(0, lambda: dispatch_data(move_data))
```

---

## 🎨 Step 2: Create Icon Assets

### **2.1 Download or Create Icons**

Create 8 PNG icons (64x64px recommended, transparent background):

1. **brilliant.png** - Sparkle/star icon (cyan/blue)
2. **best.png** - Crown or checkmark (green)
3. **excellent.png** - Upward arrow (teal)
4. **good.png** - Thumbs up (lime)
5. **inaccuracy.png** - Warning triangle (yellow)
6. **mistake.png** - X or cross (orange)
7. **blunder.png** - Skull or double exclamation (red)
8. **forced.png** - Lightning bolt (gray)

### **2.2 Place Icons**

```bash
overlay/assets/brilliant.png
overlay/assets/best.png
overlay/assets/excellent.png
overlay/assets/good.png
overlay/assets/inaccuracy.png
overlay/assets/mistake.png
overlay/assets/blunder.png
overlay/assets/forced.png
```

**Tip**: Use free icon resources like:
- [Flaticon](https://www.flaticon.com)
- [FontAwesome](https://fontawesome.com)
- [Material Icons](https://fonts.google.com/icons)

---

## ⚙️ Step 3: Configure Your Overlay

### **3.1 Option A: Use Visual Editor (Recommended)**

Run the configuration GUI:

```bash
python -m overlay.config_gui
```

This opens a visual editor where you can:
- Adjust icon size, font size, overlay dimensions
- Set position and locking options
- Choose language and theme
- Configure country filters
- Test the overlay in real-time

Click **"💾 Save Configuration"** when done.

### **3.2 Option B: Edit JSON Manually**

Edit `overlay/overlay_config.json`:

```json
{
  "icon_size": 40,
  "font_size": 18,
  "overlay_width": 450,
  "overlay_height": 280,
  "opacity": 0.95,
  "animation_speed": 1.0,
  
  "position_x": 100,
  "position_y": 100,
  "lock_position": false,
  "always_on_top": true,
  
  "show_best_move": true,
  "show_opponent_best": true,
  "show_evaluation": true,
  "auto_hide_delay": 5000,
  
  "language": "vi",
  "move_notation": "san",
  
  "allowed_countries": ["VN", "US", "GB"],
  "blocked_countries": [],
  "show_country_flags": true,
  
  "theme": "dark",
  "blur_background": true,
  "enable_sound": false
}
```

### **3.3 Vietnamese Language Example**

For Vietnamese interface:

```json
{
  "language": "vi",
  "labels": {
    "brilliant": "XUẤT SẮC!!",
    "best": "NƯỚC ĐI TỐT NHẤT",
    "excellent": "RẤT TỐT",
    "good": "TỐT",
    "inaccuracy": "KHÔNG CHÍNH XÁC",
    "mistake": "SAI LẦM",
    "blunder": "SAI LẦM LỚN!!",
    "forced": "BẮT BUỘC",
    "engine_suggests": "ĐỘNG CƠ ĐỀ XUẤT",
    "opponent_best": "ĐỐI THỦ TỐT NHẤT"
  }
}
```

---

## 🧪 Step 4: Test Your Setup

### **4.1 Test Overlay Display**

Create a test script `test_overlay.py`:

```python
from PyQt6.QtWidgets import QApplication
from overlay.dispatcher import init_dispatcher, dispatch_data
from overlay.models import MoveDisplayData
import sys
import time
import threading

def test():
    time.sleep(1)
    
    # Test different move types
    moves = [
        MoveDisplayData("brilliant", "Nxe5", "Qd4"),
        MoveDisplayData("best", "e4", "Nc6"),
        MoveDisplayData("excellent", "Bc4", "Bb4"),
        MoveDisplayData("good", "O-O", "d5"),
        MoveDisplayData("inaccuracy", "Qh5", "Nf6"),
        MoveDisplayData("mistake", "f3", "Qh4+"),
        MoveDisplayData("blunder", "Ke2", "Qxf2#"),
        MoveDisplayData("forced", "Kg1", None)
    ]
    
    for move in moves:
        print(f"Testing: {move.label}")
        dispatch_data(move)
        time.sleep(6)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_dispatcher()
    
    threading.Thread(target=test, daemon=True).start()
    
    sys.exit(app.exec())
```

Run it:

```bash
python test_overlay.py
```

You should see the overlay appear with different move classifications.

### **4.2 Test Dragging**

- Click and drag the overlay to move it
- Release to save the new position
- Restart the app - the position should be remembered

### **4.3 Test Configuration Editor**

```bash
python -m overlay.config_gui
```

Try changing settings and clicking "🧪 Test Overlay".

---

## 🎯 Step 5: Run Your Chess Analyzer

Now run your main application:

```bash
python main.py
```

The overlay should:
1. ✅ Load configuration from `overlay_config.json`
2. ✅ Display at the saved position
3. ✅ Show move analysis when you play on Chess.com
4. ✅ Use your chosen language and theme
5. ✅ Save position when you drag it

---

## 🔥 Advanced Usage

### **Country Filtering (Future Feature)**

Add player country detection to your FEN receiver, then check:

```python
from overlay.config import get_config

config = get_config()

if not config.is_country_allowed(player_country):
    print(f"❌ Player from {player_country} is not allowed")
    return
```

### **Dynamic Language Switching**

```python
from overlay.config import get_config, save_config

config = get_config()
config.language = "vi"  # Switch to Vietnamese
config.labels = config._get_default_labels()
save_config()

# Reload overlay to apply changes
from overlay.dispatcher import reload_config
reload_config()
```

### **Custom Themes**

Edit `window.py` → `_apply_theme()` to add custom color schemes:

```python
elif self.config.theme == "cyberpunk":
    bg_color = "rgba(0, 255, 255, 0.9)"
    text_color = "#FF00FF"
    container_bg = "rgba(255, 0, 255, 200)"
```

---

## 🐛 Troubleshooting

### **Problem: Overlay not showing**

**Solution**:
```python
# In main.py, ensure init_dispatcher() is called
from overlay.dispatcher import init_dispatcher
init_dispatcher()
```

### **Problem: Icons not loading**

**Solution**:
- Check files exist: `overlay/assets/brilliant.png`, etc.
- Use 64x64px PNG with transparent background
- File names must match exactly (case-sensitive)

### **Problem: Position not saving**

**Solution**:
- Check `lock_position` is `false` in config
- Ensure file permissions for `overlay/overlay_config.json`
- Drag and release mouse to trigger save

### **Problem: Language not changing**

**Solution**:
```bash
# Delete config and regenerate
rm overlay/overlay_config.json
python main.py  # Will create new config with defaults
```

---

## 📚 API Reference

### **Configuration**

```python
from overlay.config import get_config, save_config, reload_config

# Get current config
config = get_config()

# Modify settings
config.language = "vi"
config.icon_size = 48

# Validate
is_valid, error = config.validate()

# Save
save_config()

# Reload from file
reload_config()
```

### **Dispatcher**

```python
from overlay.dispatcher import init_dispatcher, dispatch_data
from overlay.models import MoveDisplayData

# Initialize (once, in main thread)
init_dispatcher()

# Dispatch (from any thread)
data = MoveDisplayData("brilliant", "Nxe5", "Qd4")
dispatch_data(data)
```

### **Overlay Window**

```python
from overlay.window import get_overlay

overlay = get_overlay()

# Show move
overlay.display_move(data)

# Reset position to center
overlay.reset_position()

# Hide
overlay.hide()
```

---

## 🎉 Congratulations!

You now have a fully functional, modern overlay system with:

- ✅ Drag-and-drop positioning
- ✅ Multi-language support
- ✅ Country filtering
- ✅ Visual configuration editor
- ✅ Custom icons and themes
- ✅ Persistent settings

**Next Steps**:
1. Customize your icons and colors
2. Add more languages if needed
3. Integrate country detection
4. Share your setup with others!

---

## 🤝 Need Help?

- Check `ARCHITECTURE.md` for technical details
- Run `python -m overlay.config_gui` for visual configuration
- Create an issue on GitHub if you encounter bugs

**Enjoy your enhanced chess overlay! ♟️✨**