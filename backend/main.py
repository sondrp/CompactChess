from dataclasses import asdict
import json
import re
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketState
from chess import Chess
from queries import GameInfo, query_update_game, query_get_game, query_create_game, query_get_games
from typing import Dict, List

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

        self.active_connections: List[WebSocket] = []

    # TODO : figure out how to refuse connections
    async def connect(self, websocket: WebSocket, username: str):
        white = self.game_info.white
        black = self.game_info.black
        await websocket.accept()
        self.active_connections.append(websocket)
        print(self.active_connections)

        if username == white or white == "no opponent": 
            self.game_info.white = username
        elif username == black or black == "no opponent":
            self.game_info.black = username
        else:
            return

        self.can_click = make_can_click_pattern(self.game_info)
        query_update_game(self.game_info)

    def disconnect(self, websocket: WebSocket) -> bool:
        self.active_connections.remove(websocket)
        return len(self.active_connections) == 0


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
        
        # TODO : don't send legal moves to the opponent
        await self.broadcast()
    
    async def broadcast(self):

        print("broadcastin..")

        data = asdict(self.game_info)
        data["legal_moves"] = [
            {"square": move.square, "result": move.result, "id": move.id}
            for move in self.chess.get_legal_moves()
        ]

        for connection in self.active_connections:
            await connection.send_json(data)

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
    try:

        await manager.broadcast()
            
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            action = data.get("action")
            if not action:
                raise HTTPException(404, "websocket data must contain some action specification")

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