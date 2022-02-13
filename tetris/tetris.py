from piece_data import pieces, kicks, rots, RNG

import numpy as np
from scipy.signal import correlate2d



class InvalidMove(Exception):
    pass


class GameOver(Exception):
    pass


class Tetris():
    def __init__(self, seed, b2b, combo):
        self.board = np.zeros((40, 10))
        self.rng = RNG(seed)
        self.convs = {}
        self.btb = b2b
        self.combo = combo

    def empty_board():
        return np.zeros((40, 10))

    def drop(self, i, j, rot, piece):
        while self.convs[piece][rot][i][j] == 0:
            i += 1
        return i - 1, j

    def rotate(self, i, j, rot, direc, piece):
        end = (rot + direc + 4) % 4

        if not end in self.convs["piece"]:
            self.convs[piece][end] = correlate2d(self.board, rots[piece][end], fillvalue=1)

        for offset in kicks[str(rot) + str(end)]:
            # offsets are evil and flipped
            if self.convs[piece][end][i + offset[1]][j + offset[0]] == 0:
                return i + offset[1], j + offset[0]
        raise InvalidMove()

    def simulate(self, col, rot, spin, piece, edge):
        """simulates dropping a piece on the board"""
        i = 18 + edge
        j = col + edge - 1
        if not piece in self.convs:
            self.convs[piece][rot] = correlate2d(self.board, rots[piece][rot], fillvalue=1)

        if self.convs[piece][rot][i][j] != 0:
            raise GameOver()

        i, j = self.drop(i, j, rot, piece)

        if spin == 0:
            return i, j

        while abs(spin) > 0:
            direc = spin // abs(spin)
            i, j = self.rotate(i, j, rot, direc, piece)
            rot = (rot + direc + 4) % 4
            i, j = self.drop(i, j, rot, piece)
            spin -= direc
        return i, j
    
    def project_piece(self, piece, i, j, rot):
        board = self.board.copy()
        end = rots[piece][rot]

        # cursed index manip to clip piece boundary
        w = max(0, i)
        z = max(0, j)
        y = min(end.shape[0], self.board.shape[0] - i)
        x = min(end.shape[1], self.board.shape[1] - j)

        board[w: i+y, z: j+x] += end[w-i: y, z-j: x]
        return board

    def place_piece(self, col, rot, spin, piece):
        shape = pieces[piece]
        # how much convolution overhangs the original array
        edge = shape.shape[0] - 1

        i, j = self.simulate(self.board, col, rot, spin, piece, edge)
        print(i, j)
        i, j = i - edge, j - edge

        disp = self.project_piece(piece, i, j, (rot + spin + 4) % 4)

        full = np.nonzero(np.sum(disp, axis=1) == 10)
        cleared = np.sum(full) 
        curr = 0
        if (np.any(full)):
            i = 39
            j = 0
            while cleared > curr:
                if full[i - j] == 10:
                    j += 1
                    cleared += 1
                else:
                    if j > 0:
                        disp[j:i + 1] = disp[:i - j + 1]
                        full[j:i + 1] = full[:i - j + 1]
                        j = 0
                    i -= 1
        return disp

    def pretty_print(board):
        s = "\n".join(["".join(["  " if j == 0 else "██" for j in i])
                      for i in board[21:]])


