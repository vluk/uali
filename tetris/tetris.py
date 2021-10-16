from piece_data import pieces, kicks

import numpy as np
import math
from scipy.signal import correlate2d

class InvalidMove(Exception):
    pass

class GameOver(Exception):
    pass

class RNG():
    def __init__(self, seed):

        self._seed = seed % 2147483647

        if (self._seed <= 0):
            self._seed += 2147483646

    def next(self):
        self._seed = self._seed * 16807 % 2147483647
        return self._seed

    def nextFloat(self):
        return (self.next() - 1) / 2147483646

    def shuffleArray(self, array):
        i = len(array)

        if (i == 0):
            return array

        for i in reversed(range(i)):
            j = math.floor(self.nextFloat() * (i + 1))
            array[i], array[j] = array[j], array[i]
        return array

    def getCurrentSeed(self):
        return self._seed


class Tetris():
    def __init__(self, seed):
        self.board = np.zeros((40, 10))
        self.rng = RNG(seed)
    
    def empty_board():
        return np.zeros((40, 10))
    
    def drop(self, i, j, rot, convs):
        while convs[rot][i][j] == 0:
            i += 1
        return i - 1, j
    
    def rotate(self, i, j, rot, direc, convs):
        end = (rot + direc + 4) % 4

        for offset in kicks[str(rot) + str(end)]:
            # offsets are evil and flipped
            if convs[end][i + offset[1]][j + offset[0]] == 0:
                return i + offset[1], j + offset[0]
        raise InvalidMove()

    def simulate(self, board, col, rot, spin, rots, edge):
        convs = [correlate2d(board, rots[i], fillvalue=1) for i in range(4)]
        i = 18 + edge
        j = col + edge - 1
        if convs[rot][i][j] != 0:
            raise GameOver()

        i, j = self.drop(i, j, rot, convs)
    
        if spin == 0:
            return i, j

        while abs(spin) > 0:
            direc = spin // abs(spin)
            i, j = self.rotate(i, j, rot, direc, convs)
            rot = (rot + direc + 4) % 4
            i, j = self.drop(i, j, rot, convs)
            spin -= direc
        return i, j

    def place_piece(self, board, col, rot, spin, piece):
        shape = pieces[piece]
        rots = [np.rot90(shape, i, axes=(1,0)) for i in range(4)]
        edge = shape.shape[0] - 1

        i, j = self.simulate(board, col, rot, spin, rots, edge)
        print(i, j)
        i, j = i - edge, j - edge

        end = rots[(rot + spin + 4) % 4]

        # cursed index manip to clip piece boundary
        w = max(0, i)
        z = max(0, j)

        y = min(end.shape[0], board.shape[0] - i)
        x = min(end.shape[1], board.shape[1] - j)

        board[w : i + y, z : j + x] += end[w - i : y, z - j:x]

        sums = np.sum(board, axis=1)
        if (np.max(sums) == board.shape[1]):
            i = 39 
            j = 0
            while i > 0:
                if sums[i - j] == 10:
                    j += 1
                else:
                    if j > 0:
                        self.pretty_print(board)
                        board[j:i + 1] = board[:i - j + 1]
                        sums[j:i + 1] = sums[:i - j + 1]
                        j = 0
                    i -= 1
        return board
    
    def pretty_print(self, board):
        s = "\n".join(["".join(["  " if j == 0 else "██" for j in i]) for i in board[21:]])
        print(s)


game = Tetris(1000)
board = Tetris.empty_board()
game.pretty_print(board)
board = game.place_piece(board, 4, 0, 0, "l")
game.pretty_print(board)
board = game.place_piece(board, 4, 0, 0, "s")
game.pretty_print(board)
board = game.place_piece(board, 8, 0, 0, "j")
game.pretty_print(board)
board = game.place_piece(board, 8, 0, 0, "z")
game.pretty_print(board)
board = game.place_piece(board, 5, 1, 0, "i")
game.pretty_print(board)
board = game.place_piece(board, 4, 0, 0, "t")
game.pretty_print(board)
board = game.place_piece(board, 3, 3, 0, "l")
game.pretty_print(board)
board = game.place_piece(board, 1, 0, 0, "o")
game.pretty_print(board)
board = game.place_piece(board, 0, 1, 0, "j")
game.pretty_print(board)
board = game.place_piece(board, 8, 1, 0, "o")
game.pretty_print(board)
board = game.place_piece(board, 8, 1, 0, "i")
game.pretty_print(board)
board = game.place_piece(board, 0, 1, -3, "t")
game.pretty_print(board)
board = game.place_piece(board, 5, 0, 0, "z")
game.pretty_print(board)
board = game.place_piece(board, 0, 1, -2, "t")
game.pretty_print(board)