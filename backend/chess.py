from typing import List
import re
from data_classes import Action, Piece, Move, State

# Chess implementation that is compact, but still possible to reason about (for me).
# Not intended to be an example of good code.

wPawnAttack = [-9, -11]
bPawnAttack = [9, 11]
knight_move = [-19, -8, 12, 21, 19, -8, -12, -21]
diagonal = [-9, 11, 9, -11]
orthogonal = [1, 10, -1, -10]
diag_and_ort = [-9, 1, 11, 10, 9, -1, -11, -10]

ranger = re.compile(r"[A-Z]\s*[a-z ]|[a-z]\s*[A-Z ]")
leaper = re.compile(r"[A-Z][a-z ]|[a-z][A-Z ]")
unoccupied = re.compile(r"^. ")
capture = re.compile(r"[A-Z][a-z]|[a-z][A-Z]")

knight = Piece([Action(knight_move, leaper)])
bishop = Piece([Action(diagonal, ranger)])
queen = Piece([Action(diag_and_ort, ranger)])
wKing = Piece([
    Action(diag_and_ort, leaper, "KQ"),
    Action([2], unoccupied, "K"),
    Action([-2], unoccupied, "Q"),
])
bKing = Piece([
    Action(diag_and_ort, leaper, "kq"),
    Action([2], unoccupied, "k"),
    Action([-2], unoccupied, "q"),
])
wPawn = Piece([
    Action(wPawnAttack, capture, "P"),
    Action([-10], unoccupied, "P"),
    Action([-20], unoccupied, "twoForward"),
    Action(wPawnAttack, unoccupied, "enPassant"),
])
bPawn = Piece([
    Action(bPawnAttack, capture, "p"),
    Action([10], unoccupied, "p"),
    Action([20], unoccupied, "twoForward"),
    Action(bPawnAttack, unoccupied, "enPassant"),
])
white_cover = Piece([
    Action(wPawnAttack, r".P"),
    Action(knight_move, r".N"),
    Action(diag_and_ort, r".K"),
    Action(orthogonal, r".\s*[QR]"),
    Action(diagonal, r".\s*[QB]"),
])
black_cover = Piece([
    Action(bPawnAttack, r".p"),
    Action(knight_move, r".n"),
    Action(diag_and_ort, r".k"),
    Action(orthogonal, r".\s*[qr]"),
    Action(diagonal, r".\s*[qb]"),
])

piece_map = {
    'R': Piece([Action(orthogonal, ranger, "R")]),
    'r': Piece([Action(orthogonal, ranger, "r")]),
    'B': bishop,
    'b': bishop,
    'N': knight,
    'n': knight,
    'Q': queen,
    'q': queen,
    'K': wKing,
    'k': bKing,
    'P': wPawn,
    'p': bPawn,
    'wc': white_cover,
    'bc': black_cover,
}

def generate_moves(board, index, action: Action, include_board=True) -> List[Move]:
    results = []

    for offset in action.directions:
        path = board[index::offset]
        match = re.match(action.type, path) 
        if not match: continue

        path = match.group(0)
        for i in range(1, len(path)):
            landing_square = index + offset * i

            if not include_board:
                results.append(Move(landing_square, "", ""))
                continue

            board_result = list(board)
            board_result[index] = " "
            board_result[landing_square] = path[0]
            results.append(Move(landing_square, "".join(board_result), action.id))

    return results

def is_square_covered(board, index, by_white):
    for action in piece_map["wc" if by_white else "bc"].actions:
        for move in generate_moves(board, index, action, False):
            if board[move.square] != " ": return True
    return False

def is_king_in_check(board, white_king):
    king_to_find = "K" if white_king else "k"
    king_index = board.find(king_to_find)
    return is_square_covered(board, king_index, not white_king)

def en_passant_filter(state: State, move: Move):
    if move.id != "enPassant": return True
    if move.square != state.en_passant: return False
    board = list(move.result)
    board[move.square + (10 if state.turn else -10)] = " "
    move.result = "".join(board)
    return True

