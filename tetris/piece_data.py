import numpy as np
import math

"""from tetrio.js"""

kicks = {
    1: [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    10: [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    12: [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]],
    21: [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
    23: [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    32: [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
    30: [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
    3: [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
    2: [[0, 0], [0, -1], [1, -1], [-1, -1], [1, 0], [-1, 0]],
    13: [[0, 0], [1, 0], [1, -2], [1, -1], [0, -2], [0, -1]],
    20: [[0, 0], [0, 1], [-1, 1], [1, 1], [-1, 0], [1, 0]],
    31: [[0, 0], [-1, 0], [-1, -2], [-1, -1], [0, -2], [0, -1]]
}

"""converted from tetrio i kick table using TTC implementation offsets"""
"""read: https://harddrop.com/wiki/SRS#How_Guideline_SRS_Really_Works"""

i_kicks = {
    1: [[1, 0], [2, 0], [-1, 0], [-1, 1], [2, -2]],
    10: [[-1, 0], [-2, 0], [1, 0], [-2, 2], [1, -1]],
    12: [[0, -1], [-1, -1], [2, -1], [-1, -3], [2, 0]],
    21: [[0, 1], [-2, 1], [1, 1], [-2, 0], [1, 3]],
    23: [[-1, 0], [1, 0], [-2, 0], [1, -1], [-2, 2]],
    32: [[1, 0], [2, 0], [-1, 0], [2, -2], [-1, 1]],
    30: [[0, 1], [1, 1], [-2, 1], [1, 3], [-2, 0]],
    3: [[0, -1], [-1, -1], [2, -1], [2, 0], [-1, -3]],
    2: [[1, -1], [1, -2]],
    13: [[-1, -1], [0, -1]],
    20: [[-1, 1], [-1, 2]],
    31: [[1, 1], [0, 1]]
}

o_kicks = {
    1: [[0, 1]],
    2: [[1, 1]],
    3: [[1, 0]],
    10: [[0, -1]],
    12: [[1, 0]],
    13: [[1, -1]],
    20: [[-1, -1]],
    21: [[-1, 0]],
    23: [[0, -1]],
    30: [[-1, 0]],
    31: [[-1, 1]],
    32: [[0, 1]]
}

I = np.identity(40, dtype=int)
U1 = np.identity(41, dtype=int)[1:,:40]
U2 = U1 @ U1
U3 = U1 @ U1 @ U1
U = [U1, U2, U3]
L1 = np.identity(41, dtype=int)[:40,1:]
L2 = L1 @ L1
L3 = L1 @ L1 @ L1
L = [L1, L2, L3]

def shift(A, x, y):
    if x > 0:
        A = A @ U[x - 1]
    elif x < 0:
        A = A @ L[-x - 1]
    if y > 0:
        A = U[y - 1] @ A
    elif y < 0:
        A = L[-y - 1] @ A
    return A

def kickrow_to_matrix(row):
    return np.array([shift(I, k[0], k[1]) for k in row])

kickstack = {i: kickrow_to_matrix(kicks[i]) for i in kicks}
i_kickstack = {i: kickrow_to_matrix(i_kicks[i]) for i in i_kicks}
o_kickstack = {i: kickrow_to_matrix(o_kicks[i]) for i in o_kicks}

minos = ["z", "l", "o", "s", "i", "j", "t"]

pieces = {
    "i": np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], dtype=np.float32),
    "j": np.array([[1, 0, 0], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "l": np.array([[0, 0, 1], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "o": np.array([[0, 1, 1], [0, 1, 1], [0, 0, 0]], dtype=np.float32),
    "s": np.array([[0, 1, 1], [1, 1, 0], [0, 0, 0]], dtype=np.float32),
    "t": np.array([[0, 1, 0], [1, 1, 1], [0, 0, 0]], dtype=np.float32),
    "z": np.array([[1, 1, 0], [0, 1, 1], [0, 0, 0]], dtype=np.float32)
}

def attack(lines, tspin, mini, b2b, combo):
    """calculates attack, not counting all-clear bonus"""
    base = 0
    if tspin:
        base = lines * 2
    elif mini:
        base = lines // 2
    elif lines == 4:
        base = 4
    else:
        base = lines - 1

    r = base

    if b2b:
        r += int(np.log(b2b)) + 1

    if combo:
        r *= 1 + 0.25 * combo
    if base == 0 and combo > 2:
        r = np.log(combo * 1.26)
        print(r)
    return int(r)


rots = {mino: [np.rot90(pieces[mino], i, axes=(1, 0))
               for i in range(4)] for mino in minos}


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
