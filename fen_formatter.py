import re

board = "1rrrrrr1/8/7n/p2R3n/7n/6nn/5n2/8 w - - 0 1"
board = board.split(" ")[0]
board = board.replace("/", "//")
board = re.sub(r"\d", lambda m: " " * int(m.group(0)), board)
print("board:")
print(board + "|")

