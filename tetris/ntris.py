from piece_data import rots, kickstack

import numpy as np
from scipy.signal import correlate2d

"""
After some thought, an input-based move generation approach
has some fundamental performance issues. We can use convolutions
and other linear algebra tricks to generate moves at a much higher
speed.
"""

TRIL = np.tril(np.ones((40, 40), dtype=int), k=1)
TRIU = np.triu(np.ones((40, 40), dtype=int), k=1)
POW = np.power(2, np.arange(40))

class Tetris():
    def drop(moves, full):
        """simulate soft drop"""
        moves = moves - full
        # TRI "drips" downwards
        # POW gives "priority" to lower elements
        moves = np.multiply(moves, POW[:, np.newaxis])
        moves = TRIL @ moves
        moves = np.clip(moves, 0, 1)
        return moves

    def wiggle(moves, full):
        """simulate left/right movement"""
        moves = moves - full 
        left = np.multiply(moves, POW[:10])
        left = left @ TRIU[:10, :10]
        right = np.multiply(moves, POW[:10][::-1])
        right = right @ TRIL[:10, :10]
        print(np.clip(left, 0, 1))
        moves = np.clip(right, 0, 1) & np.clip(left, 0, 1)
        return moves
    
    def rotate(moves, full):
        # loop through source and target rotations
        newmoves = np.zeros(moves.shape)
        for i in kickstack:
            mask = 1 - full[i % 10]
            move = moves[i // 10]
            k = kickstack[i]
            n, _, _ = k.shape
            l = np.transpose(k, (0, 2, 1)) @ np.multiply(((k @ move) & mask), POW[:n, np.newaxis, np.newaxis])
            newmoves[i % 10] += np.sum(k @ np.clip(l, 0, 1), axis=0)
        print(newmoves)

        moves = np.clip(newmoves + moves, 0, 1)
        return moves
        
    
    def generate_moves(board, piece): 
        moves = np.zeros((4, 40, 10), dtype=int)
        moves[0][18][5] = 1
        full = np.array([correlate2d(board, rots[piece][i], fillvalue=1)[1:41,1:11] for i in range(4)], dtype=int)
        full = np.clip(full, 0, 1)
        moves = Tetris.wiggle(moves, full)
        moves = Tetris.drop(moves, full)
        Tetris.pretty_print(moves[0])
        moves = Tetris.rotate(moves, full)
        return moves
    
    def empty_board():
        return np.zeros((40, 10))

    def pretty_print(board):
        s = "\n".join(["".join(["  " if j <= 0 else "██" for j in i])
                      for i in board[21:]])
        print(s)

board = Tetris.empty_board()

board[30, 5] = 1

Tetris.pretty_print(Tetris.generate_moves(board, "j")[0])