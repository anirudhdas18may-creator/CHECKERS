import pygame
import sys

from board import Board, in_bounds
from game_logic import Piece
from file_manager import initialize_game, save_game

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (245, 245, 245)
DARK_SQ = (102, 51, 0)
LIGHT_SQ = (230, 200, 160)
RED = (230, 40, 40)
BLACK = (10, 10, 10)
HIGHLIGHT = (255, 215, 0)
SELECT_COLOR = (0, 200, 200)

UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DN_LEFT = (1, -1)
DN_RIGHT = (1, 1)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers (Resume Feature)")
FONT = pygame.font.SysFont("consolas", 24)


def opponent(color):
    return "black" if color == "red" else "red"


def normal_moves(board, piece):
    moves = []
    directions = [UP_LEFT, UP_RIGHT, DN_LEFT, DN_RIGHT] if piece.king else \
        ([UP_LEFT, UP_RIGHT] if piece.color == "red" else [DN_LEFT, DN_RIGHT])

    for dr, dc in directions:
        nr, nc = piece.row + dr, piece.col + dc
        if in_bounds(nr, nc) and board.get(nr, nc) is None:
            moves.append((nr, nc))
    return moves


def capture_moves(board, piece):
    jumps = []
    directions = [UP_LEFT, UP_RIGHT, DN_LEFT, DN_RIGHT] if piece.king else \
        ([UP_LEFT, UP_RIGHT] if piece.color == "red" else [DN_LEFT, DN_RIGHT])

    for dr, dc in directions:
        mid_r = piece.row + dr
        mid_c = piece.col + dc
        land_r = piece.row + 2 * dr
        land_c = piece.col + 2 * dc

        if (
            in_bounds(mid_r, mid_c)
            and in_bounds(land_r, land_c)
            and board.get(mid_r, mid_c)
            and board.get(mid_r, mid_c).color == opponent(piece.color)
            and board.get(land_r, land_c) is None
        ):
            jumps.append((land_r, land_c, mid_r, mid_c))
    return jumps


def draw_board():
    for r in range(ROWS):
        for c in range(COLS):
            color = LIGHT_SQ if (r + c) % 2 == 0 else DARK_SQ
            pygame.draw.rect(WIN, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(board, selected_piece=None, highlights=None):
    if highlights:
        for r, c in highlights:
            pygame.draw.circle(WIN, HIGHLIGHT,
                               (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                                r * SQUARE_SIZE + SQUARE_SIZE // 2),
                               SQUARE_SIZE // 6)

    for r in range(ROWS):
        for c in range(COLS):
            piece = board.get(r, c)
            if piece:
                color = RED if piece.color == "red" else BLACK
                pygame.draw.circle(WIN, color,
                                   (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                                    r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 8)

                if piece.king:
                    k_text = FONT.render("K", True, WHITE)
                    WIN.blit(k_text, (c * SQUARE_SIZE + 28, r * SQUARE_SIZE + 26))

    if selected_piece:
        pygame.draw.rect(WIN, SELECT_COLOR,
                         (selected_piece.col * SQUARE_SIZE,
                          selected_piece.row * SQUARE_SIZE,
                          SQUARE_SIZE, SQUARE_SIZE), 4)


def get_square(pos):
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE


def main():
    clock = pygame.time.Clock()
    board = Board()

    turn = initialize_game(board)

    selected = None
    highlights = []
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(board, turn)
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                r, c = get_square(event.pos)
                piece = board.get(r, c)

                if selected:
                    if (r, c) in highlights:
                        capture = False
                        for mv in capture_moves(board, selected):
                            if mv[0] == r and mv[1] == c:
                                board.remove(mv[2], mv[3])
                                capture = True
                        board.move_piece(selected, r, c)
                        if not capture:
                            turn = opponent(turn)
                        selected = None
                        highlights = []
                    else:
                        selected = None
                        highlights = []
                else:
                    if piece and piece.color == turn:
                        selected = piece
                        caps = capture_moves(board, piece)
                        cap_lands = [(m[0], m[1]) for m in caps]
                        highlights = normal_moves(board, piece) + cap_lands

        draw_board()
        draw_pieces(board, selected, highlights)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

