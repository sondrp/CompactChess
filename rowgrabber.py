import re
print("start (remove this line later)")


board = "rnbqkbnr//pppppppp//        //        //        //        //PPPPPPPP//RNBQKBNR"
index = 71
ranger = re.compile(r"^(?:[A-Z]\s*[a-z ]|[a-z]\s*[A-Z ])")
leaper = re.compile(r"^(?:[A-Z][a-z ]|[a-z][A-Z ])")

rook = (
    [1, 10, -1, -10],
    ranger
)
knight = (
    [-19, -8, 12, 21, 29, 8, -12, -21],
    leaper
)
def generate_results(board, index, path_regex, offsets, include_board=True):
    results = []

    for offset in offsets:
        path = board[index::offset]
        match = re.match(path_regex, path) 
        if not match: continue

        path = match.group(0)
        for i in range(1, len(path)):
            landing_square = index + offset * i

            if not include_board:
                results.append(landing_square)
                continue

            board_result = list(board)
            board_result[index] = " "
            board_result[landing_square] = path[0]
            results.append((landing_square, "".join(board_result)))

    return results

# Ok, great. I am now able to do the simple stuff. 
# What about the hard stuff? 
# Castle for example. The path replacement will be slightly more challenging
# Similarly, the board reconstruction is harder too.

# for square, res in generate_results(board, index, knight[1], knight[0]):
#     print(square, res.replace("/", ""))