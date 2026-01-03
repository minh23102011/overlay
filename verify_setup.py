"""
Setup Verification Script
Checks if all overlay components are properly installed
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def check_import(module_name, item_name=None):
    """Check if a module or item can be imported"""
    try:
        if item_name:
            exec(f"from {module_name} import {item_name}")
            print(f"✅ Can import: from {module_name} import {item_name}")
        else:
            exec(f"import {module_name}")
            print(f"✅ Can import: {module_name}")
        return True
    except ImportError as e:
        if item_name:
            print(f"❌ Cannot import from {module_name} import {item_name}: {e}")
        else:
            print(f"❌ Cannot import {module_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Error importing: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 70)
    print("🔍 CHESS OVERLAY - SETUP VERIFICATION")
    print("=" * 70)
    print()
    
    all_good = True
    
    # Check Python version
    print("📌 Python Version")
    print(f"   {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8+ recommended")
    print()
    
    # Check required files
    print("📁 Required Files")
    files = [
        ("overlay/__init__.py", "Package init"),
        ("overlay/models.py", "Data models"),
        ("overlay/config.py", "Configuration system"),
        ("overlay/dispatcher.py", "Event dispatcher"),
        ("overlay/window.py", "Overlay window"),
        ("overlay/config_gui.py", "Configuration GUI"),
    ]
    
    for filepath, desc in files:
        if not check_file_exists(filepath, desc):
            all_good = False
    print()
    
    # Check assets folder
    print("🎨 Assets Folder")
    assets_dir = "overlay/assets"
    if os.path.exists(assets_dir):
        print(f"✅ Assets folder exists: {assets_dir}")
        
        required_icons = [
            "brilliant.png", "best.png", "excellent.png", "good.png",
            "inaccuracy.png", "mistake.png", "blunder.png", "forced.png"
        ]
        
        missing_icons = []
        for icon in required_icons:
            icon_path = os.path.join(assets_dir, icon)
            if os.path.exists(icon_path):
                print(f"   ✅ {icon}")
            else:
                print(f"   ❌ MISSING: {icon}")
                missing_icons.append(icon)
        
        if missing_icons:
            print(f"\n⚠️  Missing {len(missing_icons)} icon(s). Create 64x64px PNG files.")
            all_good = False
    else:
        print(f"❌ Assets folder missing: {assets_dir}")
        print("   Create this folder and add 8 PNG icon files (64x64px)")
        all_good = False
    print()
    
    # Check imports
    print("📦 Python Imports")
    imports = [
        ("PyQt6.QtWidgets", "QApplication"),
        ("PyQt6.QtCore", "Qt"),
        ("PyQt6.QtGui", "QFont"),
        ("overlay.models", "MoveDisplayData"),
        ("overlay.config", "get_config"),
        ("overlay.dispatcher", "dispatch_data"),
        ("overlay.dispatcher", "init_dispatcher"),
    ]
    
    for module, item in imports:
        if not check_import(module, item):
            all_good = False
    print()
    
    # Check config file
    print("⚙️  Configuration File")
    config_path = "overlay/overlay_config.json"
    if os.path.exists(config_path):
        print(f"✅ Config file exists: {config_path}")
        try:
            from overlay.config import get_config
            config = get_config()
            print(f"   Language: {config.language}")
            print(f"   Theme: {config.theme}")
            print(f"   Size: {config.overlay_width}x{config.overlay_height}")
            print(f"   Position: ({config.position_x}, {config.position_y})")
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            all_good = False
    else:
        print(f"⚠️  Config file will be created on first run: {config_path}")
    print()
    
    # Final summary
    print("=" * 70)
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🚀 You can now run:")
        print("   1. python -m overlay.config_gui  (Configure settings)")
        print("   2. python main.py                 (Run chess analyzer)")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("📋 To-Do List:")
        print("   1. Ensure all Python files are in overlay/ folder")
        print("   2. Create overlay/assets/ folder")
        print("   3. Add 8 PNG icon files (64x64px) to assets/")
        print("   4. Install PyQt6: pip install PyQt6")
        print("   5. Run this script again to verify")
    print("=" * 70)

if __name__ == "__main__":
    main()