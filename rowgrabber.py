import re
board = " rrrrrr //        //       n//p  RR  n//       n//      nn//     n  //        "

## Hmm... you can get the index of a match... For each match. Is that going to be useful? Let us find out!
## Tasks:
# Extract row based on row number - CHECK
# Extract column based on column number - CHECK
# Extract diagonal based on row and column number
# Extract directions from some starting point
# Extract directions from starting point until condition is met

# Do I want to extract all the indices too? Not yet.
print("start (remove this line later)")

index = 33
offsets = [1, 10, -1, -10]
path_regex = re.compile(r"^(?:[A-Z]\s*[a-z ]|[a-z]\s*[A-Z ])")

results = []

for offset in offsets:
    path = board[index::offset]
    match = re.match(path_regex, path) 
    if not match: continue

    # valid path confirmed. Each char in the path (after one) is a possible move.
    for i in range(1, len(path)):
        landing_square = index + offset * i
        board_result = list(board)
        board_result[index] = " "
        board_result[landing_square] = path[0]
        results.append(landing_square, "".join(board_result))


def extract_paths(board, index, offsets):
    return [board[index::offset] for offset in offsets]


#path_replace_regex = re.compile()

paths = extract_paths(board, index, offsets)

for path in paths:
    match = re.match(path_regex, path)
    if not match: continue

    path = match.group(0)
    piece = path[0]
    results = []
    for i in range(1, len(path)):


        board_result = list(board)
        board_result[index] = " "
        board_result[index]


        # path_result = list(path)
        # path_result[0] = " "
        # path_result[landing_square] = piece

        # at this point I have a path. The landing square is of course the click square
        # now to make the board. 
        # of course, in simple terms I don't need to create the path at all. 
        # just put the move directly in there. Makes life a lot easier, but will not do in 
        # the long term. Let us do it for now


        
paths = map(lambda p: re.match(path_regex, p), paths)

for m in paths:
    if not m: continue
    path = m.group(0)
    piece = path[0]
    results = []
    for i in range(1, len(path)):
        result = list(path)
        result[0] = " "
        result[i] = path[0]
        results.append("".join(result))

# all paths are now generated. Time to create the boards for each one.
boards = []
for i in range(len(offsets)):
    board_result = list(board)
    offset = offsets[i]
    path_result = results[i]
    for y in range(len(path_result)):
        board_result[index + offset * y] = path_result[y]
    boards.append("".join(board_result))
    

    print("lolas")





print(paths)

