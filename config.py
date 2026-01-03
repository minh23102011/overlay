"""
Enhanced Overlay Configuration System
Supports customization of appearance, positioning, and internationalization
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class OverlayConfig:
    """Configuration for the chess overlay system"""
    
    # === APPEARANCE ===
    icon_size: int = 32  # Icon size in pixels (16-64)
    font_size: int = 16  # Font size in pixels (10-32)
    overlay_width: int = 400  # Overlay width in pixels (300-800)
    overlay_height: int = 250  # Overlay height in pixels (200-600)
    opacity: float = 0.95  # Overlay opacity (0.0-1.0)
    animation_speed: float = 1.0  # Animation speed multiplier (0.5-2.0)
    
    # === POSITIONING ===
    position_x: int = 100  # X position on screen
    position_y: int = 100  # Y position on screen
    lock_position: bool = False  # Lock overlay position (disable dragging)
    always_on_top: bool = True  # Keep overlay above other windows
    
    # === DISPLAY OPTIONS ===
    show_best_move: bool = True  # Show engine's best move
    show_opponent_best: bool = True  # Show opponent's predicted response
    show_evaluation: bool = True  # Show centipawn evaluation
    auto_hide_delay: int = 5000  # Auto-hide after N milliseconds (0 = never)
    
    # === LANGUAGE & LOCALIZATION ===
    language: str = "en"  # UI language (en, vi, es, fr, de, ru, zh, etc.)
    move_notation: str = "san"  # Move notation: 'san' (e4) or 'uci' (e2e4)
    
    # === MOVE QUALITY LABELS (Customizable per language) ===
    labels: Dict[str, str] = None
    
    # === COUNTRY FILTER ===
    allowed_countries: list[str] = None  # List of ISO country codes (e.g., ["US", "GB", "VN"])
    blocked_countries: list[str] = None  # List of blocked country codes
    show_country_flags: bool = True  # Show country flags for players
    
    # === ADVANCED ===
    theme: str = "dark"  # Theme: 'dark', 'light', 'transparent'
    blur_background: bool = True  # Apply blur effect to overlay background
    enable_sound: bool = False  # Play sound effects for moves
    
    def __post_init__(self):
        """Initialize default labels if not provided"""
        if self.labels is None:
            self.labels = self._get_default_labels()
        if self.allowed_countries is None:
            self.allowed_countries = []  # Empty = allow all
        if self.blocked_countries is None:
            self.blocked_countries = []
    
    def _get_default_labels(self) -> Dict[str, str]:
        """Get default labels based on language"""
        labels_by_language = {
            "en": {
                "brilliant": "BRILLIANT!!",
                "best": "BEST MOVE",
                "excellent": "EXCELLENT",
                "good": "GOOD",
                "inaccuracy": "INACCURACY",
                "mistake": "MISTAKE",
                "blunder": "BLUNDER!!",
                "forced": "FORCED",
                "engine_suggests": "ENGINE SUGGESTS",
                "opponent_best": "OPPONENT'S BEST"
            },
            "vi": {
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
            },
            "es": {
                "brilliant": "¡¡BRILLANTE!!",
                "best": "MEJOR JUGADA",
                "excellent": "EXCELENTE",
                "good": "BUENA",
                "inaccuracy": "IMPRECISIÓN",
                "mistake": "ERROR",
                "blunder": "¡¡GRAVE ERROR!!",
                "forced": "FORZADA",
                "engine_suggests": "EL MOTOR SUGIERE",
                "opponent_best": "MEJOR DEL OPONENTE"
            },
            "fr": {
                "brilliant": "BRILLANT!!",
                "best": "MEILLEUR COUP",
                "excellent": "EXCELLENT",
                "good": "BON",
                "inaccuracy": "IMPRÉCISION",
                "mistake": "ERREUR",
                "blunder": "GAFFE!!",
                "forced": "FORCÉ",
                "engine_suggests": "LE MOTEUR SUGGÈRE",
                "opponent_best": "MEILLEUR DE L'ADVERSAIRE"
            },
            "de": {
                "brilliant": "BRILLANT!!",
                "best": "BESTER ZUG",
                "excellent": "AUSGEZEICHNET",
                "good": "GUT",
                "inaccuracy": "UNGENAUIGKEIT",
                "mistake": "FEHLER",
                "blunder": "GROBER FEHLER!!",
                "forced": "ERZWUNGEN",
                "engine_suggests": "ENGINE SCHLÄGT VOR",
                "opponent_best": "GEGNERS BESTE"
            },
            "ru": {
                "brilliant": "БЛЕСТЯЩЕ!!",
                "best": "ЛУЧШИЙ ХОД",
                "excellent": "ОТЛИЧНО",
                "good": "ХОРОШО",
                "inaccuracy": "НЕТОЧНОСТЬ",
                "mistake": "ОШИБКА",
                "blunder": "ГРУБАЯ ОШИБКА!!",
                "forced": "ВЫНУЖДЕННЫЙ",
                "engine_suggests": "ДВИЖОК ПРЕДЛАГАЕТ",
                "opponent_best": "ЛУЧШИЙ ХОД ПРОТИВНИКА"
            },
            "zh": {
                "brilliant": "精彩!!",
                "best": "最佳着法",
                "excellent": "优秀",
                "good": "良好",
                "inaccuracy": "不精确",
                "mistake": "失误",
                "blunder": "大错!!",
                "forced": "被迫",
                "engine_suggests": "引擎建议",
                "opponent_best": "对手最佳"
            }
        }
        
        return labels_by_language.get(self.language, labels_by_language["en"])
    
    def is_country_allowed(self, country_code: str) -> bool:
        """Check if a country is allowed to use the overlay"""
        # If blocked list has entries and country is in it, reject
        if self.blocked_countries and country_code in self.blocked_countries:
            return False
        
        # If allowed list is empty, allow all (except blocked)
        if not self.allowed_countries:
            return True
        
        # Check if country is in allowed list
        return country_code in self.allowed_countries
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate configuration values"""
        if not 16 <= self.icon_size <= 64:
            return False, "icon_size must be between 16 and 64"
        
        if not 10 <= self.font_size <= 32:
            return False, "font_size must be between 10 and 32"
        
        if not 300 <= self.overlay_width <= 800:
            return False, "overlay_width must be between 300 and 800"
        
        if not 200 <= self.overlay_height <= 600:
            return False, "overlay_height must be between 200 and 600"
        
        if not 0.0 <= self.opacity <= 1.0:
            return False, "opacity must be between 0.0 and 1.0"
        
        if not 0.5 <= self.animation_speed <= 2.0:
            return False, "animation_speed must be between 0.5 and 2.0"
        
        if self.theme not in ["dark", "light", "transparent"]:
            return False, "theme must be 'dark', 'light', or 'transparent'"
        
        if self.move_notation not in ["san", "uci"]:
            return False, "move_notation must be 'san' or 'uci'"
        
        return True, None
    
    def save(self, filepath: str = "overlay/overlay_config.json"):
        """Save configuration to JSON file"""
        config_dict = asdict(self)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuration saved to {filepath}")
    
    @classmethod
    def load(cls, filepath: str = "overlay/overlay_config.json") -> 'OverlayConfig':
        """Load configuration from JSON file"""
        if not os.path.exists(filepath):
            print(f"⚠️  Config file not found, creating default: {filepath}")
            config = cls()
            config.save(filepath)
            return config
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            config = cls(**data)
            
            # Validate loaded config
            is_valid, error = config.validate()
            if not is_valid:
                print(f"⚠️  Invalid config: {error}. Using defaults.")
                return cls()
            
            print(f"✅ Configuration loaded from {filepath}")
            return config
            
        except Exception as e:
            print(f"❌ Failed to load config: {e}. Using defaults.")
            return cls()
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        default = OverlayConfig()
        for key, value in asdict(default).items():
            setattr(self, key, value)
        print("✅ Configuration reset to defaults")


