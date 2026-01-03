"""
Data Models for Chess Overlay System
Defines the structure of move analysis data
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class MoveDisplayData:
    """
    Data structure for displaying chess move analysis
    
    Attributes:
        label: Move quality classification (brilliant, best, excellent, good, inaccuracy, mistake, blunder, forced)
        best_move: Engine's recommended best move in algebraic notation (e.g., "Nf3", "e4")
        opponent_best_move: Opponent's predicted best response (optional)
        evaluation: Centipawn evaluation (optional, for future use)
        depth: Engine search depth (optional, for future use)
    """
    label: str
    best_move: str
    opponent_best_move: Optional[str] = None
    evaluation: Optional[int] = None
    depth: Optional[int] = None
    
    def __post_init__(self):
        """Validate data after initialization"""
        valid_labels = ["brilliant", "best", "excellent", "good", "inaccuracy", "mistake", "blunder", "forced"]
        if self.label not in valid_labels:
            raise ValueError(f"Invalid label: {self.label}. Must be one of {valid_labels}")
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        opp = f", opp_best={self.opponent_best_move}" if self.opponent_best_move else ""
        eval_str = f", eval={self.evaluation:+d}cp" if self.evaluation is not None else ""
        return f"MoveDisplayData(label={self.label}, best={self.best_move}{opp}{eval_str})"


# Example usage
if __name__ == "__main__":
    # Test creating move data
    move1 = MoveDisplayData(
        label="brilliant",
        best_move="Nxe5",
        opponent_best_move="Qd4"
    )
    print(move1)
    
    move2 = MoveDisplayData(
        label="blunder",
        best_move="Rd1",
        opponent_best_move="Qxf2#",
        evaluation=-750
    )
    print(move2)
    
    # Test validation
    try:
        invalid_move = MoveDisplayData(label="invalid", best_move="e4")
    except ValueError as e:
        print(f"Validation error: {e}")