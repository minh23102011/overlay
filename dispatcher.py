# overlay/dispatcher.py
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import QApplication
from overlay.window import ensure_window


class _Dispatcher(QObject):
    update_requested = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.update_requested.connect(self._on_update)

    def _on_update(self, label: str, best_move: str):
        win = ensure_window()
        win.update_eval(label, best_move)


_dispatcher = None


def _get_dispatcher():
    global _dispatcher
    app = QApplication.instance()
    if not app:
        raise RuntimeError(
            "[overlay.dispatcher] QApplication chưa được tạo. "
            "Main phải tạo QApplication và chạy app.exec()."
        )

    if _dispatcher is None:
        _dispatcher = _Dispatcher()
        _dispatcher.moveToThread(app.thread())

    return _dispatcher


def dispatch(label: str, best_move: str):
    dispatcher = _get_dispatcher()

    if QThread.currentThread() == QApplication.instance().thread():
        dispatcher._on_update(label, best_move)
    else:
        dispatcher.update_requested.emit(label, best_move)
