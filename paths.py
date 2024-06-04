# All possible moves, and how they change the board. Notation:
# key : (path_rexex, replacement)

# key: used to reference the correcy move type for a piece 
# path_regex: given a path traced by a piece, this will calculate if the path is legal
# replacement: given a legal path, replacement defines how the path will change should the move be played.

paths = {
    "leaper": (r"^(?:([A-Z])[a-z ]|([a-z])[A-Z ])$", r" \1\2"),
    "ranger": (r"^(?:([A-Z])( *)[a-z ]|([a-z])( *)[A-Z ])$", r" \2\4\1\3"),
    "capture": (r"^(?:([A-Z])[a-z]|([a-z])[A-Z])$", r" \1\2"),
    "unoccupied": (r"^(?:(\w) )$", r" \1"),
    "pawnDoubleForward": (r"^([Pp])(.. ) $", r" \2\1"),
    "enPassant": (r"^(?:(P)(..)p |(p)(..)P )$", r" \2\4 \1\3"),
    "castle": (r"^(?:(K) (  ?)(R)(.)|(k) (  ?)(r)(.))$", r" \3\7\1\5\2\6\4\8")
}

# How do they work? Haha... good luck
