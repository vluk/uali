import torch
import numpy as np
from torch import clamp
import time

from tetris.piece_data import rots, kicks, i_kicks, o_kicks, POW

"""
After some thought, an input-based move generation approach has some
performance issues. We can use numpy to generate moves at
a much higher speed.
"""

class Tetris():
    def drop(moves, full):
        """simulate soft drop"""
        # POW gives "priority" to lower elements
        clamp(torch.cumsum((moves - full) * POW, 1), 0, 1, out=moves)

    def rotate(moves, full, piece):
        kick = o_kicks if piece == "o" else (i_kicks if piece == "i" else kicks)
        # loop through source and target rotations
        masks = 1 - full
        for i in kicks:
            move = torch.clone(moves[i // 10])
            mask = masks[i%10]
            for x, y, nx, ny in kick[i]:
                # add with offset, then subtract from source
                # break if all moves fulfilled
                if torch.sum(move) == 0:
                    break
                valids = move[nx:40-x, ny:10-y] & mask[x:40-nx, y:10-ny]
                moves[i % 10][x:40-nx, y:10-ny] |= valids
                move[nx:40-x, ny:10-y] -= valids

    def generate_moves(board, piece): 
        moves = torch.zeros(4, 40, 10, dtype=int)
        full = Tetris.conv(board, piece)
        moves = torch.zeros_like(full)
        moves[:,18] = full[:,18]
        Tetris.drop(moves, full)
        Tetris.rotate(moves, full, piece)
        Tetris.rotate(moves, full, piece)
        return moves
   
    def empty_board():
        return torch.zeros(40, 10)