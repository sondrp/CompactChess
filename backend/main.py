from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from chess import Chess
import re

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def db():
    try:
        db = sqlite3.connect("chess.db")
        yield db
    finally: 
        db.close()

chess = Chess()
default_board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@app.get("/games/{id}")
def get_game(id: int, db: sqlite3.Connection = Depends(db)):
    c = db.cursor()
    c.execute("SELECT id, board, white, black FROM games WHERE id = ?", (id, ))
    game = c.fetchone()

    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    board = game[1]
    global chess
    chess = Chess(board)

    return {
        "id": game[0],
        "board": board,
        "white": game[2],
        "black": game[3]
    }

@app.get("/create/{white}/{black}")
def create_game(white: str, black: str, db: sqlite3.Connection = Depends(db)):
    c = db.cursor()
    c.execute("INSERT INTO games (board, white, black) VALUES (?, ?, ?)", (
        default_board,
        white,
        black
    ))
    db.commit()
    return {"id": c.lastrowid, "board": default_board, "white": white, "black": black}


@app.get("/games/join/{id}/{username}/{color}")
def join(id: int, color: str, username: str, db: sqlite3.Connection = Depends(db)):
    c = db.cursor()
    if color == "white": 
        c.execute("""UPDATE games SET white = ? WHERE id = ?""", (username, id))
    if color == "black":
        c.execute("""UPDATE games SET black = ? WHERE id = ?""", (username, id))
    db.commit()

@app.get("/games/{id}/{username}/{square}")
def click(id: int, username: str, square: int, db: sqlite3.Connection = Depends(db)):
    c = db.cursor()
    c.execute("""SELECT board, white, black FROM games WHERE id = ?""", (id,))
    game = c.fetchone()

    if not game:
        raise HTTPException(status_code=404, detail=f"no game with id {id} exist")

    board, white, black = game[0], game[1], game[2] 

    pattern = re.compile(fr"w-{white}|b-{black}")
    test = f"{board.split(' ')[1]}-{username}"

    if not re.match(pattern, test):
        raise HTTPException(status_code=404, detail=f"{username} is not allowed to make a move here")

    move_exectuted = chess.click(square)
    if move_exectuted:
        c = db.cursor()
        c.execute("""UPDATE games SET board = ? WHERE id = ?""", (chess.fen(), id))
        db.commit()

    return {
        "game": chess.fen(),
        "legal_moves": chess.get_legal_moves()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)