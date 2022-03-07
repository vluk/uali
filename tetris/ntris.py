import torch
from torch import clamp
import time
from scipy.signal import correlate2d

from tetris.piece_data import rots, kicks, i_kicks, o_kicks, TRIL, TRIU, POW

"""
After some thought, an input-based move generation approach has some
fundamental performance issues. We can use numpy to generate moves at
a much higher speed.
"""

class Tetris():
    def drop(moves, full):
        """simulate soft drop"""
        moves -= full
        # TRI "drips" downwards
        # POW gives "priority" to lower elements
        moves = moves * POW[:, None]
        moves = TRIL @ moves
        moves = clamp(moves, 0, 1)
        moves[:,:39] -= moves[:,1:]
        moves = clamp(moves, 0, 1)
        return moves

    def wiggle(moves, full):
        """simulate left/right movement"""
        moves -= full 
        left = (moves * POW[:10]) @ TRIU
        right = (moves * POW[:10][::-1]) @ TRIL[:10, :10]
        moves = clamp(right, 0, 1) | clamp(left, 0, 1)
        return moves

    def rotate(moves, full, piece):
        kick = o_kicks if piece == "o" else (i_kicks if piece == "i" else kicks)
        # loop through source and target rotations
        for i in kicks:
            mask = 1 - full[i % 10]
            move = torch.clone(moves[i // 10])
            for x, y, nx, ny in kick[i]:
                # add with offset, then subtract from source
                valids = move[nx:40-x, ny:10-y] & mask[x:40-nx, y:10-ny]
                moves[i % 10][x:40-nx, y:10-ny] |= valids
                move[nx:40-x, ny:10-y] -= valids

        return moves

    def generate_moves(board, piece): 
        moves = torch.zeros(4, 40, 10, dtype=int)
        moves[0][18][5] = 1
        x = 2 if piece == "i" else 1
        full = torch.tensor([correlate2d(board, rots[piece][i], fillvalue=1)[x:40+x,x:10+x] for i in range(4)], dtype=int)
        full = clamp(full, 0, 1)
        moves = Tetris.rotate(moves, full, piece)
        moves = Tetris.wiggle(moves, full)
        moves = Tetris.drop(moves, full)
        moves = Tetris.rotate(moves, full, piece)
        moves = Tetris.wiggle(moves, full)
        moves = Tetris.drop(moves, full)
        return moves
   
    def empty_board():
        return torch.zeros(40, 10)