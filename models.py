# overlay/models.py
from dataclasses import dataclass

@dataclass(frozen=True)
class LabelMeta:
    key: str
    title: str
    icon: str


LABEL_META = {
    "best": LabelMeta("best", "BEST", "best.png"),
    "brilliant": LabelMeta("brilliant", "BRILLIANT", "brilliant.png"),
    "excellent": LabelMeta("excellent", "EXCELLENT", "excellent.png"),
    "great": LabelMeta("great", "GREAT", "great.png"),
    "good": LabelMeta("good", "GOOD", "good.png"),

    "theory": LabelMeta("theory", "THEORY", "theory.png"),
    "inaccuracy": LabelMeta("inaccuracy", "INACCURACY", "inaccuracy.png"),
    "miss": LabelMeta("miss", "MISS", "miss.png"),

    "mistake": LabelMeta("mistake", "MISTAKE", "mistake.png"),
    "blunder": LabelMeta("blunder", "BLUNDER", "blunder.png"),

    "forced": LabelMeta("forced", "FORCED", "forced.png"),
}