def castle_filter(state: State, move: Move):
    square, result, id = move.square, move.result, move.id
    if id == "" or id not in "QKqk": return True

    castle = state.castle
    if id not in castle: return False

    index = "QKqk".find(id)
    castle_squares = [[72, 73, 74], [74, 75, 76], [2, 3, 4], [4, 5, 6]][index]

    for square in castle_squares:
        if (is_square_covered(result, square, not state.turn)):
            return False

    pattern, repl = [(r"R K ", r"  KR"), (r" KR", r"RK "), (r"r k ", r"  kr"), (r" kr", r"rk ")][index]
    move.result = re.sub(pattern, repl, move.result)
    return True

def in_check_filter(state: State, move: Move):
    square, result = move.square, move.result
    white_move = result[square].isupper()
    return not is_king_in_check(result, white_move)

def pawn_double_forward_filter(state: State, move: Move):
    square, result, id = move.square, move.result, move.id
    if id != "twoForward": return True

    white_move = state.turn
    row = 4 if white_move else 3
    if square // 10 != row: return False

    square_to_check = square + (10 if white_move else -10)
    return result[square_to_check] == " "

def generate_legal_moves(state, index, include_board=True) -> List[Move]:
    if index % 10 > 7: return []
    board = state.board
    piece = board[index]
    if piece == " ":
        return []

    if piece.isupper() != state.turn:
        return []
        
    piece = piece_map[piece]

    legal_moves = []
    for action in piece.actions:
        legal_moves += generate_moves(board, index, action, include_board)

    legal_moves = list(filter(lambda m: pawn_double_forward_filter(state, m), legal_moves))
    legal_moves = list(filter(lambda m: castle_filter(state, m), legal_moves))
    legal_moves = list(filter(lambda m: en_passant_filter(state, m), legal_moves))
    return list(filter(lambda m: in_check_filter(state, m), legal_moves))

def update_state(state: State, move: Move):
    square, result, id = move.square, move.result, move.id
    result = list(result)
    
    state.en_passant = -1 if id != "twoForward" else square + (10 if state.turn else -10)

    if id == "P" and square // 10 == 0:
        result[square] = "Q"

    if id == "p" and square // 10 == 7:
        result[square] = "q"
    
    if re.match(r"[KQkq]+", id):
        state.castle = "".join([l for l in state.castle if l not in id])

    for letter in state.castle:
        i = "KQkq".find(letter)
        i = [7, 0, 77, 70][i]
        if result[i] == " ":
            state.castle = state.castle.replace(letter, "")

    state.board = "".join(result)
    state.half_move += 1
    state.full_move += 0 if state.turn else 1 
    state.turn = not state.turn

def check_game_active(state: State):
    return any(generate_legal_moves(state, square) for square in range(78))

class Chess:

    legal_moves: List[Move] = []
    game_active = True

    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        board, turn, castle, en_passant, half_move, full_move = fen.split(" ")
        board = board.replace("/", "//")
        board = re.sub(r"\d", lambda m: " " * int(m.group(0)), board)
        turn = turn == "w"
        en_passant = int(en_passant) if en_passant.isdigit() else -1
        self.state = State(board, turn, castle, en_passant, int(half_move), int(full_move))

    def click(self, square):
        state = self.state
        move = next((move for move in self.legal_moves if move.square == square), None)

        if move:
            update_state(state, move)
            self.legal_moves = []
            self.game_active = check_game_active(state)
            return True

        self.legal_moves = generate_legal_moves(state, square)
        return False
    
    def get_legal_moves(self):
        return list(map(lambda l: Move(l.square, self.fen(l.result), l.id), self.legal_moves))
    
    def fen(self, board=None):
        state = self.state
        board = board if board else state.board
        board = board.replace("//", "/")
        board = re.sub(r"\s+", lambda m: str(len(m.group(0))), board)
        turn = "w" if state.turn else "b"
        return f"{board} {turn} {state.castle} - {state.half_move} {state.full_move}"