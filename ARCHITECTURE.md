# Chess Overlay - New Architecture Documentation

## 🏗️ Architecture Overview

The new overlay system is a complete redesign with modern features, better configuration management, and enhanced user experience.

### **Key Components**

```
overlay/
├── assets/              # Icon files for move quality
│   ├── brilliant.png
│   ├── best.png
│   ├── excellent.png
│   ├── good.png
│   ├── inaccuracy.png
│   ├── mistake.png
│   ├── blunder.png
│   └── forced.png
├── config.py           # Configuration management system
├── window.py           # Enhanced draggable overlay window
├── dispatcher.py       # Thread-safe event dispatcher
├── models.py           # Data models (unchanged)
├── overlay_config.json # User configuration file
└── __init__.py         # Package initialization
```

---

## 🎯 Core Features

### **1. Configuration System (`config.py`)**

#### **Appearance Customization**
- `icon_size`: Icon size in pixels (16-64)
- `font_size`: Font size in pixels (10-32)
- `overlay_width`: Width in pixels (300-800)
- `overlay_height`: Height in pixels (200-600)
- `opacity`: Transparency level (0.0-1.0)
- `animation_speed`: Animation speed multiplier (0.5-2.0)

#### **Positioning**
- `position_x`, `position_y`: Screen coordinates
- `lock_position`: Disable dragging when `true`
- `always_on_top`: Keep overlay above other windows

#### **Display Options**
- `show_best_move`: Show engine's best move suggestion
- `show_opponent_best`: Show opponent's predicted response
- `show_evaluation`: Show centipawn evaluation
- `auto_hide_delay`: Auto-hide after N milliseconds (0 = never)

#### **Internationalization**
- `language`: UI language code (en, vi, es, fr, de, ru, zh)
- `move_notation`: 'san' (e4) or 'uci' (e2e4)
- `labels`: Customizable text labels per language

#### **Country Filtering**
- `allowed_countries`: Whitelist of ISO country codes (e.g., `["US", "GB", "VN"]`)
- `blocked_countries`: Blacklist of country codes
- `show_country_flags`: Display country flags for players

#### **Themes**
- `theme`: 'dark', 'light', or 'transparent'
- `blur_background`: Apply blur effect
- `enable_sound`: Play sound effects (future feature)

---

### **2. Draggable Overlay Window (`window.py`)**

#### **Features**
- ✅ **Drag-and-Drop Positioning**: Click and drag to move overlay
- ✅ **Persistent Position**: Automatically saves position to config
- ✅ **Smooth Animations**: Fade-in/out and slide-up effects
- ✅ **Custom Icons**: Uses PNG icons from `assets/` folder
- ✅ **Gradient Text**: Beautiful color gradients for move quality
- ✅ **Auto-Hide**: Automatically hides after configurable delay
- ✅ **Theme Support**: Dark, light, and transparent themes
- ✅ **Frameless Window**: Clean, modern appearance

#### **Usage**
```python
from overlay.window import get_overlay
from overlay.models import MoveDisplayData

overlay = get_overlay()

# Display a move
data = MoveDisplayData(
    label="brilliant",
    best_move="Nxe5",
    opponent_best_move="Qd4"
)
overlay.display_move(data)

# Reset position to screen center
overlay.reset_position()
```

---

### **3. Thread-Safe Dispatcher (`dispatcher.py`)**

#### **Purpose**
Safely dispatches move data from background analysis threads to the Qt UI thread.

#### **Features**
- ✅ **Thread-Safe**: Uses locks and Qt signals
- ✅ **Singleton Pattern**: Global instance accessible from anywhere
- ✅ **Country Filtering**: Can filter based on player country (extensible)
- ✅ **Auto-Connect**: Automatically connects to overlay window

#### **Usage**
```python
from overlay.dispatcher import dispatch_data, init_dispatcher
from overlay.models import MoveDisplayData

# Initialize in main thread (once at startup)
init_dispatcher()

# Dispatch from any thread (even background threads)
data = MoveDisplayData("best", "e4", "Nc6")
dispatch_data(data)
```

---

## 📋 Configuration Examples

### **Example 1: Vietnamese Language with Custom Countries**

```json
{
  "icon_size": 40,
  "font_size": 18,
  "overlay_width": 450,
  "language": "vi",
  "allowed_countries": ["VN", "US", "GB", "FR"],
  "theme": "dark",
  "labels": {
    "brilliant": "XUẤT SẮC!!",
    "best": "NƯỚC ĐI TỐT NHẤT",
    "excellent": "RẤT TỐT",
    "good": "TỐT",
    "inaccuracy": "KHÔNG CHÍNH XÁC",
    "mistake": "SAI LẦM",
    "blunder": "SAI LẦM LỚN!!",
    "forced": "BẮT BUỘC"
  }
}
```

### **Example 2: Minimal Overlay (Small, Fast)**

```json
{
  "icon_size": 24,
  "font_size": 12,
  "overlay_width": 300,
  "overlay_height": 180,
  "opacity": 0.8,
  "animation_speed": 2.0,
  "auto_hide_delay": 3000,
  "show_opponent_best": false,
  "theme": "transparent"
}
```

### **Example 3: Locked Position for Streaming**

```json
{
  "position_x": 50,
  "position_y": 50,
  "lock_position": true,
  "always_on_top": true,
  "auto_hide_delay": 4000,
  "theme": "dark"
}
```

---

## 🔄 Integration with Main.py

