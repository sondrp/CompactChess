from sqlite3 import connect, Connection
from dataclasses import dataclass
from typing import Optional

@dataclass
class GameInfo:
    white: str
    black: str
    id: Optional[int] = 0
    board: Optional[str] = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def query_get_game(id: int) -> Optional[GameInfo]:
    with connect("chess.db") as db:
        db = connect("chess.db")
        c = db.cursor()
        c.execute("SELECT board, white, black FROM games WHERE id = ?", (id,))
        game = c.fetchone()
        return GameInfo(game[1], game[2], id, game[0]) if game else None    

def query_create_game(game_info: GameInfo) -> GameInfo:
    with connect("chess.db") as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO games (board, white, black) VALUES (?, ?, ?)",
            (game_info.board, game_info.white, game_info.black)
        )
        db.commit()
        game_info.id = c.lastrowid
        return game_info

def query_update_game(gi: GameInfo):
    with connect("chess.db") as db:
        c = db.cursor()
        c.execute(
            "UPDATE games SET board = ?, white = ?, black = ? WHERE id = ?",
            (gi.board, gi.white, gi.black, gi.id)
        )
        db.commit()

