class Piece:
    def __init__(self, r, c, color, king=False):
        self.row = r
        self.col = c
        self.color = color
        self.king = king

    def make_king(self):
        self.king = True

    def to_dict(self):
        return {
            "row": self.row,
            "col": self.col,
            "color": self.color,
            "king": self.king
        }

    @staticmethod
    def from_dict(data):
        return Piece(data["row"], data["col"], data["color"], data["king"])
