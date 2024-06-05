import re

board = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
board = board.split(" ")[0]
board = board.replace("/", "//")
board = re.sub(r"\d", lambda m: " " * int(m.group(0)), board)
print("board:")
print(board + "|")

