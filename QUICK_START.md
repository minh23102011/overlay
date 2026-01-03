# 🚀 Quick Start Guide - Fix Your Setup Now

## Current Issue

You're seeing this error:
```
❌ Could not display overlay: cannot import name 'MoveDisplayData' from overlay.models
```

This means `overlay/models.py` is missing or incomplete.

---

## ✅ Immediate Fix (3 Steps)

### **Step 1: Create Required Files**

Create these 6 files in your `overlay/` folder:

#### **1. `overlay/models.py`**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class MoveDisplayData:
    label: str
    best_move: str
    opponent_best_move: Optional[str] = None
    evaluation: Optional[int] = None
    depth: Optional[int] = None
    
    def __post_init__(self):
        valid_labels = ["brilliant", "best", "excellent", "good", "inaccuracy", "mistake", "blunder", "forced"]
        if self.label not in valid_labels:
            raise ValueError(f"Invalid label: {self.label}")
```

#### **2. `overlay/__init__.py`**
```python
from overlay.models import MoveDisplayData
from overlay.dispatcher import dispatch_data, init_dispatcher
from overlay.config import get_config, save_config

__all__ = ['MoveDisplayData', 'dispatch_data', 'init_dispatcher', 'get_config', 'save_config']
```

#### **3-6. Copy from Artifacts**
- `config.py` (from artifact #2)
- `window.py` (from artifact #3)
- `dispatcher.py` (from artifact #4)
- `config_gui.py` (from artifact #10)

---

### **Step 2: Create Assets Folder**

```bash
mkdir overlay/assets
```

Download or create 8 PNG icons (64x64px, transparent):
- `brilliant.png` - ⭐ Sparkle/star
- `best.png` - 👑 Crown
- `excellent.png` - 📈 Up arrow
- `good.png` - 👍 Thumbs up
- `inaccuracy.png` - ⚠️ Warning
- `mistake.png` - ❌ X mark
- `blunder.png` - 💀 Skull
- `forced.png` - ⚡ Lightning

**Quick Icon Resources**:
- [Flaticon](https://www.flaticon.com) - Free icons
- [Material Icons](https://fonts.google.com/icons) - Google icons
- [FontAwesome](https://fontawesome.com) - Icon library

---

### **Step 3: Verify Setup**

Run the verification script:

```bash
python verify_setup.py
```

This will check:
- ✅ All required files exist
- ✅ All imports work
- ✅ Assets folder has icons
- ✅ Configuration loads correctly

---

## 🧪 Test Your Setup

### **Test 1: Simple Overlay Test**

```bash
python test_overlay_simple.py
```

This should:
1. Display 8 different move types
2. Cycle through them every 6 seconds
3. Allow you to drag the overlay
4. Save position when you release

### **Test 2: Configuration GUI**

```bash
python -m overlay.config_gui
```

This should:
1. Open the configuration window
2. Show all settings tabs
3. Allow you to click "Test Overlay" button
4. Display a test move

---

## 🔧 Common Issues & Fixes

### **Issue 1: "No module named 'PyQt6'"**

**Fix:**
```bash
pip install PyQt6
```

### **Issue 2: "No module named 'overlay.models'"**

**Fix:** Ensure `overlay/models.py` exists with the code above

### **Issue 3: Icons not showing**

**Fix:** 
- Create `overlay/assets/` folder
- Add PNG files (exact names: `brilliant.png`, `best.png`, etc.)
- Files must be 64x64px or similar size

### **Issue 4: Config file error**

**Fix:** Delete and regenerate:
```bash
rm overlay/overlay_config.json
python -m overlay.config_gui
```

### **Issue 5: Overlay not draggable**

**Fix:** Check config:
```json
{
  "lock_position": false
}
```

---

## 📁 Correct File Structure

```
your_project/
├── main.py
├── verify_setup.py         # NEW
├── test_overlay_simple.py  # NEW
└── overlay/
    ├── __init__.py         # NEW/UPDATED
    ├── models.py           # NEW
    ├── config.py           # NEW
    ├── window.py           # NEW
    ├── dispatcher.py       # UPDATED
    ├── config_gui.py       # NEW
    ├── overlay_config.json # AUTO-GENERATED
    └── assets/             # NEW
        ├── brilliant.png
        ├── best.png
        ├── excellent.png
        ├── good.png
        ├── inaccuracy.png
        ├── mistake.png
        ├── blunder.png
        └── forced.png
```

---

## 🎯 Full Integration with main.py

Once setup is verified, update `main.py`:

```python
def main():
    qt_app = QApplication(sys.argv)
    
    # Initialize dispatcher (CRITICAL - must be on main thread)
    from overlay.dispatcher import init_dispatcher
    init_dispatcher()
    
    # Load config
    from overlay.config import get_config
    config = get_config()
    print(f"📋 Overlay Config: {config.language}, {config.theme}, {config.overlay_width}x{config.overlay_height}")
    
    # ... rest of your code ...
    
    sys.exit(qt_app.exec())
```

Keep your existing dispatch code:
```python
# In analyse_job() - NO CHANGES NEEDED
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

## 🌟 Customization Quick Tips

### **Change Language to Vietnamese**

Edit `overlay/overlay_config.json`:
```json
{
  "language": "vi"
}
```

Or use GUI: Language tab → Select "vi - Tiếng Việt"

### **Change Theme**

```json
{
  "theme": "dark"  // or "light" or "transparent"
}
```

### **Make Overlay Larger**

```json
{
  "overlay_width": 500,
  "overlay_height": 300,
  "icon_size": 48,
  "font_size": 20
}
```

### **Add Country Filter**

```json
{
  "allowed_countries": ["VN", "US", "GB"]
}
```

---

## ✅ Success Checklist

- [ ] Created `overlay/models.py`
- [ ] Created `overlay/__init__.py`
- [ ] Created `overlay/config.py`
- [ ] Created `overlay/window.py`
- [ ] Updated `overlay/dispatcher.py`
- [ ] Created `overlay/config_gui.py`
- [ ] Created `overlay/assets/` folder
- [ ] Added 8 PNG icon files
- [ ] Ran `python verify_setup.py` ✅
- [ ] Ran `python test_overlay_simple.py` ✅
- [ ] Ran `python -m overlay.config_gui` ✅
- [ ] Updated `main.py` with init_dispatcher()
- [ ] Tested with `python main.py` ✅

---

## 🆘 Still Having Issues?

1. **Run verification**: `python verify_setup.py`
2. **Check Python version**: Python 3.8+ required
3. **Check PyQt6**: `pip list | grep PyQt6`
4. **Check file permissions**: Ensure you can read/write in overlay/
5. **Check import path**: Run `python -c "import overlay.models"`

If verification passes but overlay still doesn't work:
- Check terminal output for error messages
- Try test script: `python test_overlay_simple.py`
- Check if main.py calls `init_dispatcher()`

---

## 🎉 Next Steps After Setup

1. ✅ Customize appearance in config GUI
2. ✅ Add your preferred language
3. ✅ Position overlay where you want it
4. ✅ Test with Chess.com games
5. ✅ Enjoy your professional overlay!

---

**Your overlay system is now ready! 🏆♟️**