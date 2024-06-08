from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chess import Chess
from queries import GameInfo, query_update_game, query_get_game, query_create_game
from typing import Dict

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

@app.get("/games/{id}")
def get_game(id: int):
    game = query_get_game(id)
    if not game: 
        raise HTTPException(404, "Game not found")

    return game
    
@app.get("/create/{white}/{black}")
def create_game(white:str, black: str):
    return query_create_game(GameInfo(white, black))


@app.get("/games/join/{id}/{username}/{color}")
def join(id: int, username: str, color: str):
    game = get_game(id)
    if color == "white":
        game.white = username
    if color == "black":
        game.black = username
    
    query_update_game(game)

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

    async def click(self, square: int):
        chess = self.chess
        move_executed = chess.click(square)
        fen = chess.fen()

        if move_executed:
            self.game_info.board = fen
            query_update_game(self.game_info)
        
        legal_moves = [
            {"square": move.square, "result": move.result, "id": move.id}
            for move in chess.get_legal_moves()
        ]

        for connection in self.active_connections:
            await connection.send_json({"game": fen, "legal_moves": legal_moves})

games: Dict[int, SessionManager] = {}

@app.websocket("/ws/{game_id}/{username}")
async def websocket_endpoint(
    websocket: WebSocket, 
    game_id: int, 
    username: str, 
):

    game = query_get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game_id not in games:
        games[game_id] = SessionManager(game)

    manager = games[game_id]

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()

            square = int(data)
            row = square // 8
            square += row * 2
            await manager.click(square)
            

    except WebSocketDisconnect:
        empty_game = manager.disconnect(websocket)
        print(f"{username} has left the game.")
        if empty_game:
            del games[game_id]