# === GLOBAL CONFIG INSTANCE ===
CONFIG = OverlayConfig.load()


# === HELPER FUNCTIONS ===
def get_config() -> OverlayConfig:
    """Get the global configuration instance"""
    return CONFIG


def reload_config():
    """Reload configuration from file"""
    global CONFIG
    CONFIG = OverlayConfig.load()
    return CONFIG


def save_config():
    """Save current configuration to file"""
    CONFIG.save()


# === EXAMPLE USAGE ===
if __name__ == "__main__":
    # Create custom configuration
    config = OverlayConfig(
        icon_size=40,
        font_size=18,
        overlay_width=450,
        language="vi",
        allowed_countries=["VN", "US", "GB"],
        show_country_flags=True
    )
    
    # Validate
    is_valid, error = config.validate()
    print(f"Valid: {is_valid}, Error: {error}")
    
    # Save
    config.save("overlay/overlay_config.json")
    
    # Load
    loaded_config = OverlayConfig.load("overlay/overlay_config.json")
    print(f"Loaded language: {loaded_config.language}")
    print(f"Loaded labels: {loaded_config.labels}")
    
    # Check country filter
    print(f"VN allowed: {loaded_config.is_country_allowed('VN')}")
    print(f"CN allowed: {loaded_config.is_country_allowed('CN')}")