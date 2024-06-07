from fastapi import FastAPI, Header, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from chess import Chess

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

@app.get("/users")
def create_user(username: str = Header(...), db: sqlite3.Connection = Depends(db)):
    c = db.cursor()

    c.execute("SELECT username FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user:
        return {"username": user[0]}

    try:
        c.execute("INSERT INTO users (username) VALUES (?)", (username,))
        db.commit()
        return {"username": username}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="username already exist")

@app.get("/create")
def create_game(white: str = Header(...), black: str = Header(...), db: sqlite3.Connection = Depends(db)):
    c = db.cursor()
    c.execute("INSERT INTO games (board, white, black) VALUES (?, ?, ?)", (
        default_board,
        white,
        black
    ))
    db.commit()
    return {"id": c.lastrowid, "board": default_board, "white": white, "black": black}

@app.get("/reset")
def reset():
    global chess
    chess = Chess()
    return {"game": chess.fen()}

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

@app.get("/")
def read_root():
    return {
        "game": chess.fen()
    }

@app.get("/games/join/{id}")
def join(id: int, color: str = Header(...), username = Header(...), db: sqlite3.Connection = Depends(db)):
    c = db.cursor()
    print(id)
    print(color)
    print(username)
    if color == "white": 
        c.execute("""UPDATE games SET white = ? WHERE id = ?""", (username, id))
    if color == "black":
        c.execute("""UPDATE games SET black = ? WHERE id = ?""", (username, id))
    db.commit()

@app.get("/click")
def click(id: int = Header(...), index: int = Header(...), white: bool = Header(...), db: sqlite3.Connection = Depends(db)):
    if chess.state.turn == white: 
        move_exectuted = chess.click(index)
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