from sqlite3 import connect
from typing import List, Optional
from data_classes import GameInfo

DATABASE = "chess.db"

def query_get_game(id: int) -> Optional[GameInfo]:
    with connect(DATABASE) as db:
        c = db.cursor()
        c.execute("SELECT board, white, black FROM games WHERE id = ?", (id,))
        game = c.fetchone()
        return GameInfo(game[1], game[2], id, game[0]) if game else None    

def query_get_games(username: str) -> List[GameInfo]:
    with connect(DATABASE) as db:
        c = db.cursor()
        c.execute("SELECT id, board, white, black FROM games WHERE white = ? OR black = ?", (username, username))

        return [GameInfo(game[2], game[3], game[0], game[1]) for game in c.fetchall()]


def query_create_game(game_info: GameInfo) -> GameInfo:
    with connect(DATABASE) as db:
        c = db.cursor()
        c.execute(
            "INSERT INTO games (board, white, black) VALUES (?, ?, ?)",
            (game_info.board, game_info.white, game_info.black)
        )
        db.commit()
        game_info.id = c.lastrowid
        return game_info

def query_update_game(gi: GameInfo):
    with connect(DATABASE) as db:
        c = db.cursor()
        c.execute(
            "UPDATE games SET board = ?, white = ?, black = ? WHERE id = ?",
            (gi.board, gi.white, gi.black, gi.id)
        )
        db.commit()

