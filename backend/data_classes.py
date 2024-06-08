from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GameInfo:
    white: str
    black: str
    id: Optional[int] = 0
    board: Optional[str] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@dataclass
class State:
    board: str
    turn: bool
    castle: str
    en_passant: int
    half_move: int
    full_move: int

@dataclass
class Move:
    square: int
    result: str
    id: str

@dataclass
class Action:
    directions: List[int]
    type: str
    id: Optional[str] = ""

@dataclass
class Piece:
    actions: List[Action]