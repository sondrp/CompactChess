from dataclasses import dataclass
from typing import List, Optional
import re

# No comments or explanations will be given :)
# For now at least

### Data classes

@dataclass
class Action:
    directions: List[str]
    type: str
    id: Optional[str] = ""

@dataclass
class Piece:
    actions: List[Action]

### Maps

paths = {
    "leaper": (r"^(?:([A-Z])[a-z ]|([a-z])[A-Z ])$", r" \1\2"),
    "ranger": (r"^(?:([A-Z])( *)[a-z ]|([a-z])( *)[A-Z ])$", r" \2\4\1\3"),
    "capture": (r"^(?:([A-Z])[a-z]|([a-z])[A-Z])$", r" \1\2"),
    "unoccupied": (r"^(?:(\w) )$", r" \1"),
    "pawnDoubleForward": (r"^([Pp])(.. ) $", r" \2\1"),
    "enPassant": (r"^(?:(P)(..)p |(p)(..)P )$", r" \2\4 \1\3"),
    "castle": (r"^(?:(K) (  ?)(R)(.)|(k) (  ?)(r)(.))$", r" \3\7\1\5\2\6\4\8"),
    
    # The following are used in the reverse king piece. To see if the king is in check.
    "orthogonal": (r"Kk|kK|K\s*[qr]|k\s*[QR]", r""),
    "diagonal": (r"Kk|kK|K\s*[qb]|k\s*[QB]", r""),
    "bPawnAttack": (r"Kp", r""),
    "wPawnAttack": (r"kP", r""),
    "knightAttack": (r"Kn|kN", r""),
}

id_to_castle_squares = {
    "Q": [72, 73, 74],
    "K": [74, 75, 76],
    "q": [2, 3, 4],
    "k": [4, 5, 6],
}

### Pieces

rook = Piece([Action(["E", "S", "W", "N"], "ranger")])
knight = Piece([Action(["NNW", "WWN", "WWS", "SSW", "SSE", "EES", "EEN", "NNE"], "leaper")])
bishop = Piece([Action(["NW", "SW", "SE", "NE"], "ranger")])
queen = Piece([Action(["NE", "E", "SE", "S", "SW", "W", "NW", "N"], "ranger")])
wKing = Piece([
    Action(["NE", "E", "SE", "S", "SW", "W", "NW", "N"], "leaper", "KQ"),
    Action(["E E- E 7NW"], "castle", "K"),
    Action(["W W- W W 7NE"], "castle", "Q"),
])
bKing = Piece([
    Action(["NE", "E", "SE", "S", "SW", "W", "NW", "N"], "leaper", "kq"),
    Action(["E E- E 7SW"], "castle", "k"),
    Action(["W W- W W 7SE"], "castle", "q"),
])
wPawn = Piece([
    Action(["NE", "NW"], "capture", "P"),
    Action(["N"], "unoccupied", "P"),
    Action(["S 7N 5S N"], "pawnDoubleForward", "pawnDoubleForward"),
    Action(["4S 7N 3S1W N", "4S 7N 3S1E N"], "enPassant", "enPassant"),
])

bPawn = Piece([
    Action(["SE", "SW"], "capture", "p"),
    Action(["S"], "unoccupied", "p"),
    Action(["N 7S 5N S"], "pawnDoubleForward", "pawnDoubleForward"),
    Action(["4N 7S 3N1S S", "4N 7S 3N1E S"], "enPassant", "enPassant"),
])
cover_piece = Piece([
    Action(["E", "S", "W", "N"], "orthogonal"),
    Action(["NE", "SE", "SW", "NW"], "diagonal"),
    Action(["NE", "NW"], "bPawnAttack"),
    Action(["SE", "SW"], "wPawnAttack"),
    Action(["NNE", "EEN", "EES", "SSE", "SSW", "WWS", "WWN", "NNW"], "knightAttack"),
])

piece_map = {
    "R": rook,
    "r": rook,
    "N": knight,
    "n": knight,
    "B": bishop,
    "b": bishop,
    "Q": queen,
    "q": queen,
    "K": wKing,
    "k": bKing,
    "P": wPawn,
    "p": bPawn,
}

