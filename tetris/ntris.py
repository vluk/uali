from piece_data import rots, kicks, i_kicks, o_kicks

import numpy as np
from numpy import clip, copy
from scipy.signal import correlate2d

"""
After some thought, an input-based move generation approach
has some fundamental performance issues. We can use convolutions
and other linear algebra tricks to generate moves at a much higher
speed.
"""

TRIL = np.tril(np.ones((40, 40), dtype=int), k=0)
TRIU = np.triu(np.ones((40, 40), dtype=int), k=0)
POW = np.power(2, np.arange(40))

class Tetris():
    def drop(moves, full):
        """simulate soft drop"""
        moves -= full
        # TRI "drips" downwards
        # POW gives "priority" to lower elements
        moves = moves * POW[:, np.newaxis]
        # TODO: test if matrix multiplication is actually faster than for loop
        moves = TRIL @ moves
        moves = clip(moves, 0, 1)
        return moves

    def wiggle(moves, full):
        """simulate left/right movement"""
        moves -= full 
        left = (moves * POW[:10]) @ TRIU[:10, :10]
        right = (moves * POW[:10][::-1]) @ TRIL[:10, :10]
        moves = clip(right, 0, 1) | clip(left, 0, 1)
        return moves
    
    def rotate(moves, full, piece):
        kick = o_kicks if piece == "o" else (i_kicks if piece == "i" else kicks)
        # loop through source and target rotations
        newmoves = np.zeros(moves.shape, dtype=int)
        for i in kicks:
            mask = 1 - full[i % 10]
            move = copy(moves[i // 10])
            for x, y, nx, ny in kick[i]:
                # add with offset, then subtract from source
                valids = move[nx:40-x, ny:10-y] & mask[x:40-nx, y:10-ny]
                newmoves[i % 10][x:40-nx, y:10-ny] += valids
                move[nx:40-x, ny:10-y] -= valids

        moves = clip(newmoves + moves, 0, 1)
        return moves
        
    
    def generate_moves(board, piece): 
        moves = np.zeros((4, 40, 10), dtype=int)
        moves[0][18][5] = 1
        x = 2 if piece == "i" else 1
        full = np.array([correlate2d(board, rots[piece][i], fillvalue=1)[x:40+x,x:10+x] for i in range(4)], dtype=int)
        full = clip(full, 0, 1)
        moves = Tetris.rotate(moves, full, piece)
        moves = Tetris.wiggle(moves, full)
        moves = Tetris.drop(moves, full)
        moves = Tetris.rotate(moves, full, piece)
        moves = Tetris.rotate(moves, full, piece)
        moves = Tetris.rotate(moves, full, piece)
        moves[:,:39] -= moves[:,1:]
        moves = clip(moves, 0, 1)
        return moves
    
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
    
    def empty_board():
        return np.zeros((40, 10))

    def pretty_print(board):
        print("###")
        s = "\n".join(["".join(["  " if j <= 0 else "██" for j in i])
                      for i in board[21:]])
        print(s)