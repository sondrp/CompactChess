from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from game import Chess

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

chess = Chess()

@app.get("/")
def read_root():
    return {
        "game": chess.fen()
    }

@app.get("/click")
def read_item(index: int = Header(...), white: bool = Header(...)):
    if chess.state.turn == white: 
        chess.click(index)
    return {
        "game": chess.fen(),
        "legal_moves": chess.get_legal_moves()
    }