### **Updated `main.py` Initialization**

```python
def main():
    """
    Initialize all systems with new overlay architecture
    """
    qt_app = QApplication(sys.argv)
    
    # Initialize dispatcher on main thread
    from overlay.dispatcher import init_dispatcher
    init_dispatcher()
    
    # Load custom configuration
    from overlay.config import get_config
    config = get_config()
    print(f"📋 Loaded config: Language={config.language}, Theme={config.theme}")
    
    # Subscribe to store updates
    STORE.subscribe(on_new_fen)
    
    # Start receiver server
    threading.Thread(target=server.start, daemon=True).start()
    
    # Pre-warm engine
    threading.Thread(target=prewarm_engine, daemon=True).start()
    
    print("🚀 [MAIN] READY — Waiting for moves from Chess.com...")
    sys.exit(qt_app.exec())
```

### **Dispatch Move Data (No Changes Required)**

The existing code in `main.py` already works:

```python
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

## 🎨 Asset Requirements

### **Required Icons (PNG, Transparent Background)**

Place these files in `overlay/assets/`:

1. `brilliant.png` - Cyan/blue sparkle icon
2. `best.png` - Green crown or checkmark
3. `excellent.png` - Teal upward arrow
4. `good.png` - Lime thumbs up
5. `inaccuracy.png` - Yellow warning triangle
6. `mistake.png` - Orange X or cross
7. `blunder.png` - Red skull or exclamation
8. `forced.png` - Gray lightning bolt

**Recommended Size**: 64x64px (will be scaled based on `icon_size` config)

---

## 🚀 Quick Start Guide

### **1. Install Dependencies**

```bash
pip install PyQt6
```

### **2. Create Default Config**

```python
from overlay.config import OverlayConfig

config = OverlayConfig()
config.save()  # Creates overlay/overlay_config.json
```

### **3. Add Icons**

Place PNG icons in `overlay/assets/` folder.

### **4. Run the Application**

```bash
python main.py
```

### **5. Customize Settings**

Edit `overlay/overlay_config.json` to customize:
- Language
- Appearance
- Position
- Country filters

---

## 🌍 Supported Languages

- **English** (`en`)
- **Vietnamese** (`vi`)
- **Spanish** (`es`)
- **French** (`fr`)
- **German** (`de`)
- **Russian** (`ru`)
- **Chinese** (`zh`)

Add more languages by extending `_get_default_labels()` in `config.py`.

---

## 🔧 Advanced Usage

### **Programmatic Configuration**

```python
from overlay.config import get_config, save_config

# Get current config
config = get_config()

# Modify settings
config.language = "vi"
config.icon_size = 48
config.allowed_countries = ["VN", "US"]

# Validate
is_valid, error = config.validate()
if is_valid:
    save_config()
else:
    print(f"Invalid config: {error}")
```

### **Country Filtering**

```python
from overlay.config import get_config

config = get_config()

# Check if country is allowed
if config.is_country_allowed("VN"):
    print("Vietnam is allowed")
```

### **Reset to Defaults**

```python
from overlay.config import get_config, save_config

config = get_config()
config.reset_to_defaults()
save_config()
```

---

## 📊 Move Quality Classification

| Label | Centipawn Loss | Description |
|-------|----------------|-------------|
| **Brilliant** | Sacrifice with gain | Material sacrifice that improves position |
| **Best** | 0 to -20 cp | Engine's top choice or equivalent |
| **Excellent** | -20 to -50 cp | Very strong move |
| **Good** | -50 to -100 cp | Solid move |
| **Inaccuracy** | -100 to -300 cp | Suboptimal move |
| **Mistake** | -300 to -700 cp | Significant error |
| **Blunder** | -700+ cp | Critical error |
| **Forced** | N/A | Only legal move available |

---

## 🐛 Troubleshooting

### **Overlay Not Showing**

1. Check if dispatcher is initialized: `init_dispatcher()`
2. Verify config file exists: `overlay/overlay_config.json`
3. Ensure Qt application is running: `app.exec()`

### **Icons Not Loading**

1. Verify PNG files exist in `overlay/assets/`
2. Check file names match exactly (case-sensitive)
3. Use 64x64px transparent PNG images

### **Position Not Saving**

1. Check file permissions for `overlay/overlay_config.json`
2. Ensure `lock_position` is `false` in config
3. Drag overlay to new position and release mouse

### **Country Filter Not Working**

1. Use ISO 3166-1 alpha-2 country codes (e.g., "US", "VN")
2. Empty `allowed_countries` = allow all
3. `blocked_countries` takes precedence over `allowed_countries`

---

## 🎯 Future Enhancements

- [ ] Sound effects for different move qualities
- [ ] Multiple overlay profiles (switch between configs)
- [ ] Keyboard shortcuts for quick settings
- [ ] Integration with Twitch/OBS for streaming
- [ ] Statistical dashboard (move quality over time)
- [ ] Custom themes (user-defined color schemes)
- [ ] Mobile app companion

---

## 📝 License

This overlay system is part of the Chess Analysis Tool project.

---

## 🤝 Contributing

To add a new language:
1. Add translation in `config.py` → `_get_default_labels()`
2. Test with `config.language = "your_language_code"`
3. Submit pull request

To improve design:
1. Modify `window.py` → `_apply_theme()` or `_get_color_gradient()`
2. Add new icons to `assets/`
3. Update configuration schema if needed

---

**Built with ❤️ for chess players worldwide**