from dataclasses import asdict
import json
import re
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from chess import Chess
from queries import GameInfo, query_update_game, query_get_game, query_create_game, query_get_games
from typing import Dict, Optional

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
    
@app.get("/games/user/{username}")
def get_games(username: str):
    return query_get_games(username)

@app.get("/create/{white}/{black}")
def create_game(white:str, black: str):
    return query_create_game(GameInfo(white, black))

def make_can_click_pattern(game_info: GameInfo):
    return re.compile(fr"w-{game_info.white}|b-{game_info.black}")

class SessionManager:
    def __init__(self, game_info: GameInfo):
        self.game_info = game_info
        self.chess = Chess(game_info.board)
        self.can_click = make_can_click_pattern(game_info)

        self.white_connection: Optional[WebSocket] = None
        self.black_connection: Optional[WebSocket] = None

    # TODO : figure out how to refuse connections
    async def connect(self, websocket: WebSocket, username: str):
        white = self.game_info.white
        black = self.game_info.black
        await websocket.accept()

        if username == white or white == "no opponent": 
            self.white_connection = websocket
            self.game_info.white = username

        if username == black or black == "no opponent":
            self.white_connection = websocket
            self.game_info.black = username
        
        self.can_click = make_can_click_pattern(self.game_info)
        query_update_game(self.game_info)

    def disconnect(self, websocket: WebSocket) -> bool:
        if websocket == self.white_connection:
            self.white_connection = None

        if websocket == self.black_connection:
            self.black_connection = None

        # True if any player remain
        return not self.white_connection and not self.black_connection        

    async def click(self, username: str, square: int):
        chess = self.chess
        move_executed = False

        turn = "w" if chess.state.turn else "b"
        if re.match(self.can_click, f"{turn}-{username}"):
            move_executed = chess.click(square)
        fen = chess.fen()

        if move_executed:
            self.game_info.board = fen
            query_update_game(self.game_info)
        
        legal_moves = [
            {"square": move.square, "result": move.result, "id": move.id}
            for move in chess.get_legal_moves()
        ]

        # TODO : don't send legal moves to the opponent
        await self.broadcast({"type": "click_result", "game": fen, "legal_moves": json.dumps(legal_moves)})
    
    async def broadcast(self, data):
        if self.white_connection is not None:
            await self.white_connection.send_json(data)
        if self.black_connection is not None:
            await self.black_connection.send_json(data)


managers: Dict[int, SessionManager] = {}

@app.websocket("/ws/join/{game_id}/{username}")
async def websocket_endpoint(
    websocket: WebSocket, 
    game_id: int, 
    username: str, 
):
    
    if game_id not in managers:
        game = query_get_game(game_id)
        if not game:
            raise HTTPException(404, "Game not found")

        managers[game_id] = SessionManager(game)

    manager = managers[game_id]
    await manager.connect(websocket, username)
    
    await manager.broadcast({"type": "game_info", "game_info": json.dumps(asdict(manager.game_info))})

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            action = data.get("action")
            if not action:
                raise HTTPException(404, "websocket data must contain some action specification")

            print("we the best music")
            if action == "click":
                username = data.get("username")

                square = int(data.get("square"))
                row = square // 8
                square += row * 2
                await manager.click(username, square)
            
    except WebSocketDisconnect:
        empty_game = manager.disconnect(websocket)
        print(f"{username} has left the game.")
        if empty_game:
            print("No connections left, deleting session manager")
            del managers[game_id]