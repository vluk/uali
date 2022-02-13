from piece_data import rots, kick_kernals

import numpy as np
from scipy.signal import correlate2d

"""
After some thought, an input-based move generation approach
has some fundamental performance issues. We can use convolutions
and other linear algebra tricks to generate moves at a much higher
speed.
"""

TRIL = np.tril(np.ones((40, 40)), k=1)
TRIU = np.triu(np.ones((40, 40)), k=1)
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
        moves = np.clip(np.clip(right, 0, 1) + np.clip(left, 0, 1), 0, 1)
        return moves
    
    # please let me know if you know how this works, because i certainly don't
    def rotate(moves, full):
        empty = 1 - full
        rotates = np.zeros(empty.shape)
        # loop through rotations
        for i in range(1, 4):
            mask = np.roll(moves, i, axis=0) - empty
            # loop through states
            # it's not isomorphic, but it's non-branching which eases computation
            rmoves = np.array([correlate2d(mask[i], kick_kernals[str(j) + str((i + j) % 4)], fillvalue=0) for j in range(4)])[:,3:43, 3:13]
            print(rmoves.shape)
            rotates += np.clip(rmoves, 0, 1)
        moves = np.clip(rotates + moves, 0, 1)
        return moves
        
    
    def generate_moves(board, piece): 
        moves = np.zeros((4, 40, 10))
        moves[0][18][5] = 1
        full = np.array([correlate2d(board, rots[piece][i], fillvalue=1)[1:41,1:11] for i in range(4)])
        full = np.clip(full, 0, 1)
        moves = Tetris.rotate(moves, full)
        moves = Tetris.wiggle(moves, full)
        moves = Tetris.drop(moves, full)
        moves = Tetris.rotate(moves, full)
        return moves
    
    def empty_board():
        return np.zeros((40, 10))

    def pretty_print(board):
        s = "\n".join(["".join(["  " if j == 0 else "██" for j in i])
                      for i in board[21:]])
        print(s)

board = Tetris.empty_board()

board[30, 5] = 1
print(board)

Tetris.pretty_print(Tetris.generate_moves(board, "j")[0])