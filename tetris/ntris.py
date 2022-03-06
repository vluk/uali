import numpy as np
from numpy import clip, copy
from scipy.signal import correlate2d

from piece_data import rots, kicks, i_kicks, o_kicks, TRIL, TRIU, POW

"""
After some thought, an input-based move generation approach has some
fundamental performance issues. We can use numpy to generate moves at
a much higher speed.
"""
n = 3

class Tetris():
    def drop(moves, full):
        """simulate soft drop"""
        moves -= full
        # TRI "drips" downwards
        # POW gives "priority" to lower elements
        moves = moves * POW[:, np.newaxis]
        moves = TRIL @ moves
        moves = clip(moves, 0, 1)
        moves[:,:39] -= moves[:,1:]
        moves = clip(moves, 0, 1)
        return moves

    def wiggle(moves, full):
        """simulate left/right movement"""
        moves -= full 
        left = (moves * POW[:10]) @ TRIU
        right = (moves * POW[:10][::-1]) @ TRIL[:10, :10]
        moves = clip(right, 0, 1) | clip(left, 0, 1)
        return moves

    def rotate(moves, full, piece):
        kick = o_kicks if piece == "o" else (i_kicks if piece == "i" else kicks)
        # loop through source and target rotations
        for i in kicks:
            mask = 1 - full[i % 10]
            move = copy(moves[i // 10])
            for x, y, nx, ny in kick[i]:
                # add with offset, then subtract from source
                valids = move[nx:40-x, ny:10-y] & mask[x:40-nx, y:10-ny]
                moves[i % 10][x:40-nx, y:10-ny] += valids
                move[nx:40-x, ny:10-y] -= valids

        moves = clip(moves, 0, 1)
        return moves

    def generate_moves(board, piece): 
        moves = np.zeros((4, 40, 10), dtype=int)
        moves[0][18][5] = 1
        x = 2 if piece == "i" else 1
        full = np.array([correlate2d(board, rots[piece][i], fillvalue=1)[x:40+x,x:10+x] for i in range(4)], dtype=int)
        full = clip(full, 0, 1)
        for _ in range(n):
            moves = Tetris.rotate(moves, full, piece)
            moves = Tetris.wiggle(moves, full)
            moves = Tetris.drop(moves, full)
        return moves
   
    def empty_board():
        return np.zeros((40, 10))