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

def extract_paths(board, index, offsets):
    return [board[index::offset] for offset in offsets]

# Ok, seems I am able to just extract by offset directly, no need to do anything at all...... So good! 
# Also, no need to use numberings on diagonals I think

# This gives me a new way of thinking. Just assume all are rangers, then filter down based on path regex :)
# Holy... this will improve life a lot.


# Now, one challenge is that I actually need the indices. Not just the path? Otherwise, how
# can I show which moves to click on.

# No need, because I have the offsets used to generate the path in the first place.

path_regex = re.compile(r"^(?:[A-Z]\s*[a-z ]|[a-z]\s*[A-Z ])")
#path_replace_regex = re.compile()

index = 33
offsets = [1, 10, -1, -10]
paths = extract_paths(board, index, offsets)
paths = map(lambda p: re.match(path_regex, p), paths)

for m in paths:
    if not m: continue
    path = m.group(0)
    path = m.group(0)[::-1]
    for result in re.finditer(r".(?=.*R)", path):
        start_index = result.start()
        result_path = path[start_index:]
        print(result_path)

# Great! I am not able to extract many results from one string. 
# Now I have to make the replacement, and put it back into the board...
# I can let the replacement regexes be the other way around right?
# I think so...

print(paths)

