# overlay/test_overlay.py
import sys
import time
from PyQt6.QtWidgets import QApplication

from overlay.dispatcher import dispatch
from overlay import config

def main():
    app = QApplication(sys.argv)

    print("[test_overlay] ENABLED_LABELS =", config.ENABLED_LABELS)
    print("[test_overlay] SHOW_LABEL =", config.SHOW_LABEL)
    print("[test_overlay] SHOW_BEST_MOVE =", config.SHOW_BEST_MOVE)

    tests = [
        ("inaccuracy", "Nf3"),
        ("great", "e4"),
        ("theory", "h3"),
        ("excellent", "Qh5"),
        ("good", "g2g4"),
        ("mistake", "Qe2"),
        ("blunder", "f3"),
    ]

    for label, move in tests:
        print(f"[test_overlay] dispatch({label}, {move})")
        dispatch(label, move)
        app.processEvents()
        time.sleep(1.2)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
