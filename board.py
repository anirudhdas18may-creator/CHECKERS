from game_logic import Piece

ROWS, COLS = 8, 8

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def setup(self):
        for r in range(ROWS):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    if r < 3:
                        self.grid[r][c] = Piece(r, c, "black")
                    elif r > 4:
                        self.grid[r][c] = Piece(r, c, "red")

    def get(self, r, c):
        return self.grid[r][c] if in_bounds(r, c) else None

    def set(self, r, c, piece):
        if in_bounds(r, c):
            self.grid[r][c] = piece
            if piece:
                piece.row = r
                piece.col = c

    def remove(self, r, c):
        if in_bounds(r, c):
            self.grid[r][c] = None

    def move_piece(self, piece, r, c):
        self.remove(piece.row, piece.col)
        self.set(r, c, piece)

        if piece.color == "red" and r == 0:
            piece.make_king()
        if piece.color == "black" and r == ROWS - 1:
            piece.make_king()

    def to_dict(self):
        data = {}
        for r in range(ROWS):
            data[str(r)] = {}
            for c in range(COLS):
                piece = self.grid[r][c]
                data[str(r)][str(c)] = piece.to_dict() if piece else None
        return data

    def from_dict(self, data):
        for r in range(ROWS):
            for c in range(COLS):
                cell = data[str(r)][str(c)]
                if cell:
                    self.grid[r][c] = Piece.from_dict(cell)
                else:
                    self.grid[r][c] = None
