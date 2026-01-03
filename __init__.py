"""
Chess Overlay Package
Provides visual overlay for chess move analysis
"""

from overlay.models import MoveDisplayData
from overlay.dispatcher import dispatch_data, init_dispatcher
from overlay.config import get_config, save_config, reload_config, OverlayConfig

__all__ = [
    'MoveDisplayData',
    'dispatch_data',
    'init_dispatcher',
    'get_config',
    'save_config',
    'reload_config',
    'OverlayConfig'
]

__version__ = '2.0.0'