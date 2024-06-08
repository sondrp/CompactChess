from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlite3 import connect, Connection
from chess import Chess
from queries import GameInfo, query_update_game, query_get_game, query_create_game

app = FastAPI()

def db():
    try:
        db = connect("chess.db")
        yield db
    finally:
        db.close()

@app.get("games/{id}")
def get_game(id: int, db: Connection = Depends(db)):
    game = query_get_game(id, db)
    if not game: 
        raise HTTPException(404, "Game not found")

    return game
    
@app.get("/create/{white}/{black}")
def create_game(white:str, black: str, db: Connection = Depends(db)):
    return query_create_game(GameInfo(white=white, black=black), db)


@app.get("games/join/{id}/{username}/{color}")
def join(id: int, username: str, color: str, db: Connection = Depends(db)):
    game = get_game(id, db)
    if color == "white":
        game.white = username
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