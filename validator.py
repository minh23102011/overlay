# overlay/validator.py
from overlay import config


def is_label_enabled(label: str) -> bool:
    return config.LABEL_ENABLED.get(label.lower(), False)
