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
        game.black = username
    
    query_update_game(game, db)

class SessionManager:
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.chess = Chess(game_info.board)
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        return len(self.active_connections) == 0

    async def click(self, square: int, db: Connection):
        chess = self.chess
        move_executed = chess.click(square)
        fen = chess.fen()

        if move_executed:
            self.game_info.board = fen
            query_update_game(self.game_info, db)

        for connection in self.active_connections:
            await connection.send_json({"board": fen, "legal_moves": chess.get_legal_moves()})


games = {}

@app.websocket("/ws/{game_id}/{username}")
async def websocket_endpoint(
    websocket: WebSocket, 
    game_id: int, 
    username: str, 
    db: Connection = Depends(db)
):

    game = query_get_game(game_id, db)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game_id not in games:
        games[game_id] = SessionManager(game)

    manager = games[game_id]

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            

    except WebSocketDisconnect:
        empty_game = manager.disconnect(websocket)
        print(f"{username} has left the game.")
        if empty_game:
            del games[game_id]