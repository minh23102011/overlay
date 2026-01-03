"""
Simple Overlay Test
Tests overlay display without requiring full integration
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

def test_overlay():
    """Test the overlay with sample data"""
    
    print("🧪 Testing overlay...")
    
    try:
        # Import after Qt is initialized
        from overlay.models import MoveDisplayData
        from overlay.window import get_overlay
        
        # Create overlay
        overlay = get_overlay()
        print("✅ Overlay created successfully")
        
        # Test data
        test_moves = [
            ("brilliant", "Nxe5", "Qd4"),
            ("best", "e4", "Nc6"),
            ("excellent", "Bc4", "Bb4"),
            ("good", "O-O", "d5"),
            ("inaccuracy", "Qh5", "Nf6"),
            ("mistake", "f3", "Qh4+"),
            ("blunder", "Ke2", "Qxf2#"),
            ("forced", "Kg1", None)
        ]
        
        # Display moves with delay
        for i, (label, best, opp) in enumerate(test_moves):
            def show_move(l=label, b=best, o=opp):
                data = MoveDisplayData(l, b, o)
                overlay.display_move(data)
                print(f"📤 Displayed: {l} - {b}")
            
            QTimer.singleShot(i * 6000, show_move)
        
        print("✅ Test sequence started")
        print("💡 You should see 8 different move types displayed every 6 seconds")
        print("💡 Try dragging the overlay to move it")
        print("💡 The position will be saved automatically")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n📋 To fix:")
        print("1. Ensure overlay/models.py exists")
        print("2. Ensure overlay/window.py exists")
        print("3. Run: python verify_setup.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Chess Overlay - Simple Test")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Run test
    test_overlay()
    
    # Keep app running
    sys.exit(app.exec())