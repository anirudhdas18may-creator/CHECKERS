import json
import os

SAVE_FILE = "savegame.json"


def save_exists():
    return os.path.exists(SAVE_FILE)


def save_game(board, turn):
    data = {
        "board": board.to_dict(),
        "turn": turn
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
    print("Game saved.")


def load_game(board):
    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    board.from_dict(data["board"])
    print("Game loaded.")
    return data["turn"]


def delete_save():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


def ask_resume():
    answer = input("Resume previous game? (Y/N): ").strip().lower()
    return answer == "y"


def initialize_game(board):
    if save_exists():
        if ask_resume():
            return load_game(board)
        else:
            delete_save()
            board.setup()
            return "red"
    else:
        board.setup()
        return "red"