### Functions

def is_square_covered(board, square):
    for action in cover_piece.actions:
        for direction in action.directions:
            for move in generate_moves(board, square, action, direction):
                if board[move[0]] != " ": return True
    return False

def castle_filter(board, move):
    id = move[2]
    if not id or id not in "KQkq": return True
    castle_squares = id_to_castle_squares[move[2]]
    for square in castle_squares:
        if (is_square_covered(board, square)):
            return True
    return False

def state_filter(move, en_passant, castle):
    id = move[2]
    
    if id == "enPassant" and move[0] != en_passant:
        return False
    
    if id in "KQkq" and id not in castle:
        return False
    return True

def check_filter(board, white_king):
    king_to_find = "K" if white_king else "k"
    king_index = board.find(king_to_find)
    return not is_square_covered(board, king_index)

def parse_direction(match):
    direction, click_spec = match.groups()
    offset = 0

    for m in re.finditer(r"(\d?)([ESWN]+)", direction):
        reps, num = m.groups()
        reps = int(reps) if reps.isdecimal() else 1
        num = 10 * num.count("S") + num.count("E") - 10 * num.count("N") - num.count("W")
        offset += reps * num

    return offset, bool(click_spec)

def generate_moves(board, index, action, direction):
    path_regex, replacement = paths[action.type]

    current_square = index
    current_path = board[index]
    visited = [index]
    square_to_click = None

    moves = []

    for sub_direction in re.finditer(r"([ESWN\d]+)(-?)", direction):

        offset, should_specify_click = parse_direction(sub_direction)

        while (True):

            current_square += offset
            if current_square < 0 or 77 < current_square: return moves 
            current_path += board[current_square]
            visited.append(current_square)
            if (should_specify_click):
                square_to_click = current_square

            resulting_path = re.sub(path_regex, replacement, current_path)

            if (resulting_path == current_path): break

            result = list(board)
            for i in range(len(visited)):
                result[visited[i]] = resulting_path[i]

            square_to_click = square_to_click if square_to_click else current_square
            moves.append((square_to_click, "".join(result), action.id))
            square_to_click = None
    return moves

class Chess:
    board = "rnbqkbnr//pppppppp//        //        //        //        //PPPPPPPP//RNBQKBNR"
    en_passant = -1
    castle = "KQkq"
    legal_moves = []
    turn = True

    def click(self, index):
        move = next((move for move in self.legal_moves if move[0] == index), None)

        if move:
            square, board, id = move
            self.turn = not self.turn
            self.board = board
            if id == "enPassant":
                offset = -10 if board[square].isupper() else 10
                self.en_passant = square + offset
            
            if id in self.castle:
                self.castle.replace(id, "")
            
            return True

        self.legal_moves = self.calculate_legal_moves(index)
        return False

    def calculate_legal_moves(self, index):
        if index < 0 or 77 < index: return []
        piece = self.board[index]

        legal_moves = []

        if piece == " " or self.turn == piece.islower():
            return legal_moves

        piece = piece_map[piece]  

        for action in piece.actions:
            for direction in action.directions:
                legal_moves += generate_moves(self.board, index, action, direction)
        legal_moves = filter(lambda m: check_filter(self.board, self.turn), legal_moves)
        legal_moves = filter(lambda m: state_filter(m, self.en_passant, self.castle), legal_moves)
        legal_moves = filter(lambda m: castle_filter(self.board, m), legal_moves)
        return list(legal_moves)

    def check_game_over(self):
        for index, piece in enumerate(self.board):
            if piece == " " or piece == "/": continue
            if self.turn != piece.isupper(): continue
            piece = piece_map[piece]
            for action in piece.actions:
                for direction in action.directions:
                    if generate_moves(self.board, index, action, direction):
                        return False
        return True

    def print(self):
        print(self.board.replace("//", "\n"))

def main():
    chess = Chess()
    while (True):
        square = int(input("Square: "))
        if (chess.click(square)):
            chess.print()
        else:
            print([m[0] for m in chess.legal_moves])

if __name__ == "__main__":
    main()

