import time

from tetris.piece_data import rots
from tetris.ntris import Tetris

def place_piece(board, x, y, piece, rot):
    # cursed index manip to clip piece boundary
    # for debugging purposes only
    piece = rots[piece][rot]
    x = x - piece.shape[0] // 2
    y = y - piece.shape[1] // 2
    w = max(0, x)
    z = max(0, y)
    x1 = min(piece.shape[0], board.shape[0] - x)
    y1 = min(piece.shape[1], board.shape[1] - y)

    board[w: x+x1, z: y+y1] += piece[w-x: x1, z-y: y1]
    return board
 

def pretty_print(board):
    print("###")
    s = "\n".join(["".join(["  " if j <= 0 else "██" for j in i])
                    for i in board[21:]])
    print(s)

# dt cannon
board = Tetris.empty_board()
board = place_piece(board, 39, 4, "l", 0)
board = place_piece(board, 39, 8, "j", 0)
board = place_piece(board, 37, 6, "i", 1)
board = place_piece(board, 38, 4, "s", 0)
board = place_piece(board, 38, 8, "z", 0)
board = place_piece(board, 36, 4, "t", 0)
board = place_piece(board, 39, 0, "o", 0)
board = place_piece(board, 36, 0, "j", 1)
board = place_piece(board, 34, 3, "l", 3)
board = place_piece(board, 35, 9, "i", 1)
board = place_piece(board, 36, 7, "o", 0)

pretty_print(board)

for i in range(100):
    Tetris.generate_moves(board, "t")