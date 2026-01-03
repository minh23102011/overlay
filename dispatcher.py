"""
Enhanced Thread-Safe Dispatcher for Overlay Updates
Integrates with new configuration system and draggable overlay
"""

from PyQt6.QtCore import QObject, pyqtSignal
from overlay.models import MoveDisplayData
from overlay.config import get_config
import threading

class OverlayDispatcher(QObject):
    """
    Thread-safe dispatcher for sending move data to overlay
    Uses Qt signals to ensure UI updates happen on main thread
    """
    
    # Signal emitted when new move data arrives
    move_received = pyqtSignal(MoveDisplayData)
    
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._overlay = None
        self._connected = False
        
    def connect_overlay(self):
        """Connect signal to overlay window (must be called from main thread)"""
        if self._connected:
            return
        
        from overlay.window import get_overlay
        
        self._overlay = get_overlay()
        self.move_received.connect(self._overlay.display_move)
        self._connected = True
        
        print("✅ Dispatcher connected to overlay")
    
    def dispatch(self, data: MoveDisplayData):
        """
        Dispatch move data to overlay (thread-safe)
        Can be called from any thread
        """
        with self._lock:
            # Check country filter if applicable
            config = get_config()
            
            # You can add country checking here if move data includes player info
            # For now, we'll just dispatch to overlay
            
            if not self._connected:
                print("⚠️  Dispatcher not connected to overlay yet")
                return
            
            # Emit signal (will be handled on main thread)
            self.move_received.emit(data)
            
            print(f"📤 Dispatched: {data.label} | Best: {data.best_move} | Opp: {data.opponent_best_move}")


# === GLOBAL DISPATCHER INSTANCE ===
_dispatcher_instance = None
_dispatcher_lock = threading.Lock()


def _get_dispatcher() -> OverlayDispatcher:
    """Get or create the global dispatcher instance (thread-safe singleton)"""
    global _dispatcher_instance
    
    with _dispatcher_lock:
        if _dispatcher_instance is None:
            _dispatcher_instance = OverlayDispatcher()
            print("✅ Dispatcher created")
        
        return _dispatcher_instance


def dispatch_data(data: MoveDisplayData):
    """
    Public API: Dispatch move data to overlay
    Thread-safe, can be called from any thread
    """
    dispatcher = _get_dispatcher()
    dispatcher.dispatch(data)


def init_dispatcher():
    """
    Initialize dispatcher and connect to overlay
    MUST be called from main thread (Qt UI thread)
    """
    dispatcher = _get_dispatcher()
    dispatcher.connect_overlay()


# === TEST CODE ===
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    import time
    
    app = QApplication(sys.argv)
    
    # Initialize dispatcher (on main thread)
    init_dispatcher()
    
    # Simulate dispatching from background thread
    def test_dispatch():
        time.sleep(1)
        
        test_moves = [
            MoveDisplayData("brilliant", "Nxe5", "Qd4"),
            MoveDisplayData("best", "e4", "Nc6"),
            MoveDisplayData("inaccuracy", "Qh5", "Nf6"),
            MoveDisplayData("blunder", "Ke2", "Qxf2#")
        ]
        
        for move_data in test_moves:
            dispatch_data(move_data)
            time.sleep(3)
    
    # Start test in background thread
    threading.Thread(target=test_dispatch, daemon=True).start()
    
    sys.exit(app.exec())