from fastapi import FastAPI, Header
from game import Chess

app = FastAPI()
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